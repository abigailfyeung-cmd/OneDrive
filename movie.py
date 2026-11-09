import argparse
import csv
import contextlib
import html
import io
import math
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Iterable, TextIO


LABELS = ("negative", "positive")
TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")
TAG_PATTERN = re.compile(r"<[^>]+>")
DEFAULT_OUTPUT_PATH = Path(__file__).resolve().with_name("movie_output.txt")


class _Tee:
    def __init__(self, console: TextIO, output_file: TextIO) -> None:
        self.console = console
        self.output_file = output_file

    @property
    def encoding(self) -> str | None:
        return self.console.encoding

    def write(self, text: str) -> int:
        self.console.write(text)
        self.output_file.write(text)
        return len(text)

    def flush(self) -> None:
        self.console.flush()
        self.output_file.flush()

    def isatty(self) -> bool:
        return self.console.isatty()


class SentimentClassifier:
    def __init__(self) -> None:
        self.document_counts: Counter[str] = Counter()
        self.feature_counts = {label: Counter() for label in LABELS}
        self.feature_totals: Counter[str] = Counter()
        self.vocabulary: set[str] = set()

    @staticmethod
    def _features(text: str) -> Counter[str]:
        plain_text = TAG_PATTERN.sub(" ", html.unescape(text)).lower()
        tokens = TOKEN_PATTERN.findall(plain_text)
        features = Counter(tokens)
        features.update(
            f"BI:{first}_{second}" for first, second in zip(tokens, tokens[1:])
        )
        return features

    def fit(self, labeled_reviews: Iterable[tuple[str, str]]) -> None:
        self.document_counts.clear()
        self.feature_counts = {label: Counter() for label in LABELS}
        self.feature_totals.clear()
        self.vocabulary.clear()

        for review, label in labeled_reviews:
            if label not in LABELS:
                raise ValueError(f"Unsupported sentiment label: {label!r}")

            features = self._features(review)
            self.document_counts[label] += 1
            self.feature_counts[label].update(features)
            self.feature_totals[label] += sum(features.values())
            self.vocabulary.update(features)

        if not all(self.document_counts[label] for label in LABELS):
            raise ValueError("Training data must include positive and negative reviews.")
        if not self.vocabulary:
            raise ValueError("Training data must include at least one word or number.")

    def predict(self, review: str) -> str:
        if not self.vocabulary:
            raise ValueError("Train the classifier before predicting.")

        features = self._features(review)
        if not features:
            raise ValueError("Review must contain at least one word or number.")

        document_total = sum(self.document_counts.values())
        vocabulary_size = len(self.vocabulary)
        alpha = 1.0
        scores: dict[str, float] = {}

        for label in LABELS:
            score = math.log(self.document_counts[label] / document_total)
            denominator = self.feature_totals[label] + alpha * vocabulary_size
            for feature, count in features.items():
                probability = (
                    self.feature_counts[label][feature] + alpha
                ) / denominator
                score += count * math.log(probability)
            scores[label] = score

        best_label = max(LABELS, key=scores.__getitem__)
        return best_label


def _read_reviews(stream: TextIO) -> Iterable[tuple[str, str]]:
    reader = csv.DictReader(stream)
    if reader.fieldnames is None:
        raise ValueError("Dataset CSV is empty.")

    columns = {name.strip().lower(): name for name in reader.fieldnames if name}
    if "review" not in columns or "sentiment" not in columns:
        raise ValueError("Dataset CSV must contain 'review' and 'sentiment' columns.")

    for row_number, row in enumerate(reader, start=2):
        review = row.get(columns["review"])
        sentiment = row.get(columns["sentiment"])
        if review is None or sentiment is None:
            raise ValueError(f"Missing review or sentiment on CSV row {row_number}.")
        yield review, sentiment.strip().lower()


def load_reviews(dataset_path: Path) -> Iterable[tuple[str, str]]:
    if dataset_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(dataset_path) as archive:
            csv_names = [
                name for name in archive.namelist() if name.lower().endswith(".csv")
            ]
            if len(csv_names) != 1:
                raise ValueError(
                    "Dataset archive must contain exactly one CSV file."
                )
            with archive.open(csv_names[0]) as binary_stream:
                with io.TextIOWrapper(
                    binary_stream, encoding="utf-8-sig", newline=""
                ) as stream:
                    yield from _read_reviews(stream)
    else:
        with dataset_path.open(encoding="utf-8-sig", newline="") as stream:
            yield from _read_reviews(stream)


def display_reviews(
    labeled_reviews: Iterable[tuple[str, str]], classifier: SentimentClassifier
) -> tuple[int, float | None]:
    count = 0
    outcomes: Counter[tuple[str, str]] = Counter()
    for count, (review, original_sentiment) in enumerate(labeled_reviews, start=1):
        predicted_sentiment = classifier.predict(review)
        outcomes[original_sentiment, predicted_sentiment] += 1
        readable_review = " ".join(
            html.unescape(TAG_PATTERN.sub(" ", review)).split()
        )
        print(
            f"{count}. Original: {original_sentiment.title()} | "
            f"Predicted: {predicted_sentiment.title()} | Review: {readable_review}"
        )

    positive_positive = outcomes["positive", "positive"]
    positive_negative = outcomes["positive", "negative"]
    negative_positive = outcomes["negative", "positive"]
    negative_negative = outcomes["negative", "negative"]
    denominator = math.sqrt(
        (positive_positive + positive_negative)
        * (negative_positive + negative_negative)
        * (positive_positive + negative_positive)
        * (positive_negative + negative_negative)
    )
    pearson_score = (
        (positive_positive * negative_negative - positive_negative * negative_positive)
        / denominator
        if denominator
        else None
    )
    return count, pearson_score


def default_dataset_path() -> Path | None:
    candidates = (
        Path(__file__).resolve().parent / "IMDB Dataset.csv.zip",
        Path.home() / "Downloads" / "IMDB Dataset.csv.zip",
    )
    return next((path for path in candidates if path.is_file()), None)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Predict whether movie reviews express positive or negative sentiment."
    )
    parser.add_argument(
        "reviews",
        nargs="*",
        help="one or more reviews to classify",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        help="CSV or ZIP dataset path (defaults to IMDB Dataset.csv.zip in Downloads)",
    )
    parser.add_argument(
        "--show-all",
        action="store_true",
        help="print every dataset review alongside its positive/negative label (the default)",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="enter reviews interactively instead of listing the dataset",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"file for a copy of command output (default: {DEFAULT_OUTPUT_PATH})",
    )
    return parser


def _run(parser: argparse.ArgumentParser, argv: list[str] | None) -> int:
    args = parser.parse_args(argv)

    if args.interactive and (args.show_all or args.reviews):
        parser.error("--interactive cannot be used with --show-all or review text")
    if args.show_all and args.reviews:
        parser.error("--show-all cannot be used with review text arguments")

    dataset_path = args.dataset or default_dataset_path()
    if dataset_path is None:
        parser.error(
            "could not find IMDB Dataset.csv.zip; pass its location with --dataset"
        )
    if not dataset_path.is_file():
        parser.error(f"dataset file does not exist: {dataset_path}")

    classifier = SentimentClassifier()
    try:
        classifier.fit(load_reviews(dataset_path))
    except (OSError, ValueError, csv.Error, zipfile.BadZipFile) as error:
        parser.error(f"could not train from {dataset_path}: {error}")

    print(f"Trained on {sum(classifier.document_counts.values()):,} reviews.")
    if args.show_all or (not args.reviews and not args.interactive):
        try:
            count, pearson_score = display_reviews(
                load_reviews(dataset_path), classifier
            )
        except (OSError, ValueError, csv.Error, zipfile.BadZipFile) as error:
            parser.error(f"could not read reviews from {dataset_path}: {error}")
        print(f"Displayed {count:,} reviews.")
        if pearson_score is None:
            print("Pearson correlation (original vs. predicted): undefined")
        else:
            print(
                "Pearson correlation (original vs. predicted): "
                f"{pearson_score:.6f}"
            )
        return 0

    if args.reviews:
        try:
            for review in args.reviews:
                label = classifier.predict(review)
                print(f"{label.title()} feedback")
        except ValueError as error:
            parser.error(f"could not classify review: {error}")
    elif args.interactive:
        try:
            while True:
                review = input("Enter a review (blank to quit): ").strip()
                if not review:
                    break
                label = classifier.predict(review)
                print(f"{label.title()} feedback")
        except EOFError:
            pass

    return 0


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    output_parser = argparse.ArgumentParser(add_help=False)
    output_parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    output_parser.add_argument("--dataset", type=Path)
    output_args, _ = output_parser.parse_known_args(argv)

    output_path = output_args.output
    dataset_path = output_args.dataset or default_dataset_path()
    protected_paths = [Path(__file__).resolve()]
    if dataset_path is not None:
        protected_paths.append(dataset_path.resolve())
    if output_path.resolve() in protected_paths:
        print(
            f"Command output file cannot overwrite the script or dataset: {output_path}",
            file=sys.stderr,
        )
        return 2

    try:
        with output_path.open("w", encoding="utf-8", newline="") as output_file:
            stdout = _Tee(sys.stdout, output_file)
            stderr = _Tee(sys.stderr, output_file)
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = _run(_build_parser(), argv)
                print(f"Command output saved to {output_path}")
                return result
    except OSError as error:
        print(f"Could not write command output to {output_path}: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
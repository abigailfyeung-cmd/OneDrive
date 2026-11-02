import argparse
import csv
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


def default_dataset_path() -> Path | None:
    candidates = (
        Path(__file__).resolve().parent / "IMDB Dataset.csv.zip",
        Path.home() / "Downloads" / "IMDB Dataset.csv.zip",
    )
    return next((path for path in candidates if path.is_file()), None)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Predict whether movie reviews express positive or negative sentiment."
    )
    parser.add_argument(
        "reviews",
        nargs="*",
        help="one or more reviews to classify; omit to enter reviews interactively",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        help="CSV or ZIP dataset path (defaults to IMDB Dataset.csv.zip in Downloads)",
    )
    args = parser.parse_args(argv)

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
    if args.reviews:
        reviews = args.reviews
        try:
            for review in reviews:
                label = classifier.predict(review)
                print(f"{label.title()} feedback")
        except ValueError as error:
            parser.error(f"could not classify review: {error}")
    else:
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


if __name__ == "__main__":
    sys.exit(main())
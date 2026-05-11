import argparse
size_small = {1: 15, 2: 24, 3: 28, 4: 32, 5: 36, 6: 40, 7: 44, 8: 48, 9: 52, 10: 56, 11: 60, 12: 64, 13: 68, 14: 72, 15: 76, 16: 80}
size_medium = {1:15, 2:24, 3:28, 4:32, 5:36, 6:42, 7:47, 8:51, 9:56, 10:60, 11:65, 12:69, 13:74, 14:78, 15:83, 16:87}
size_large = {1:15, 2:24, 3:28, 4:32, 5:36, 6:45, 7:50, 8:55, 9:61, 10:66, 11:72, 12:77, 13:82, 14:88, 15:93, 16:99}
size_giant = {1:12, 2:22, 3:31, 4:38, 5:45, 6:49, 7:56, 8:64, 9:71, 10:79, 11:86, 12:93, 13:100, 14:107, 15:114, 16:121}

p = argparse.ArgumentParser(prog='test_results', description= 'hi')
p.add_argument("--age", type=int)
p.add_argument("--size", type=str, choices=["small", "medium", "large", "giant"])
args = p.parse_args()

# AGE always prints
if args.age is not None:
    if args.size == "small":
        if args.age in size_small.keys():
            print(size_small[args.age])
        else:
            print(args.age, "is not in size_small", size_medium)
    elif args.size == "medium":
        if args.age in size_medium.keys():
            print(size_medium[args.age])
        else:
            print(args.age, "is not in size_medium", size_medium)
    elif args.size == "large":
        if args.age in size_large.keys():
            print(size_large[args.age])
        else:
            print(args.age, "is not in size_large", size_large)
    elif args.size =="giant":
        if args.age in size_giant.keys():
            print(size_giant[args.age])
        else:
            print(args.age, "is not in size_giant", size_giant)









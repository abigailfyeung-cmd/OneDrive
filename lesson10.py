import argparse
#usd 
#rmb
#yen
#ntd
#wan

#usd - rmb = 6.8
#usd - yen = 160
#usd - ntd = 31.8
#usd - wan = 1490

p = argparse.ArgumentParser(prog='test_results', description= 'hi')
p.add_argument("--start", type=str)
p.add_argument("--end", type=str)
p.add_argument("--amount", type=int)
args = p.parse_args()

if args.amount is not None:
    if args.start == "usd":
        if args.end == "rmb":
            print (args.amount * 6.8)
        if args.end == "yen":
            print (args.amount * 160)
        if args.end == "ntd":
            print (args.amount * 31.8)
        if args.end == "wan":
            print (args.amount * 1490)
    if args.start == "rmb":
        if args.end == "usd":
            print (args.amount / args.start)
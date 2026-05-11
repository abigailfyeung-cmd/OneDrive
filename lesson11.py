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
    #start with usd is the args.amount
    usd_amount = args.amount
    if args.start != "usd":
        #translate to usd here:
        if args.start == "rmb":
            usd_amount = args.amount / 6.8
        elif args.start == "yen":
            usd_amount = args.amount / 160 
        elif args.start == "ntd":
            usd_amount = args.amount / 31.8
        elif args.start == "wan":
            usd_amount = args.amount / 1490
        
    if args.end == "rmb":
        print (usd_amount * 6.8)
    elif args.end == "yen":
        print (usd_amount * 160)
    elif args.end == "ntd":
        print (usd_amount * 31.8)
    elif args.end == "wan":
        print (usd_amount * 1490)


#import argparse
pot = {1: 15, 2: 24, 3: 28, 4: 32, 5: 36, 6: 40, 7: 44, 8: 48, 9: 52, 10: 56, 11: 60, 12: 64, 13: 68, 14: 72, 15: 76, 16: 80}

p = argparse.ArgumentParser(prog='test_results', description= 'hi')
p.add_argument('--age', type=int, help='0101101010101010101011010100101010101010', action="store", default='')
print(pot[p.parse_args().age])



small_age = {1: 15, 2: 24, 3: 28, 4: 32, 5: 36, 6: 40, 7: 44, 8: 48, 9: 52, 10: 56, 11: 60, 12: 64, 13: 68, 14: 72, 15: 76, 16: 80}



n = argparse.ArgumentParser(prog='test_results', description= 'hi')
n.add_argument("--size", type=int, help='0101101010101010101011010100101010101010', action="store", default='')
print(pot[n.parse_args([]).age])









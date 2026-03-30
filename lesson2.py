
import argparse
import sys
import csv
test_scores = {"Name" : ["Ann", "Bob", "Chris", "Derek"], "Math": [[70, 80, 90], [82, 62, 92], [73, 73, 73], [54, 94, 94]], "Eng" : [[20, 80, 70], [52, 82, 92], [93, 73, 33], [44, 74, 54]]}
#print(test_scores["Eng"])
parser = argparse.ArgumentParser(prog='test_results', description= 'hi')
parser.add_argument('--name', help='0101101010101010101011010100101010101010', action="store", default='')
args = parser.parse_args()
print(args.name)
if args.name == '' or args.name not in test_scores["Name"]:
   print("Error: bad name")
   sys.exit(1)
else:
   name_list = test_scores["Name"]
   name_index = name_list.index(args.name)
   math_scores = test_scores["Math"] [name_index]
   eng_scores = test_scores ["Eng"] [name_index]
   print("Math scores: ", math_scores)
   print("English scores: ", eng_scores)
   print(f"Name is in position {name_index}")
print("Program completed correctly")


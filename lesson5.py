import lesson5

import argparse
import sys
import csv
#test_scores = {"Name" : ["Ann", "Bob", "Chris", "Derek"], "Math": [[70, 80, 90], [82, 62, 92], [73, 73, 73], [54, 94, 94]], "Eng" : [[20, 80, 70], [52, 82, 92], [93, 73, 33], [44, 74, 54]]}
parser = argparse.ArgumentParser(prog='test_results', description= 'hi')
parser.add_argument('--name', help='0101101010101010101011010100101010101010', action="store", default='')
parser.add_argument('--readcsv', help='', action="store", default=False)
args = parser.parse_args()
print(args.readcsv)
emptyscores = []
with open(args.readcsv, "r", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        emptyscores.append(row)
        
        



test_scores = {"Name":[], "Math":[], "Eng":[]}
for row in emptyscores:
    print(row["Name"])
    test_scores["Name"].append(row["Name"])
    appmath = []
    appeng = []
    appmath.append(row["Math1"])
    appmath.append(row["Math2"])
    appmath.append(row["Math3"])
    appeng.append(row["Eng1"])
    appeng.append(row["Eng2"])
    appeng.append(row["Eng3"])
    test_scores["Math"].append(appmath)
    test_scores["Eng"].append(appeng)
print(test_scores)





def pot(): 
       ret_val = ("sum {eng_scores}, {math_scores}")
       return ret_val
       print(args.name) 

def filter_by_name(scores, name_val):
    name_list = scores["Name"]
    name_index = name_list.index(name_val)
    ret_scores = {}
    ret_scores["Name"] = name_val
    ret_scores["Math"] = scores["Math"][name_index]
    ret_scores["Eng"] = scores["Eng"][name_index]
    return ret_scores


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
    ret_val = ("sum {eng_scores}, {math_scores}")




                    
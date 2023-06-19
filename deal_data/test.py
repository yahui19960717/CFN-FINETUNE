
import json

def read_data(file):
    with open(file, "r", encoding="utf-8") as f:
        dic_g, dic_o = {}, {}
        data = json.load(f)
        for i in data:
            temp = "\t".join([str(i[0]), i[1]])
            if temp not in dic_g.keys():
                dic_g[temp] = 0
        print(len(dic_g))
        return dic_g

def compare(dic_1, dic_2):
    not_equal, equal = 0, 0
    for key in dic_1.keys():
        if key not in dic_2.keys():
            not_equal += 1
            print("error!")
        else:
            equal += 1
    print(not_equal)
if __name__=="__main__":
    task_guanwang_task_10000_seed1 ="../data/result-task1/B_task1_test-zsl-10000-seed1.json"
    task_guanwang_task_20000_seed1 = "../data/result-task1/B_task1_test-zsl-20000-seed1.json"
    task_guanwang_task_seed1 ="../data/result-task1/B_task1_test-zsl-seed1.json"
    task_guanwang_task_seed33 = "../data/result-task1/B_task1_test-zsl-seed33.json"
    # our = "../ccl-cfn/result_B/result-seed777/B_task1_test-zsl-seed777.json"
    guan = read_data(task_guanwang_task_10000_seed1)
    o = read_data(task_guanwang_task_20000_seed1)
    a11 = read_data(task_guanwang_task_seed1)
    a33 = read_data(task_guanwang_task_seed33)
    compare(guan, o)
    compare(o, a11)
    compare(a11, a33)

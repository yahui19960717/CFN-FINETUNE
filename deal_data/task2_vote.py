import json
from collections import defaultdict, Counter

def vote_data(file1, file2=None, file3=None, file4=None):
    dic = defaultdict(int)
    dic_arg = {}
    dic_1, s_list1 = read_data(file1)
    dic_2, s_list2 = read_data(file2) 
    dic_3, s_list3 = read_data(file3)
    dic_4, s_list4 = read_data(file4)
    # for i in s_list1:
    #     sentence_id, left_span_id, right_span_id = i[0], i[1], i[2]
    #     dic[(sentence_id, left_span_id, right_span_id)] += 10

    for i in s_list1+s_list2+s_list3+s_list4:
        sentence_id, left_span_id, right_span_id = i[0], i[1], i[2]
        dic[(sentence_id, left_span_id, right_span_id)] += 1
        if sentence_id not in dic_arg.keys():
            dic_arg[sentence_id] = []
            dic_arg[sentence_id].append([sentence_id, left_span_id, right_span_id])
        else:
            dic_arg[sentence_id].append([sentence_id, left_span_id, right_span_id])
    final_result = []
    for key, count_vote in dic.items():
        if count_vote >=2:
            final_result.append([key[0], key[1], key[2]])
    print(len(final_result))

    return final_result
    

def read_data(file1):
    dic_s, s_list = {}, []
    with open(file1, "r", encoding="utf-8") as f:
        data = json.load(f)
        for span in data:
            if span[0] not in dic_s.keys():
                dic_s[span[0]] = []
                dic_s[span[0]].append(span)
                s_list.append(span)
            else:
                dic_s[span[0]].append(span)
                s_list.append(span)
    print(len(dic_s), len(s_list))
    return dic_s,  s_list     

def obtain_submit_task2(data, f2):
     p_args = []
     with open(f2, "w", encoding="utf-8") as f_w:
        json.dump(data, f_w, ensure_ascii=False)
     
##B榜

model1 = "../data/result-task2/B_task2_test_20000_1.json"
model2 = "../data/result-task2/B_task2_test_20000_777.json"
model3 = "../data/result-task2/B_task2_test_1.json"
model4 = "../data/result-task2/B_task2_test_33.json"
final =  "../data/result-final/B_task2_test.json"
final_result = vote_data(model1, model2, model3, model4)
obtain_submit_task2(final_result,final)

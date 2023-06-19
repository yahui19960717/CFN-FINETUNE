
import json
from collections import defaultdict, Counter
from config import config

def vote_data(file1, file2=None, file3=None, file4=None):
    # dic = defaultdict(int)
    dic, final_result = {}, []
    dic_1, s_list1 = read_data(file1)
    dic_2, s_list2 = read_data(file2) 
    
    if file3!=None:
        dic_3, s_list3 = read_data(file3)
        dic_4, s_list4 = read_data(file4)
        for i in s_list1+s_list2+s_list3+s_list4:
            sentence_id, sense = i[0], i[1]
            # if 
            if sentence_id not in dic.keys():
                dic[sentence_id] = []
                dic[sentence_id].append(sense)
            else:
                dic[sentence_id].append(sense)
    else:
        for i in s_list1+s_list2:
            sentence_id, sense = i[0], i[1]
            # if 
            if sentence_id not in dic.keys():
                dic[sentence_id] = []
                dic[sentence_id].append(sense)
            else:
                dic[sentence_id].append(sense)        
    
    i = 0
    for key in dic.keys():
       vote_counts =  Counter(dic[key]) # Counter({'参加': 2, '参与': 1})
       most_common_labels = vote_counts.most_common(1) # [('参加', 2)]
       most_common_label, max_votes = most_common_labels[0] # 参加 2
       if max_votes == 1:
           i += 1
       final_result.append([key, most_common_label])
    print(i)
    return final_result

def read_data(file1):
    dic_s, s_list = {}, []
    with open(file1, "r", encoding="utf-8") as f:
        data = json.load(f)
        for span in data:
            if span[0] not in dic_s.keys():
                dic_s[span[0]] = span
                s_list.append(span)
    print(len(dic_s), len(s_list))
    return dic_s,  s_list     

def obtain_submit_task1(data, f1):
     p_args = []
     with open(f1, "w", encoding="utf-8") as f_w:
        json.dump(data, f_w, ensure_ascii=False)

if __name__=="__main__":     
    #####B榜

    model1 =   "../data/result-task1/B_task1_test-zsl-20000-seed1.json"
    model2 =   "../data/result-task1/B_task1_test-zsl-10000-seed1.json"
    model3 =   "../data/result-task1/B_task1_test-zsl-seed33.json"
    model4 =   "../data/result-task1/B_task1_test-zsl-seed1.json"
    final  =   "../data/result-final/B_task1_test.json"
    final_result = vote_data(model1, model2, model3, model4)
    obtain_submit_task1(final_result,final)

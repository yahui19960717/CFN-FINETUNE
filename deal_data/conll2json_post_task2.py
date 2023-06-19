from config import config
from preprocessing import get_sentences
from frames import get_frames
import json

class cfn_span:# frame element
    def __init__(self, obj) -> None:
        self.fe_name = obj["fe_name"]
        self.fe_abbr = obj["fe_abbr"]
        self.start = obj["start"]
        self.end = obj["end"]

def get_pred(file):
    with open(file, "r", encoding="utf-8") as f:
        sentences, s, words, pos, arg = [], [], [], [], []
        for line in f:
            if len(line.strip()) == 0:
                sentences.append([words, pos, arg])
                words,pos,arg = [], [], []
            else:
                words.append(line.strip().split()[1])
                pos.append(line.strip().split()[4])
                arg.append(line.strip().split()[8])
    print(len(sentences))
    return sentences

def get_final_results(pred, gold, id2frame):
    '''
    需要将gold的结果放在词典中，因为test中有重复的句子
    gold的数据需要通过句子+谓词来查找，因为可能一个句子有多个谓词
    '''
    dic_pred = {}
    for s in pred: # 词，词性，标签
        for i in range(len(s[2])):
            if ":" in s[2][i] and int(s[2][i].split(":")[0])==0:
                p_idx = i # 谓词从1开始
                p = s[2][i]
        words = "\t".join(["".join(s[0]), str(p_idx)])
        if words not in dic_pred.keys():
            dic_pred[words] = [s, p]
        else:
            print("重复句子:",words)
    print("预测的句子数为：", len(dic_pred))

    gold_dic = {}
    for s in gold:
        p_idx, p_word = s.get_pred_idx()
        temp = "\t".join([s.text, str(p_idx)])  
        if temp not in gold_dic.keys():
            gold_dic[temp] = s    # 原始数据
        if temp in dic_pred.keys(): 
            # 将预测的frame都填到数据中
            if str.isdigit(dic_pred[temp][1].split(":")[1]) == True:
                temp_frame = id2frame[int(dic_pred[temp][1].split(":")[1])]
                s.frame = temp_frame
            else:
                temp_frame = ""
            # 将预测的cfn论元都填到数据中
            sen, ws, las, w_idx_range = s.get_segmented_text()
            word_dic = {} # 用于存储每个句子分词后和分词前的下标
            for w_i in range(len(w_idx_range)):
                if w_idx_range[w_i][1] not in word_dic.keys():
                    word_dic[w_idx_range[w_i][1]] = w_idx_range[w_i] # ['中国队', 0, [0, 2]]
                else:
                    print("error!")
            args = []
            for pre_arg_i in range(len(dic_pred[temp][0][2])):
                if ":" in dic_pred[temp][0][2][pre_arg_i] and dic_pred[temp][0][2][pre_arg_i].split(":")[0] != 0:
                    bes_label = dic_pred[temp][0][2][pre_arg_i].split(":")[1].split("-")
                    temp_cfn = {}
                    if bes_label[0] == "S":
                        idx_arg = word_dic[pre_arg_i]
                        temp_cfn["start"] = idx_arg[2][0]
                        temp_cfn["end"] = idx_arg[2][1]
                        temp_cfn["fe_name"] = bes_label[1]
                        temp_cfn["fe_abbr"] = ""
                        args.append(cfn_span(temp_cfn))
                    elif bes_label[0] == "B":
                        idx_arg = word_dic[pre_arg_i]
                        temp_cfn["start"] = idx_arg[2][0]
                        flag = 1
                        for pre_arg_j in range(pre_arg_i+1, len(dic_pred[temp][0][2])):
                            if ":" in dic_pred[temp][0][2][pre_arg_j] and dic_pred[temp][0][2][pre_arg_j].split(":")[0] != 0:
                                bes_temp = dic_pred[temp][0][2][pre_arg_j].split(":")[1].split("-")
                                if bes_temp[0] == "E":
                                    temp_cfn["end"] = word_dic[pre_arg_j][2][1]
                                    flag = 0
                                    break
                        if flag == 1: # 如果只有B但没有E的标签
                        #    print( s.target,dic_pred[temp])
                            # print(bes_label)
                        #    temp_cfn["end"] = word_dic[pre_arg_j][2][1] = idx_arg[2][1]
                            # print("预测有错")
                            continue
                    
                        temp_cfn["fe_name"] = bes_label[1]
                        temp_cfn['fe_abbr'] = ""
                        args.append(cfn_span(temp_cfn))
            s.cfn_spans = args      
        else:
            print(temp)
            # print("error!预测中没有这个句子！")  
    print("原始数据中句子不重复的个数：",len(gold_dic))

    return gold

def data2json(file, sentences):
    with open(file, "w", encoding="utf-8") as f:
        s_list = []
        for s in sentences:
            dic, args = {}, []
            dic["sentence_id"] = s.sentence_id
            for arg in s.cfn_spans:
                # print({"start": "", "end": arg.end, "fe_abbr": "", "fe_name": arg.fe_name})
                args.append({"start": arg.start, "end": arg.end, "fe_abbr": "", "fe_name": arg.fe_name})
            dic["cfn_spans"] = args
            dic["frame"] = s.frame
            dic["target"] = s.target
            dic["text"] = s.text
            dic['word'] = s.word
            s_list.append(dic)
        json.dump(s_list,f, ensure_ascii=False)

def frame_f1(file):
    with open(file, 'r') as f:
        dev_data = json.load(f)

def obtain_submit_task2(file, f2):
     p_args = []
     with open(file, 'r') as f, open(f2, "w", encoding="utf-8") as f_w:
        data = json.load(f) 
        for s in data:
            for arg in s["cfn_spans"]:
                temp = [s["sentence_id"],arg["start"], arg["end"]]
                p_args.append(temp)
        json.dump(p_args, f_w, ensure_ascii=False)

def BI2BES(file1, file2):
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "w", encoding="utf-8") as f2:
        sentences = []
        for line in f1:
            sentences.append(line)
        for i in range(len(sentences)):
            if len(sentences[i].strip()) != 0:
                temp = sentences[i].strip().split()[8]
                if len(sentences[i+1].strip()) != 0:
                    temp_j = sentences[i+1].strip().split()[8]
                    if  temp != "_":
                        if temp.split(":")[1].split("-")[0] == "B":
                            if temp_j == "_" or temp_j.split(":")[1].split("-")[0] == "B" or temp_j.split(":")[1]=="[prd]":
                                label = "".join([temp.split(":")[0], ":", "S-", temp.split(":")[1].split("-")[1]])
                                f2.write("\t".join(["\t".join(sentences[i].strip().split("\t")[:8]), label, "\t".join(sentences[i].strip().split("\t")[9:])]))
                                f2.write("\n")
                            else:
                                f2.write(sentences[i])
                            
                        elif temp.split(":")[1].split("-")[0] == "I":
                            if temp_j == "_" or temp_j.split(":")[1].split("-")[0] == "B" or temp_j.split(":")[1]=="[prd]":
                                label = "".join([temp.split(":")[0], ":", "E-", temp.split(":")[1].split("-")[1]])  
                                f2.write("\t".join(["\t".join(sentences[i].strip().split("\t")[:8]), label, "\t".join(sentences[i].strip().split("\t")[9:])]))
                                f2.write("\n")       
                            else: 
                                f2.write("\t".join(["\t".join(sentences[i].strip().split("\t")[:8]), "_", "\t".join(sentences[i].strip().split("\t")[9:])]))
                                f2.write("\n")
                        elif temp.split(":")[1]=="[prd]":
                            f2.write(sentences[i])
                    else:
                        f2.write(sentences[i])
                else:
                    if temp != "_":
                        if temp.split(":")[1].split("-")[0] == "B":
                            label = "".join([temp.split(":")[0], ":", "S-", temp.split(":")[1].split("-")[1]])
                            f2.write("\t".join(["\t".join(sentences[i].strip().split("\t")[:8]), label, "\t".join(sentences[i].strip().split("\t")[9:])]))
                            f2.write("\n")
                        elif temp.split(":")[1].split("-")[0] == "I":
                            label = "".join([temp.split(":")[0], ":", "E-", temp.split(":")[1].split("-")[1]])
                            f2.write("\t".join(["\t".join(sentences[i].strip().split("\t")[:8]), label, "\t".join(sentences[i].strip().split("\t")[9:])]))
                            f2.write("\n")
                        elif temp.split(":")[1]=="[prd]":
                            f2.write(sentences[i])
                    else:
                        f2.write(sentences[i])
            else:
                f2.write(sentences[i])

if __name__=="__main__":

    # testB 数据转换
    ######################    task2   ########################
    #得到模型预测的结果
    testB_s = get_sentences(config["testB"]) # 获得原始的句子
    frames_,_,id2frame = get_frames(config['frame_info'])
    pred_testB_zy_20000_1 = "../crfsrl/pred/testB.dataenhance20000.seed1.conllu"
    pred_testB_zy_20000_777 = "../crfsrl/pred/testB.dataenhance20000.seed777.conllu"
    pred_testB_zy_1 = "../crfsrl/pred/testB.seed1.conllu"
    pred_testB_zy_33 = "../crfsrl/pred/testB.seed33.conllu"
    # 转化成BES格式：
    BI2BES(pred_testB_zy_20000_1, "../crfsrl/pred/testB.BES.dataenhance20000.seed1.conllu")
    BI2BES(pred_testB_zy_20000_777, "../crfsrl/pred/testB.BES.dataenhance20000.seed777.conllu")
    BI2BES(pred_testB_zy_1, "../crfsrl/pred/testB.BES.seed1.conllu")
    BI2BES(pred_testB_zy_33, "../crfsrl/pred/testB.BES.seed33.conllu")
    # 获得预测并获得json文件
    pred_testB_20000_1_s = get_pred("../crfsrl/pred/testB.BES.dataenhance20000.seed1.conllu") 
    results_1 = get_final_results(pred_testB_20000_1_s, testB_s, id2frame)
    data2json("../data/pred_json/testB.zy.dataenhance.20000.seed1.json", results_1)
    pred_testB_20000_777_s = get_pred("../crfsrl/pred/testB.BES.dataenhance20000.seed777.conllu") 
    results_2 = get_final_results(pred_testB_20000_777_s, testB_s, id2frame)
    data2json("../data/pred_json/testB.zy.dataenhance.20000.seed777.json", results_2)
    pred_testB_1_s = get_pred("../crfsrl/pred/testB.BES.seed1.conllu") 
    results_3 = get_final_results(pred_testB_1_s, testB_s, id2frame)
    data2json("../data/pred_json/testB.zy.seed1.json", results_3)
    pred_testB_33_s = get_pred( "../crfsrl/pred/testB.BES.seed33.conllu") 
    results_4 = get_final_results(pred_testB_33_s, testB_s, id2frame)
    data2json("../data/pred_json/testB.zy.seed33.json", results_4)
    # 获得组织方要求的task2格式
    obtain_submit_task2("../data/pred_json/testB.zy.dataenhance.20000.seed1.json", "../data/result-task2/B_task2_test_20000_1.json")
    obtain_submit_task2("../data/pred_json/testB.zy.dataenhance.20000.seed777.json","../data/result-task2/B_task2_test_20000_777.json")
    obtain_submit_task2("../data/pred_json/testB.zy.seed1.json", "../data/result-task2/B_task2_test_1.json")
    obtain_submit_task2("../data/pred_json/testB.zy.seed33.json","../data/result-task2/B_task2_test_33.json")
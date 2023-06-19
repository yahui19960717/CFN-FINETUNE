import random
from config import config
def read_data(file1): # 谓词是0:[pred]
    sentences, words, preds= [], [], []
    with open(file1, "r", encoding="utf-8") as f:
        for line in f:
            if len(line.strip())==0:
                sentences.append([words, preds])
                words, preds = [], []
            else:
                if line.strip().split("\t")[8] != "0:[prd]":
                    words.append(line.strip().split("\t")[1])
                    preds.append("_")
                else:
                    words.append(line.strip().split("\t")[1])
                    preds.append(line.strip().split("\t")[8])
    p_count = 0 
    s_dic = {}              
    for s in sentences:
        if " ".join(s[0]) not in s_dic.keys():
            s_dic[" ".join(s[0])] = []
        for i in range(len(s[1])):
            if s[1][i] == "0:[prd]":
                p_count += 1
                s_dic[" ".join(s[0])].append(i) # 谓词从0开始
    print(file1, ":", "句子数为:", len(sentences), "谓词数为：", p_count, "不重复的句子数为：",len(s_dic))
    return sentences, s_dic

def read_data_classified(file1): # 谓词是0:数字
    sentences, words, preds= [], [], []
    with open(file1, "r", encoding="utf-8") as f:
        for line in f:
            if len(line.strip())==0:
                sentences.append([words, preds])
                words, preds = [], []
            else:
                if line.strip().split("\t")[8]!="_" and str.isdigit(line.strip().split("\t")[8].split(":")[-1])==True:  
                    words.append(line.strip().split("\t")[1])
                    preds.append("0:[prd]")
                elif  line.strip().split("\t")[8]!="_" and str.isdigit(line.strip().split("\t")[8].split(":")[-1])==False:
                    words.append(line.strip().split("\t")[1])
                    preds.append("_") 
                else:                  
                    words.append(line.strip().split("\t")[1])
                    preds.append(line.strip().split("\t")[8])
    p_count = 0 
    s_dic = {}              
    for s in sentences:
        if " ".join(s[0]) not in s_dic.keys():
            s_dic[" ".join(s[0])] = []
        for i in range(len(s[1])):
            if s[1][i] == "0:[prd]":
                p_count += 1
                s_dic[" ".join(s[0])].append(i) # 谓词从0开始
    print(file1, ":", "句子数为:", len(sentences), "谓词数为：", p_count, "不重复的句子数为：",len(s_dic))
    return sentences, s_dic

def get_single_s(dic, file):
    new_dic = {}
    pred_count = 0
    sentences = []
    for key in dic.keys():
        new_dic[key] = []
        for i in dic[key]:
            pred_count+=1
            temp = ["_"]*i
            temp.extend(["0:[prd]"])
            temp.extend("_"*len(key.split(" ")[i+1:]))
            new_dic[key].append(temp)
            sentences.append([key, temp])
    assert len(sentences) == pred_count
    print("谓词的个数为：", pred_count)

    with open(file, "w", encoding="utf-8") as f_w:
        random.seed(1)
        random.shuffle(sentences)
        print(len(sentences[:20000]))
        for s in sentences[:20000]:
            for i in range(len(s[0].split())):
                f_w.write("\t".join([str(i+1),s[0].split()[i], s[0].split()[i], "_", "_", "_", "_", "_", s[1][i], "_"]))
                f_w.write("\n")
            f_w.write("\n")

def read_pred(file1, file2,file3):
    s1, s2 = [], []
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2,open(file3, "w", encoding="utf-8") as f3:
        for line in f1:
            s1.append(line)
        for line in f2:
            s2.append(line)
        s = s1 + s2
        print(len(s1), len(s2), len(s))
        for i in s:
            f3.write(i)
        
def deal_check(file1, file2):
    s1, _ = read_data_classified(file1)
    print(len(s1))
    s2, _ = read_data(file2)
    repeat_c = 0
    dic1, dic2 = {}, {}
    for  i in s1:
        dic1[" ".join(i[0])] = i
    for i in s2:
        dic2[" ".join(i[0])] = i
    for key in dic1.keys():
        if key in dic2.keys() and dic1[key]==dic2[key]:
            repeat_c += 1
            # print(dic1[key], dic2[key])
            # exit()
    
    print(repeat_c)

def cfn_train_dev(file1):
    sentences, words= [], []
    with open(file1, "r", encoding="utf-8") as f:
        for line in f:
            if len(line.strip())==0:
                sentences.append(words)
                words = []
            else:
                words.append(line.strip().split("\t")[1])
    print(len(sentences))
    return sentences

def exclude_train_dev(cfn, conll09):
    cfn_dic, dic_10000 = {}, {}
    for i in cfn:
        cfn_dic[" ".join(i)] =0
    print(len(cfn_dic)) # cfn train和dev的句子个数
    count_repeat = 0
    for key in conll09.keys():
        if key not in cfn_dic.keys():
            if 1 <= len(conll09[key]) <=3:
                dic_10000[key] = conll09[key][-1]
            if len(dic_10000) == 10000:
                break
    print(len(dic_10000))
    return dic_10000

def get_final_form(dic, file):
    new_dic = {}
    pred_count = 0
    sentences = []
    for key in dic.keys():
        temp = ["_"]*dic[key]
        temp.extend(["0:[prd]"])
        temp.extend("_"*len(key.split(" ")[dic[key]+1:]))
        new_dic[key] = temp
        sentences.append([key, temp])
    assert len(sentences) == 10000
    assert len(sentences) == len(new_dic)

    with open(file, "w", encoding="utf-8") as f_w:
        random.seed(1)
        random.shuffle(sentences)
        print(len(sentences))
        for s in sentences:
            for i in range(len(s[0].split())):
                f_w.write("\t".join([str(i+1),s[0].split()[i], s[0].split()[i], "_", "_", "_", "_", "_", s[1][i], "_"]))
                f_w.write("\n")
            f_w.write("\n")

if __name__ == "__main__":

    # 抽取conll09数据
    # 1	中国队	中国队	_	nz	_	_	_	_	_
    cfn_train = config["train_v2"]
    cfn_dev = config["dev_v2"]
    cfn_t = cfn_train_dev(cfn_train)
    cfn_d = cfn_train_dev(cfn_dev)
    # conll09数据，不知会不会有版权问题，所以没放conll09全部的数据集
    s_train, dic_train = read_data("/data/yhliu/Chinese-Frame-Semantic-Parsing/ccl-cfn/CoNLL_form/train.conllu")
    s_dev, dic_dev= read_data("/data/yhliu/Chinese-Frame-Semantic-Parsing/ccl-cfn/CoNLL_form/dev.conllu")
    s_test, dic_test= read_data("/data/yhliu/Chinese-Frame-Semantic-Parsing/ccl-cfn/CoNLL_form/test.conllu")
    dic_train.update(dic_dev)
    dic_train.update(dic_test)
    get_single_s(dic_train, "/data/yhliu/Chinese-Frame-Semantic-Parsing/ccl-cfn/CoNLL_form/conll09toCFN_20000.conllu")
    
    dic = exclude_train_dev(cfn_t+cfn_d, dic_train)
    get_final_form(dic,  "/data/yhliu/Chinese-Frame-Semantic-Parsing/ccl-cfn/CoNLL_form/conll09toCFN_10000.conllu")

    # 将获得数据conll09toCFN_20000.conllu和conll09toCFN_10000.conllu用基础的模型进行预测的结果
    SGP_conll_20000 = "CFN-finetune/SRL-as-GP/pred/dataenhance-20000.pred"
    SGP_conll_10000 = "CFN-finetune/SRL-as-GP/pred/dataenhance-20000.pred"
    crfsrl = "CFN-finetune/crfsrl/pred/dataenhance20000.pred"

    # 用预测的结果和原始训练数据进行混合
    train_bes = config["train_v2"]
    train_sgp_10000 = config["train_10000"]
    train_sgp_20000 = config["train_20000"]
    
    train_bii = config["crf_train"]
    train_cfn_20000 = config["crf_train_20000"]
    read_pred(SGP_conll_10000, train_bes, train_sgp_10000)
    read_pred(SGP_conll_20000, train_bes, train_sgp_20000)
    read_pred(crfsrl, train_bii, train_cfn_20000)
  
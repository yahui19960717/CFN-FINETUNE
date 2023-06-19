from config import config
import json

class Frame():

    def __init__(self, obj) -> None:
        self.frame_name = obj['frame_name'] # str
        self.frame_ename = obj["frame_ename"] # str
        self.frame_def = obj["frame_def"] # str
        self.fes = obj["fes"] # list
    
    def get_fes(self): 
        f_element = []
        # print(type(self.fes), self.fes[0].keys())
        for e in self.fes:
            f_element.append(Fe(e))
        # print(len(f_element), len(self.fes))
        return len(f_element), f_element


class Fe():# frame element
    def __init__(self, obj) -> None:
        self.fe_name = obj['fe_name']
        self.fe_abbr = obj['fe_abbr']
        self.fe_def = obj["fe_def"]

def get_frames(filepath):
    '''
    将frame定义为类，计算框架个数以及框架内的元素的个数
    '''
    with open(filepath, "r", encoding="utf-8") as f:
        frames = []
        dic_label = {}
        data = json.load(f)
        print(type(data), len(data)) # 692个框架
        n = 0 # 计算框架里面的元素个数
        for frame in data:
            # print(type(frame), frame.keys())
            frames.append(Frame(frame))
            n_fes, fes_= Frame(frame).get_fes()
            n += n_fes
            for e in fes_:
                # print(e.fe_name)
                if e.fe_name not in dic_label.keys():
                    dic_label[e.fe_name] = 0
        print("标签总个数：",len(dic_label))
        frame2id = map_frame2id(frames)
        id2frame = map_id2frame(frame2id)
        # print(id2frame)

    print("frame个数：", len(frames))
    print("frame中的论元总数：", n) # 平均一个frame有43个论元数？
    return frames, frame2id, id2frame
            
def map_id2frame(frame):
    dic = {}
    for key in frame.keys():
        if frame[key] not in dic.keys():
            dic[frame[key]] = key
    print(len(dic))   
    return dic

def map_frame2id(frames):
    dic = {}
    dic[""] = 0
    id = 1
    for i in frames:
        if i.frame_name not in dic.keys():
            dic[i.frame_name] = id
        id += 1
    
    return dic

def detect_pre(train, frames, id2frame):
    prd = 0
    dic = {}
    with open(train, "r", encoding="utf-8") as f:
        for line in f:
            if len(line.strip()) != 0:
                if "0:" in line.strip().split("\t")[8]:
                    if str.isdigit(line.strip().split("\t")[8].split(":")[1]):
                        dic[id2frame[int(line.strip().split("\t")[8].split(":")[1])]] =1
                        prd += 1
    print(prd, len(frames), len(dic))
    for i in frames:
        if i.frame_name not in dic.keys():
            print("error!", i.frame_name)

    

if __name__=="__main__":
    frames,_,id2frame= get_frames(config['frame_info'])
    # detect_pre(config["train_v2"], frames, id2frame)
    
    # result_frame2id = map_frame2id(frames)


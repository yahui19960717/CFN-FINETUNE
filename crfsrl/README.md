### 代码来源：基于下面论文的代码进行了修改
Yu Zhang, Qingrong Xia, Shilin Zhou, Yong Jiang, Guohong Fu, Min Zhang. _Semantic Role Labeling as Dependency Parsing: Exploring Latent Tree Structures Inside Arguments_. 2021. 

github网址：
Clone this repo recursively:
```sh
git clone https://github.com/yzhangcs/crfsrl.git --recursive
```

### 复现环境
```shell
conda env create -f environment.yaml
pip install -r  requirements.txt
```

### 数据说明
1. CFN-finetune/crfsrl/data/train.conllu:用于task1的训练数据
2. CFN-finetune/crfsrl/data/train_dataenhancezy.20000.conllu：数据增强了20000个conll句子的task2/3的训练数据
3. CFN-finetune/crfsrl/data/dev.conllu:用于task2/3的开发数据
4. CFN-finetune/crfsrl/data/testB_p.conllu：用于task2/3的B榜测试数据



### 代码说明：
/CFN-finetune/crfsrl/crf2o.py：参数配置文件
/CFN-finetune/SRL-as-GP/supar/cmds/cmd.py：参数配置文件
/CFN-finetune/SRL-as-GP/supar/parsers/srl.py：解析文件
/CFN-finetune/SRL-as-GP/supar/models/srl.py：模型代码

### 运行脚本
# 训练
/CFN-finetune/crfsrl/train.sh:训练脚本
```shell
sh train.sh
```
# 预测
/CFN-finetune/crfsrl/predict.sh：预测脚本
```shell
sh predict.sh
```

### 配置说明
# 训练脚本
  python -u crf2o.py train -b \
       -c configs/conll12.crf2o.srl.bert.ini \ ：配置文件
       --train data/train.conllu \ :训练数据路径
       --dev data/dev.conllu \ :开发数据路径
       --test data/test.conllu \ :测试数据路径
       --seed 777 \ ：随机数种子
       -p exp/xxx/model \ :存放模型的路径
       --batch-size=1000 \ ：指定在每次参数更新中用于计算梯度的样本数量
       --encoder bert \ ：编码器
       --bert bert-base-chinese \ ：指定bert
       --cache \ ：缓存数据
       --binarize \ ：二叉化
       --prd \ ：给定谓词设定
       --epochs=25 \ # 将整个训练数据集完整地通过神经网络训练一次的次数
       --finetune \ :使用Bert进行finetune
       -d 3 ：GPU id
# 预测脚本       
python -u crf2o.py  predict \
       -c configs/conll12.crf2o.srl.bert.ini   \  ：配置文件
       -p exp/xxx/model  \ ：模型路径
       --data  data/testB_p.conllu \ ：需要预测的数据路径
       --pred pred/testB.test.conllu \ ：预测结果的路径
       --bert=bert-base-chinese \ ：指定bert
       --prd  \  ：给定谓词设定
       -d 3 : GPU id


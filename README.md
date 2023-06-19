
# 如何训练和预测模型
### 一、任务1:使用SRL-asGP模型
#### 训练：使用SRL-as-GP/train.sh，需要跑四个模型，-d是gpu的id
1）使用conll09里面随机抽取的10000个句子进行数据增强,seed=1
python -m supar.cmds.vi_srl train -b \
        --train data/train_dataenhancezsl.10000.conllu\
        --dev data/dev.conllu \
        --test data/dev.conllu \
        --batch-size 400 \
        --unk "" \
        --epochs 60 \
        --encoder bert \
        --bert bert-base-chinese \
        --seed 1 \
        --schema BES \
        --train_given_prd \
        -p exp/dataenhance.zsl.10000.seed1/model \
        -d 1
2)使用conll09里面随机抽取的20000个句子进行数据增强,seed=1
python -m supar.cmds.vi_srl train -b \
        --train data/train_dataenhancezsl.20000.conllu\
        --dev data/dev.conllu \
        --test data/dev.conllu \
        --batch-size 400 \
        --unk "" \
        --epochs 60 \
        --encoder bert \
        --bert bert-base-chinese \
        --seed 1 \
        --schema BES \
        --train_given_prd \
        -p exp/dataenhance.zsl.20000.seed1/model \
        -d 2
3)使用原始的训练集进行数据增强，seed=1
python -m supar.cmds.vi_srl train -b \
        --train data/train.conllu\
        --dev data/dev.conllu \
        --test data/dev.conllu \
        --batch-size 400 \
        --unk "" \
        --epochs 60 \
        --encoder bert \
        --bert bert-base-chinese \
        --seed 1 \
        --schema BES \
        --train_given_prd \
        -p exp/dataenhance.zsl.seed1/model \
        -d 3
4）使用原始的训练集进行数据增强，seed=33
python -m supar.cmds.vi_srl train -b \
        --train data/train.conllu\
        --dev data/dev.conllu \
        --test data/dev.conllu \
        --batch-size 400 \
        --unk "" \
        --epochs 60 \
        --encoder bert \
        --bert bert-base-chinese \
        --seed 33 \
        --schema BES \
        --train_given_prd \
        -p exp/dataenhance.zsl.seed33/model \
        -d 4
#### 预测：使用SRL-as-GP/predict.sh,用四个训练的模型分别预测
1)使用conll09里面随机抽取的10000个句子进行数据增强的结果
python -m supar.cmds.vi_srl predict \
        --data data/testB_p.conllu\
        --batch-size 100 \
        -p exp/dataenhance.zsl.10000.seed1/model \
        --pred pred/testB.dataenhance.10000.seed1.pred \
        --task 05 \
        --schema BES \
        --given_prd \
        --vtb \
        -d 1
2)使用conll09里面随机抽取的20000个句子进行数据增强的结果
python -m supar.cmds.vi_srl predict \
        --data data/testB_p.conllu\
        --batch-size 100 \
        -p exp/dataenhance.zsl.20000.seed1/model \
        --pred pred/testB.dataenhance.20000.seed1.pred \
        --task 05 \
        --schema BES \
        --given_prd \
        --vtb \
        -d 2
3)使用原始的训练集进行数据增强的结果（seed=1）
python -m supar.cmds.vi_srl predict \
        --data data/testB_p.conllu\
        --batch-size 100 \
        -p exp/dataenhance.zsl.seed1/model \
        --pred pred/testB.seed1.pred \
        --task 05 \
        --schema BES \
        --given_prd \
        --vtb \
        -d 3
4）使用原始的训练集进行数据增强，seed=33
python -m supar.cmds.vi_srl predict \
        --data data/testB_p.conllu\
        --batch-size 100 \
        -p exp/dataenhance.zsl.seed33/model \
        --pred pred/testB.seed33.pred \
        --task 05 \
        --schema BES \
        --given_prd \
        --vtb \
        -d 4
#### 后处理 使用deal_data/conll2json_post_task1.py
1）使用deal_data/conll2json_post_task1.py得到组织方要求的结果
2）使用deal_data/task1_vote.py用获得的预测结果进行投票得到最终结果

### 二、任务2:使用crfsrl模型
#### 训练：使用crfsrl/train.sh，需要跑四个模型,-d是gpu的id
1）使用conll09里面随机抽取的20000个句子进行数据增强,seed=1
```shell
  python -u crf2o.py train -b \
       -c configs/conll12.crf2o.srl.bert.ini \
       --train data/train_dataenhancezy.20000.conllu \
       --dev data/dev.conllu \
       --test data/dev.conllu \
       --seed 1 \
       -d 1 \
       -p exp/dataenhance.zy.20000.seed1/model \
       --batch-size=1000 \
       --encoder bert \
       --bert bert-base-chinese \
       --cache \
       --binarize \
       --prd \
       --epochs=25 \
       --finetune 
```
2)使用conll09里面随机抽取的20000个句子进行数据增强,seed=777
```shell
  python -u crf2o.py train -b \
       -c configs/conll12.crf2o.srl.bert.ini \
       --train data/train_dataenhancezy.20000.conllu \
       --dev data/dev.conllu \
       --test data/dev.conllu \
       --seed 777 \
       -d 1 \
       -p exp/dataenhance.zy.20000.seed777/model \
       --batch-size=1000 \
       --encoder bert \
       --bert bert-base-chinese \
       --cache \
       --binarize \
       --prd \
       --epochs=25 \
       --finetune 
```
3)使用原始的训练集进行数据增强，seed=1
```shell
  python -u crf2o.py train -b \
       -c configs/conll12.crf2o.srl.bert.ini \
       --train data/train.conllu \
       --dev data/dev.conllu \
       --test data/dev.conllu \
       --seed 1 \
       -d 1 \
       -p exp/dataenhance.zy.seed1/model \
       --batch-size=1000 \
       --encoder bert \
       --bert bert-base-chinese \
       --cache \
       --binarize \
       --prd \
       --epochs=25 \
       --finetune 
```
4）使用原始的训练集进行数据增强，seed=33
```shell
  python -u crf2o.py train -b \
       -c configs/conll12.crf2o.srl.bert.ini \
       --train data/train.conllu \
       --dev data/dev.conllu \
       --test data/dev.conllu \
       --seed 33 \
       -d 1 \
       -p exp/dataenhance.zy.seed33/model \
       --batch-size=1000 \
       --encoder bert \
       --bert bert-base-chinese \
       --cache \
       --binarize \
       --prd \
       --epochs=25 \
       --finetune 
```
#### 预测：使用crfsrl/predict.sh,用四个训练的模型分别预测
1）使用conll09里面随机抽取的20000个句子进行数据增强的结果，seed=1
```shell
python -u crf2o.py  predict \
       -c configs/conll12.crf2o.srl.bert.ini   \
       --buckets 1 \
       -d 3 \
       -p exp/dataenhance.zy.20000.seed1/model  \
       --data  data/testB_p.conllu \
       --pred pred/testB.dataenhance20000.seed1.conllu\
       --bert=bert-base-chinese \
       --prd
```
2）使用conll09里面随机抽取的20000个句子进行数据增强的结果，seed=777
```shell
python -u crf2o.py  predict \
       -c configs/conll12.crf2o.srl.bert.ini   \
       --buckets 1 \
       -d 3 \
       -p exp/dataenhance.zy.20000.seed777/model  \
       --data  data/testB_p.conllu \
       --pred pred/testB.dataenhance20000.seed777.conllu\
       --bert=bert-base-chinese \
       --prd
```
3）使用原始的训练集进行数据增强的结果，seed=1
```shell
python -u crf2o.py  predict \
       -c configs/conll12.crf2o.srl.bert.ini   \
       --buckets 1 \
       -d 3 \
       -p exp/dataenhance.zy.seed1/model  \
       --data  data/testB_p.conllu \
       --pred pred/testB.seed1.conllu \
       --bert=bert-base-chinese \
       --prd
```
4）使用原始的训练集进行数据增强的结果，seed=33
```shell
python -u crf2o.py  predict \
       -c configs/conll12.crf2o.srl.bert.ini   \
       --buckets 1 \
       -d 3 \
       -p exp/dataenhance.zy.seed33/model  \
       --data  data/testB_p.conllu \
       --pred pred/testB.seed33.conllu \
       --bert=bert-base-chinese \
       --prd
```
#### 后处理 使用deal_data/conll2json_post_task2.py
1）使用deal_data/conll2json_post_task2.py得到组织方要求的结果
2）使用deal_data/task2_vote.py用获得的预测结果进行投票得到最终结果

### 三、任务3:使用crfsrl模型
#### 训练：使用crfsrl/train.sh，需要跑三个模型，但有一个模型（exp/dataenhance.zy.20000.seed777/model）在任务2已经跑完了，预测结果可以直接用，所以只需要再跑两个模型
1）使用conll09里面随机抽取的10000个句子进行数据增强,seed=777
```shell
  python -u crf2o.py train -b \
       -c configs/conll12.crf2o.srl.bert.ini \
       --train data/train_dataenhancezy.10000.conllu \
       --dev data/dev.conllu \
       --test data/dev.conllu \
       --seed 777 \
       -d 1 \
       -p exp/dataenhance.zy.10000.seed777/model \
       --batch-size=1000 \
       --encoder bert \
       --bert bert-base-chinese \
       --cache \
       --binarize \
       --prd \
       --epochs=25 \
       --finetune 
```
2)使用原始的训练集进行数据增强，seed=777
```shell
  python -u crf2o.py train -b \
       -c configs/conll12.crf2o.srl.bert.ini \
       --train data/train.conllu \
       --dev data/dev.conllu \
       --test data/dev.conllu \
       --seed 777 \
       -d 1 \
       -p exp/dataenhance.zy.seed777/model \
       --batch-size=1000 \
       --encoder bert \
       --bert bert-base-chinese \
       --cache \
       --binarize \
       --prd \
       --epochs=25 \
       --finetune 
```
#### 预测：使用crfsrl/predict.sh,用四个训练的模型分别预测
1）使用conll09里面随机抽取的10000个句子进行数据增强的结果，seed=777
```shell
python -u crf2o.py  predict \
       -c configs/conll12.crf2o.srl.bert.ini   \
       --buckets 1 \
       -d 3 \
       -p exp/dataenhance.zy.10000.seed777/model  \
       --data  data/testB_p.conllu \
       --pred pred/testB.dataenhance10000.seed777.conllu\
       --bert=bert-base-chinese \
       --prd
```
2）使用原始的训练集进行数据增强的结果，seed=777
```shell
python -u crf2o.py  predict \
       -c configs/conll12.crf2o.srl.bert.ini   \
       --buckets 1 \
       -d 3 \
       -p exp/dataenhance.zy.seed777/model  \
       --data  data/testB_p.conllu \
       --pred pred/testB.seed777.conllu \
       --bert=bert-base-chinese \
       --prd
```
#### 后处理 使用deal_data/conll2json_post_task3.py
1）使用deal_data/conll2json_post_task3.py得到组织方要求的结果
2）使用deal_data/task3_vote.py用获得的预测结果进行投票得到最终结果





---------------------------分割线 之前的README.md---------------------------







#### data：组织方提供的数据集

#### deal_data: 数据处理（预处理和后处理）

#### SRL-as-GP：用于跑task1。具体来说就是，在MTL的框架下进行框架识别、论元范围识别及论元角色识别，但我们只使用了框架识别的结果，将基于span的CFN转化为基于词的图解析，图表示采用BES。

#### crfsrl:用于跑task2和task3。将CFN任务转化为树解析任务。

文件夹下都有其对应的README.md文件

#### 具体实验介绍

1）Task1:在数据增强方法的基础上使用了投票机制，随机抽取20000个conll09的数据用原始数据训练的模型（seed=1）进行预测，然后将结果混入原始训练集再训练一个模型（seed=1），随机抽取10000个conll09的数据用原始数据训练的模型（seed=1）进行预测，然后将结果混入原始训练集训练一个模型（seed=1），使用原始training data训练了两个模型（seed=1和seed=33），然后进行投票。（多个模型的参数总共约473M）

2）Task2:在数据增强方法的基础上使用了投票机制，随机抽取20000个conll09的数据用原始数据训练的模型（seed=1）进行预测，然后将结果混入原始训练集后训练了两个模型（seed=1和seed=777）和原始训练数据训练了两个模型（seed=1, seed=33)，然后进行M投票。（多个模型的参数总共约448M）

3）Task3:在数据增强方法的基础上使用了投票机制，随机抽取20000个conll09的数据用原始数据训练的模型（seed=1）进行预测，然后将结果混入原始训练集再训练一个模型（seed=777），随机抽取10000个conll09的数据用原始数据训练的模型（seed=1）进行预测，然后将结果混入原始训练集训练一个模型（seed=777），使用原始training data训练了一个模型（seed=777），然后进行投票。（多个模型的参数总共约为337M）
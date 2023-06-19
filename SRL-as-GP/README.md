### 代码来源：基于下面论文的代码进行了修改
《Fast and Accurate End-to-End Span-based Semantic Role Labeling as Word-based Graph Parsing》
This is the repo for SRLasSDGP, a novel approach to form span-based SRL as word-based graph parsing, to be presented at [COLING2022](https://coling2022.org/coling). A preprint of the paper can be found at the [following location on arxiv](https://arxiv.org/abs/2112.02970).

### 复现环境
```shell
conda env create -f environment.yaml
pip install -r  requirements.txt
```
### 数据说明
1. CFN-finetune/SRL-as-GP/data/train.conllu:用于task1的训练数据
2. CFN-finetune/SRL-as-GP/data/train_dataenhancezsl.10000.conllu：数据增强了10000个conll句子的task1的训练数据
3. CFN-finetune/SRL-as-GP/data/train_dataenhancezsl.20000.conllu：数据增强了20000个conll句子的task1的训练数据
4. CFN-finetune/SRL-as-GP/data/dev.conllu::用于task1的开发数据
5. CFN-finetune/SRL-as-GP/data/testB_p.conllu ：用于task1的B榜测试数据

### 代码说明：
/CFN-finetune/SRL-as-GP/supar/cmds/vi_srl.py：参数配置文件
/CFN-finetune/SRL-as-GP/supar/cmds/cmd.py：参数配置文件
/CFN-finetune/SRL-as-GP/supar/parsers/srl.py：解析文件
/CFN-finetune/SRL-as-GP/supar/models/srl.py：模型代码

### 运行脚本
# 训练
/CFN-finetune/SRL-as-GP/train.sh:训练脚本
```shell
sh train.sh
```
# 预测
/CFN-finetune/SRL-as-GP/predict.sh：预测脚本
```shell
sh predict.sh
```

### 配置说明
# 训练脚本
python -m supar.cmds.vi_srl train -b \
        --train  train.conllu \ :训练数据路径
        --dev   dev.conllu \:开发数据路径
        --test  test.conllu \:测试数据路径
        --batch-size 400 \ ：指定在每次参数更新中用于计算梯度的样本数量
        --epochs 60 \ ：迭代次数
        --encoder bert \ 编码器
        --bert bert-base-chinese \:使用的bert类型
        --seed 1 \ :随机数种子
        --schema BES \ ：选择图表示的类型
        --train_given_prd \ # 给定谓词的设定
        -p exp/xxx/model \ :存放模型的路径
        -d 3  :GPU
# 预测脚本       
python -m supar.cmds.vi_srl predict \
        --data test.conllu \ ：需要预测的文件路径
        --batch-size 100 \ ：指定在每次参数更新中用于计算梯度的样本数量
        -p exp/xx/model \ :存放模型的路径
        --pred pred/testB.seed33.pred \ :预测的结果路径
        --task 05 \ ：任务选择（可以不用管）
        --schema BES \ ：选择图表示的类型
        --given_prd \ ： 给定谓词的设定
        --vtb \ ： 使用受约束的维特比进行解码
        -d 3   : GPU id





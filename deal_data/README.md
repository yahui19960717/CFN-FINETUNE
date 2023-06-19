
### 代码说明

# 数据路径配置 CFN-finetune/deal_data/config.py

# 预处理代码 
1. CFN-finetune/deal_data/frames.py：处理frames，映射成数字，用于task1的框架识别.
2. CFN-finetune/deal_data/preprocessing.py：获得模型需要的输入。
3. extract_conll09.py ：抽取conll09的数据用于数据增强。


# 后处理代码 
1）CFN-finetune/deal_data/conll2json_post.py ：获得不同模型的预测结果;
2）CFN-finetune/deal_data/task1_vote.py：将CFN-finetune/data/result-task1中的结果进行投票，为最终task1的结果;
3）CFN-finetune/deal_data/task2_vote.py ：将CFN-finetune/data/result-task2中的结果进行投票，为最终task2的结果;
4）CFN-finetune/deal_data/task3_vote.py ：将CFN-finetune/data/result-task3中的结果进行投票，为最终task3的结果.

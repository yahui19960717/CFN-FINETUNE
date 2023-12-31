  python -u crf2o.py train -b \
       -c configs/conll12.crf2o.srl.bert.ini \
       --train data/train_dataenhancezy.20000.conllu \
       --dev data/dev.conllu \
       --test data/dev.conllu \
       --seed 777 \
       -d 2 \
       -p exp/dataenhance.zy.20000.seed777/model \
       --batch-size=1000 \
       --encoder bert \
       --bert bert-base-chinese \
       --cache \
       --binarize \
       --prd \
       --epochs=25 \
       --finetune
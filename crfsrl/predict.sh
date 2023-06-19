python -u crf2o.py  predict \
       -c configs/conll12.crf2o.srl.bert.ini   \
       --buckets 1 \
       -d 3 \
       -p exp/dataenhance.zy.20000.seed777/model  \
       --data  data/testB_p.conllu \
       --pred pred/testB.dataenhance20000.seed777.conllu\
       --bert=bert-base-chinese \
       --prd
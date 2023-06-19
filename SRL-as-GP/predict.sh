python -m supar.cmds.vi_srl predict \
        --data data/testB_p.conllu\
        --batch-size 100 \
        -p exp/dataenhance.zsl.10000.seed1/model \
        --pred pred/testB.dataenhance.10000.seed1.pred \
        --task 05 \
        --schema BES \
        --given_prd \
        --vtb \
        -d 3
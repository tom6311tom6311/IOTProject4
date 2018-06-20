#!/bin/bash

if [ $1 ]; then
  data_dir=$1
else
  data_dir="data"
fi

if [ ! -d "$1" ]; then
  mkdir $data_dir
else
  rm -r $data_dir/*
fi

curl -o $data_dir/zh.tsv -L https://www.dropbox.com/s/gh3zk6rze7xegi0/zh.tsv?dl=1
curl -o $data_dir/dict.txt.big -L https://github.com/fxsjy/jieba/raw/master/extra_dict/dict.txt.big

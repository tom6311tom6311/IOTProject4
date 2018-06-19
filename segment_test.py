# _*_ coding: utf-8 _*_

import jieba

raw_sentence = "聾子聽見啞巴說瞎子看到鬼"

segmented_sentence = jieba.cut(raw_sentence)

print(' '.join(segmented_sentence))
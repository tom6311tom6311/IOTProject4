#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys
import numpy as np
import jieba.posseg
import random



def progress(count, total, suffix=''):
  bar_len = 60
  filled_len = int(round(bar_len * count / float(total)))
  percents = round(100.0 * count / float(total), 1)
  bar = '#' * filled_len + '-' * (bar_len - filled_len)
  sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
  sys.stdout.flush()

def closest_nodes(node, nodes, num):
  deltas = nodes - node
  dist_2 = np.einsum('ij,ij->i', deltas, deltas)
  return np.argsort(dist_2)[:num]

class WordAnalyzer:
  def __init__(self):
    self.load_word_embed()

  def load_word_embed(self, path='data/zh.tsv'):
    print('loading...')
    lines = []
    with open(path, 'r') as f:
      lines = f.readlines()
      f.close()
    word2id = {}
    id2word = []
    id2embed = []
    vec_temp = []
    for idx, line in enumerate(lines):
      if '\t' in line:
        [word_id, word, vec_temp] = line.split('\t')
        word2id[word] = int(word_id)
        vec_temp = [float(e) for e in vec_temp[2:].split(' ') if e != '']
      elif ']' in line:
        vec_temp.extend([float(e) for e in line[2:-2].split(' ') if e != ''])
        id2word.append(word)
        id2embed.append(np.array(vec_temp))
      else:
        vec_temp.extend([float(e) for e in line[2:].split(' ') if e != ''])
      progress(idx + 1, len(lines))
    print('\n Embed finished')
    self.word2id = word2id
    self.id2word = id2word
    self.id2embed = id2embed

  def find_closest_words(self, word, num=25):
    word_ids = closest_nodes(self.id2embed[self.word2id[word]], self.id2embed, num)
    return [self.id2word[i] for i in word_ids]

  def find_similar_sentence(self, sentence, random_choice=True, use_jieba_seg=True, rest_sentence=''):
    if use_jieba_seg:
      j_sentence = list(jieba.posseg.cut(sentence))
      if len(sentence) == 1:
        if sentence not in self.word2id:
          return ['ㄜ']
        j_w = j_sentence[0]
        closest_words = self.find_closest_words(sentence)
        closest_words = [c_w for c_w in closest_words if len(c_w) == 1]
        closest_j_words = [list(jieba.posseg.cut(w))[0] for w in closest_words]
        # closest_j_words = [closest_j_words[i] for i in range(len(closest_j_words)) if closest_j_words[i].word == closest_words[i]]
        suit_words = [c_j_w.word for c_j_w in closest_j_words if c_j_w.flag == j_w.flag and c_j_w.word != j_w.word]
        if len(suit_words) >= 1:
          return [random.choice(suit_words)] if random_choice else [suit_words[0]]
        else:
          return [j_w.word]

      if (j_sentence[0]).word == sentence:
        if sentence not in self.word2id:
          return ['ㄜ' * len(sentence)]
        j_w = j_sentence[0]
        closest_words = self.find_closest_words(sentence)
        closest_words = [c_w for c_w in closest_words if len(c_w) == len(sentence)]
        closest_j_words = [list(jieba.posseg.cut(w))[0] for w in closest_words]
        closest_j_words = [closest_j_words[i] for i in range(len(closest_j_words)) if closest_j_words[i].word == closest_words[i]]
        suit_words = [c_j_w.word for c_j_w in closest_j_words if c_j_w.flag == j_w.flag and c_j_w.word != j_w.word]
        if len(suit_words) >= 1:
          return [random.choice(suit_words)] if random_choice else [suit_words[0]]
        else:
          return [j_w.word]
      sim_sentence = []
      for j_w in j_sentence:
        sim_sentence.extend(self.find_similar_sentence(j_w.word, random_choice))
      return sim_sentence
    else:
      if sentence == '':
        return []
      if sentence in self.word2id:
        print('a')
        closest_words = self.find_closest_words(sentence)
        closest_words = [c_w for c_w in closest_words if len(c_w) == len(sentence) and c_w != sentence]
        if len(closest_words) != 0:
          print('c')
          sentence_part = [random.choice(closest_words)] if random_choice else [closest_words[0]]
          return sentence_part + self.find_similar_sentence(rest_sentence, random_choice, use_jieba_seg, '')
        else:
          print('d')
          if len(sentence) == 1:
            return ['ㄜ'] + self.find_similar_sentence(rest_sentence, random_choice, use_jieba_seg, '')
          else:
            return self.find_similar_sentence(sentence[:-1], random_choice, use_jieba_seg, sentence[-1] + rest_sentence)
      else:
        print('b')
        if len(sentence) == 1:
          return ['ㄜ'] + self.find_similar_sentence(rest_sentence, random_choice, use_jieba_seg, '')
        else:
          return self.find_similar_sentence(sentence[:-1], random_choice, use_jieba_seg, sentence[-1] + rest_sentence)


def main():
  jieba.set_dictionary('data/dict.txt.big')
  word_analyzer = WordAnalyzer()
  while True:
    sentence = input("請输入句子：")
    similar_seg_sentence = word_analyzer.find_similar_sentence(sentence, random_choice=False, use_jieba_seg=False)
    print('照樣造句：', ' '.join(similar_seg_sentence))

if __name__ == '__main__':
  main()

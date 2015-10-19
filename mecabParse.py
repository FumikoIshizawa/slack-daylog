# -*- coding: utf-8 -*-

import MeCab
import re

class MecabParse:
  tagger = MeCab.Tagger("-Ochasen")
  STOPWORD = " 。 、 「 」 （ ） \? ？ ： ， , ． ! ！ # \$ % & ' \( \) = ~ \| ` { } \* \+ \? _ > \[ \] @ : ; / \. ¥ \^ 【 】 ［ ］￥ ＿ ／ 『 』 ＞ ？ ＿ ＊ ＋ ｀ ｜ 〜 ＊ ＋ ＞ ？ ＃ ” ＃ ＄ ％ ＆ ’ \" ・ tpl".split()
  RE = []
  for s_word in STOPWORD:
    pattern = re.compile(r'.*%s.*' % s_word)
    RE.append(pattern)

  url_pattern = r'<http.*>'
  mention_pattern = r'<@.*>'
  emoji_pattern = r':[a-z]*:'

  def __init__(self):
    self.count_url = 0
    self.count_emoji = 0
    self.count_mention = 0

  def get_params(self):
    return [self.count_url, self.count_mention, self.count_emoji]

  def _replace_url(self, text):
    if re.search(re.compile(self.url_pattern), text) != None:
      self.count_url += 1
    return re.sub(self.url_pattern, "URL", text)

  def _replace_mention(self, text):
    if re.search(re.compile(self.mention_pattern), text) != None:
      self.count_mention += 1
    return re.sub(self.mention_pattern, "MENTION", text)

  def _replace_emoji(self, text):
    if re.search(re.compile(self.emoji_pattern), text) != None:
      self.count_emoji += 1
    return re.sub(self.emoji_pattern, "EMOJI", text)

  def _is_stopword(self, node):
    for rexp in self.RE:
      if rexp.match(node.surface) or node.feature.split(',')[0] == 'BOS/EOS':
        return True
    return False

  def parse_wordpart(self, text):
    node = self.parse(text)
    lines = []
    while node:
      line = []
      if self._is_stopword(node):
        node = node.next
        continue
      feature = node.feature.split(',')
      # feature内の単語(6)と品詞(0)
      line.append(feature[6])
      line.append(feature[0])
      lines.append(line)
      node = node.next

    return lines

  def parse(self,text):
    text = self._replace_url(text)
    text = self._replace_mention(text)
    text = self._replace_emoji(text)
    self.tagger.parse('')
    node = self.tagger.parseToNode(text)

    return node
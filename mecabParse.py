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
  mention_patten = r'<@.*>'
  emoji_patten = r':[a-z]*:'

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

  def _replace_mention(self,text):
    if re.search(re.compile(self.mention_patten), text) != None:
      self.count_mention += 1
    return re.sub(self.mention_patten, "MENTION", text)

  def _replace_emoji(self,text):
    if re.search(re.compile(self.emoji_patten), text) != None:
      self.count_emoji += 1
    return re.sub(self.emoji_patten, "EMOJI", text)

  def parse(self,text):
    text = self._replace_url(text)
    text = self._replace_mention(text)
    text = self._replace_emoji(text)
    self.tagger.parse('')
    node = self.tagger.parseToNode(text)
    while node:
      print(node.surface + '\t' + node.feature)
      node = node.next

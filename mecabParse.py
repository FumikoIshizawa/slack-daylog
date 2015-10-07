import MeCab
import re

tagger = MeCab.Tagger ("-Ochasen")
STOPWORD = " 。 、 「 」 （ ） \? ？ ： ， , ． ! ！ # \$ % & ' \( \) = ~ \| ` { } \* \+ \? _ > \[ \] @ : ; / \. ¥ \^ 【 】 ［ ］￥ ＿ ／ 『 』 ＞ ？ ＿ ＊ ＋ ｀ ｜ 〜 ＊ ＋ ＞ ？ ＃ ” ＃ ＄ ％ ＆ ’ \" ・ tpl".split()
RE = []
for s_word in STOPWORD:
  pattern = re.compile(r'.*%s.*' % s_word)
  RE.append(pattern)

url_pattern = re.compile(r'<http.*>')
mention_patten = re.compile(r'<@.*>')

def replace_url(text):
  return re.sub(r'<http.*>', "URL", text)

def replace_mention(text):
  return re.sub(r'<@.*>', "MENTION", text)

def replace_emoji(text):
  return re.sub(r':[a-z]+:', "EMOJI", text)

def parse(text):
  text = replace_url(text)
  text = replace_mention(text)
  text = replace_emoji(text)
  node = tagger.parseToNode(text)
  while node:
    print(node.surface + '\t' + node.feature)
    node = node.next
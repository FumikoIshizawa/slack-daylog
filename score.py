# -*- coding: utf-8 -*-

score_num_log = [0.2, 0.4, 0.6, 0.8, 1.0]
threshold_num_log = [0, 3, 6, 9, 12]
keys = ['動詞', '名詞', '形容詞', '副詞', '助動詞']

class Score:
	def __init__(self, channels):
		# Scores
		self.score_all = 0
		self.score_all_pn = 0
		self.channel_count = channels

		self.pndic = {}
		for key in keys:
			self.pndic[key] = []
		with open('resources/custom_pn_ja.txt') as f:
			for line in f:
				line = line.strip('/n')
				line = line.split(':')
				self.pndic[line[2]].append({'kanji': line[0], 'yomi': line[1], 'score': float(line[3])})
		with open('resources/pn_ja.txt') as f:
			for line in f:
				line = line.strip('/n')
				line = line.split(':')
				self.pndic[line[2]].append({'kanji': line[0], 'yomi': line[1], 'score': float(line[3])})

	def get_score_all(self):
		return self.score_all / self.channel_count

	# -1~1を0~1に調整
	def get_score_pn(self):
		return (self.score_all_pn / self.channel_count + 1) / 2

	def score_log(self, num, members):
		score = 0
		count = len(score_num_log) - 1

		for threshold in reversed(threshold_num_log):
			if num / members > threshold:
				score = score_num_log[count]
				break
			count -= 1

		self.score_all += score
		return score

	# lines: リスト（[0] = 単語, [1] = 品詞） emoji: 絵文字の数
	def score_pn(self, lines, emoji):
		score = 0
		for line in lines:
			if line[1] not in keys:
				continue
			score += self._score_pn_word(line[0], line[1])

		score += emoji
		score = score / (len(lines) + emoji)
		self.score_all_pn += score

		return score

	def _score_pn_word(self, word, part):
		dics = self.pndic[part]
		for dic in dics:
			if word == dic['kanji'] or word == dic['yomi']:
				return dic['score']
		return 0

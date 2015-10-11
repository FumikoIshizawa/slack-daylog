# -*- coding: utf-8 -*-

score_num_log = [0, 10, 20, 30, 40]
threshold_num_log = [0, 3, 6, 9, 12]
keys = ['動詞', '名詞', '形容詞', '副詞', '助動詞']

class Score:
	def __init__(self):
		self.pndic = {}
		for key in keys:
			self.pndic[key] = []
		with open('resources/pn_ja.txt') as f:
			for line in f:
				line = line.strip('/n')
				line = line.split(':')
				self.pndic[line[2]].append({'kanji': line[0], 'yomi': line[1], 'score': float(line[3])})

	# TODO: example
	def score_log(self, num, members):
		score = 0

		if num == threshold_num_log[0]:
			score = score_num_log[0]
		elif threshold_num_log[0] < num and num <= threshold_num_log[1]:
			score = score_num_log[1]
		elif threshold_num_log[1] < num and num <= threshold_num_log[2]:
			score = score_num_log[2]
		elif threshold_num_log[2] < num and num <= threshold_num_log[3]:
			score = score_num_log[3]
		elif threshold_num_log[3] < num and num <= threshold_num_log[4]:
			score = score_num_log[4]
		return score / members

	# lines: リスト（[0] = 単語, [1] = 品詞）　
	def calculate_pn_score(self, lines):
		score = 0
		for line in lines:
			if line[1] not in keys:
				continue
			score += self._score_pn_word(line[0], line[1])

		score = score / len(lines)
		return score

	def _score_pn_word(self, word, part):
		dics = self.pndic[part]
		for dic in dics:
			if word == dic['kanji'] or word == dic['yomi']:
				return dic['score']
		return 0

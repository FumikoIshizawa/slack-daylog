class Progress:
	score_num_log = [0, 5, 10, 15, 20]
	threshold_num_log = [0, 3, 6, 9, 12]

	def score_log(self, num):
		score = 0
		
		if num == self.threshold_num_log[0]:
			score = self.score_num_log[0]
		elif self.threshold_num_log[0] < num and num <= self.threshold_num_log[1]:
			score = self.score_num_log[1]
		elif self.threshold_num_log[1] < num and num <= self.threshold_num_log[2]:
			score = self.score_num_log[2]
		elif self.threshold_num_log[2] < num and num <= self.threshold_num_log[3]:
			score = self.score_num_log[3]
		elif self.threshold_num_log[3] < num and num <= self.threshold_num_log[4]:
			score = self.core_num_log[4]
		return score
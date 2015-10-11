# Python3

from datetime import datetime, timedelta
from mecabParse import MecabParse
from slack import Slack
from score import Score

now = datetime.now()
oldest_day=-3
duration_day=1
oldest = datetime(now.year, now.month, now.day, 0, 0, 0, 0) + timedelta(days=oldest_day)
latest = oldest + timedelta(days=duration_day)
score_all = 0

print(oldest, ' ~ ', latest)

# get all id
ids = Slack.get_channel_list()
sc = Score()

# 計算
list = []
word = ['優れる', '動詞']
list.append(word)
word = ['喜び', '名詞']
list.append(word)

score_pn = sc.calculate_pn_score(list)
print(score_pn)

for id in ids:
	log = Slack(oldest, latest, id)
	print('#', log.info['name'], '(', len(log.info['members']), 'members) -', len(log.logs), 'logs')
	print(log.logs)

	score = sc.score_log(len(log.logs), len(log.info['members']))
	print('score:', score, '\n')
	score_all += score

	p = MecabParse()
	for message in log.logs:
		p.parse(message)
	print(p.get_params())

print('Score: ', score_all)

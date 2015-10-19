# Python3

from datetime import datetime, timedelta
from mecabParse import MecabParse
from slack import Slack
from score import Score

# oledest_day日前から
oldest_day=-7

now = datetime.now()
duration_day=1
oldest = datetime(now.year, now.month, now.day, 0, 0, 0, 0) + timedelta(days=oldest_day)
latest = oldest + timedelta(days=duration_day)
score_all = 0
score_pn_all = 0

print(oldest, ' ~ ', latest)

# get all id
ids = Slack.get_channel_list()
sc = Score()

for id in ids:
	log = Slack(oldest, latest, id)
	print('#', log.info['name'], '(', len(log.info['members']), 'members) -', len(log.logs), 'logs')
	print(log.logs)

	score = sc.score_log(len(log.logs), len(log.info['members']))
	print('num-score:', score)
	score_all += score

	if len(log.logs) == 0:
		score_pn = 0
		print("np-score:", score_pn)
		print("\n")
		continue

	p = MecabParse()
	score_pn = 0
	for message in log.logs:
		line = p.parse_wordpart(message)
		score_pn += sc.calculate_pn_score(line)
	score_pn = score_pn / len(log.logs)
	score_pn_all += score_pn
	print("np-score:", score_pn)
	print(p.get_params())
	print("\n")

print('Score: ', score_all)
print('Score: ', score_pn_all / len(ids))
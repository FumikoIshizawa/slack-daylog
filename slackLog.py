# Python3

import os
from datetime import datetime, timedelta
from mecabParse import MecabParse
from slack import Slack
from progress import Progress

api_token = os.environ['SLACK_API_TOKEN']
now = datetime.now()
oldest_day=-1
duration_day=1
oldest = datetime(now.year, now.month, now.day, 0, 0, 0, 0) + timedelta(days=oldest_day)
latest = oldest + timedelta(days=duration_day)
score_all = 0

print(oldest, ' ~ ', latest)

# get all id
log = Slack(api_token, oldest, latest)
progress = Progress()
ids = log.get_channel_list()

# get history(logs) 
for id in ids:
	info = log.get_channel_info(id)
	history = log.get_history(id)
	print('#', info['name'], '(', len(info['members']), 'members) -', len(history), 'logs')
	print(history)
	score = progress.score_log(len(history))
	print('score:', score, '\n')
	score_all += score
	p = MecabParse()
	for message in history:
		p.parse(message)
	print(p.get_params())

print('Score: ', score_all)

# Python3

import os
from datetime import datetime, timedelta
from mecabParse import MecabParse
from slack import Slack

api_token = os.environ['SLACK_API_TOKEN']
now = datetime.now()
oldest_day=-1
duration_day=1
oldest = datetime(now.year, now.month, now.day, 0, 0, 0, 0) + timedelta(days=oldest_day)
latest = oldest + timedelta(days=duration_day)

print(oldest, ' ~ ', latest)

# get all id
log = Slack(api_token, oldest, latest)
ids = log.get_channel_list()

# get history(logs) 
for id in ids:
	print(id, ':')
	history = log.get_history(id)
	print(history, '\n\n')
	p = MecabParse()
	for message in history:
		p.parse(message)
	print(p.get_params())

# Python3

from datetime import datetime, timedelta
from mecabParse import MecabParse
from slack import Slack
from score import Score
import urllib

# oledest_day日前から
oldest_day = -1

now = datetime.now()
duration_day = 1
oldest = datetime(now.year, now.month, now.day, 0, 0, 0, 0) + timedelta(days=oldest_day)
latest = oldest + timedelta(days=duration_day)
score_all_np = 0

server_url = 'http://pom.l-u-l.tk/'
post_url = 'api/slack_score'

print(oldest, ' ~ ', latest)

# get all id
ids = Slack.get_channel_list()
sc = Score(len(ids))

for id in ids:
	log = Slack(oldest, latest, id)
	print('#', log.info['name'], '(', len(log.info['members']), 'members) -', len(log.logs), 'logs')
	print(log.logs)

	score = sc.score_log(len(log.logs), len(log.info['members']))
	print('num-score:', score)

	if len(log.logs) == 0:
		score_pn = 0
		print("np-score:", score_pn)
		print("\n")
		continue

	p = MecabParse()
	score_pn = 0
	line = []
	# channel毎にパースしてリスト化
	for message in log.logs:
		line += p.parse_wordpart(message)
	
	param = p.get_params()
	print(param)
	score_pn += sc.score_pn(line, param[2])
	print("score-pn: ", score_pn)
	print("\n")

print('Score: ', sc.get_score_all())
print('NP-Score: ', sc.get_score_pn());

url = server_url + post_url
params = {
	'date': datetime.now().strftime('%Y-%M-%d'),
	'project_id': 1,
	'value': sc.get_score_pn(),
}
try:
	encoded_params = urllib.parse.urlencode(params).encode(encoding='utf-8')
	urllib.request.urlopen(url=url, data=encoded_params)
	print('Data send: success')
except:
	print('Data send: error')

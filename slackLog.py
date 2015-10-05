# Python3

import urllib.parse
import urllib.request
import json
import os
import time
from datetime import datetime, timedelta
import mecabParse

api_token = os.environ['SLACK_API_TOKEN']
api_channel_url = "https://slack.com/api/channels.list"
api_history_url = "https://slack.com/api/channels.history"
now = datetime.now()
oldest_day=-1
duration_day=1
oldest = datetime(now.year, now.month, now.day, 0, 0, 0, 0) + timedelta(days=oldest_day)
latest = oldest + timedelta(days=duration_day)

def request_json_data(url, params):
	params = params.encode('utf-8')
	req = urllib.request.Request(url, params)
	response = urllib.request.urlopen(req).read()
	result = json.loads(response.decode('utf-8'))

	return result

def parse_channel_id(channels):
	ids = []
	for channel in channels:
		ids.append(channel['id'])

	return ids

def get_channel_list():
	params = urllib.parse.urlencode({
			'token': api_token,
		})
	channel_list = request_json_data(api_channel_url, params)
	ids = parse_channel_id(channel_list['channels'])

	return ids

def parse_history_text(messages):
	texts = []
	for message in messages:
		texts .append(message['text'])

	return texts

def get_history(id):
	oldest_ts = time.mktime(oldest.timetuple())
	latest_ts = time.mktime(latest.timetuple())
	params = urllib.parse.urlencode({
			'token': api_token,
			'channel': id,
			'oldest': oldest_ts,
			'latest': latest_ts,
		})
	history = request_json_data(api_history_url, params)
	logs = parse_history_text(history['messages'])

	return logs

# get all id
ids = get_channel_list()

# get history(logs) 
for id in ids:
	history = get_history(id)
	print(history, '\n\n')
	for message in history:
		mecabParse.parse(message)

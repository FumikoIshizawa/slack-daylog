import urllib.parse
import urllib.request
import json
import time
import os

api_channel_url = "https://slack.com/api/channels.list"
api_channel_info = "https://slack.com/api/channels.info"
api_history_url = "https://slack.com/api/channels.history"
api_token = os.environ['SLACK_API_TOKEN']

score_num_log = [0, 10, 20, 30, 40]
threshold_num_log = [0, 3, 6, 9, 12]

class Slack:
	def __init__(self, oldest, latest, id):
		self.oldest = oldest
		self.latest = latest
		self.info = self._get_channel_info(id)
		self.logs = self._get_history(id)

	@classmethod
	def get_channel_list(cls):
		params = urllib.parse.urlencode({
				'token': api_token,
			})
		params = params.encode('utf-8')
		req = urllib.request.Request(api_channel_url, params)
		response = urllib.request.urlopen(req).read()
		channels = json.loads(response.decode('utf-8'))

		ids = []
		for channel in channels['channels']:
			ids.append(channel['id'])

		return ids

	def get_channel_numlogs(id, self):
		info = get_channel_info(id)

		return len(info['members'])

	# TODO: example
	def score_log(self):
		score = 0
		num = len(self.logs)
		members = len(self.info['members'])

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

	def _get_channel_info(self, id):
		params = urllib.parse.urlencode({
				'token': api_token,
				'channel': id,
			})
		info = self._request_json_data(api_channel_info, params)
		
		return info['channel']

	def _get_history(self, id):
		oldest_ts = time.mktime(self.oldest.timetuple())
		latest_ts = time.mktime(self.latest.timetuple())
		params = urllib.parse.urlencode({
				'token': api_token,
				'channel': id,
				'oldest': oldest_ts,
				'latest': latest_ts,
			})
		history = self._request_json_data(api_history_url, params)
		logs = self._parse_history_text(history['messages'])

		return logs

	def _request_json_data(self, url, params):
		params = params.encode('utf-8')
		req = urllib.request.Request(url, params)
		response = urllib.request.urlopen(req).read()
		result = json.loads(response.decode('utf-8'))

		return result

	def _parse_history_text(self, messages):
		texts = []
		for message in messages:
			texts .append(message['text'])

		return texts

import urllib.parse
import urllib.request
import json
import time
import os

api_channel_url = "https://slack.com/api/channels.list"
api_channel_info = "https://slack.com/api/channels.info"
api_history_url = "https://slack.com/api/channels.history"
api_token = os.environ['SLACK_API_TOKEN']

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

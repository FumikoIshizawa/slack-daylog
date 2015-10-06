import urllib.parse
import urllib.request
import json
import time

class Slack:
	api_channel_url = "https://slack.com/api/channels.list"
	api_channel_info = "https://slack.com/api/channels.info"
	api_history_url = "https://slack.com/api/channels.history"

	def __init__(self, token, oldest, latest):
		self.token = token
		self.oldest = oldest
		self.latest = latest

	def get_channel_list(self):
		params = urllib.parse.urlencode({
				'token': self.token,
			})
		channel_list = self._request_json_data(self.api_channel_url, params)
		ids = self._parse_channel_id(channel_list['channels'])

		return ids

	def get_channel_info(self, id):
		params = urllib.parse.urlencode({
				'token': self.token,
				'channel': id,
			})
		info = self._request_json_data(self.api_channel_info, params)
		
		return info['channel']

	def get_channel_numlogs(id, self):
		info = get_channel_info(id)

		return len(info['members'])

	def get_history(self, id):
		oldest_ts = time.mktime(self.oldest.timetuple())
		latest_ts = time.mktime(self.latest.timetuple())
		params = urllib.parse.urlencode({
				'token': self.token,
				'channel': id,
				'oldest': oldest_ts,
				'latest': latest_ts,
			})
		history = self._request_json_data(self.api_history_url, params)
		logs = self._parse_history_text(history['messages'])

		return logs

	def _request_json_data(self, url, params):
		params = params.encode('utf-8')
		req = urllib.request.Request(url, params)
		response = urllib.request.urlopen(req).read()
		result = json.loads(response.decode('utf-8'))

		return result

	def _parse_channel_id(self, channels):
		ids = []
		for channel in channels:
			ids.append(channel['id'])

		return ids

	def _parse_history_text(self, messages):
		texts = []
		for message in messages:
			texts .append(message['text'])

		return texts

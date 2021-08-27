import json

class ResponseData(object):
	STATUS_OK = "ok"
	STATUS_FAIL = "fail"

	def __init__(self):
		self._status = ResponseData.STATUS_OK
		self._result = None
		self._message = None


	@property
	def status(self):
		return self._status

	@property
	def result(self):
		return self._result

	@property
	def message(self):
		return self._message
	
	@status.setter
	def status(self, newStatus):
		self._status = newStatus

	@result.setter
	def result(self, result):
		self._result = result

	@message.setter
	def message(self, message):
		self._message = message

	def toJSON(self):
		return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)

	def fromJSON(self, data):
		return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
	
	
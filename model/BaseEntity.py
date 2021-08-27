import json

class BaseEntity(object):
	def __init__(self, *args, **kwargs):
		self._createTime = kwargs['createTime']

		if 'id' in kwargs:
			self._id = kwargs['id']
		else:
			self._id = 0

	def toJSON(self):
		return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)

	@property
	def ID(self):
		return self._id

	@property
	def createTime(self):
		return self._createTime

	@ID.setter
	def ID(self, myid):
		self._id = myid

	@createTime.setter
	def createTime(self, createTime):
		self._createTime = createTime
	
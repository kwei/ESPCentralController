from model.BaseEntity import *
import sys

class EspData(BaseEntity):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if 'esp' in kwargs:
			self._esp = kwargs['esp']
		if 'measurements' in kwargs:
			self._measurements = kwargs['measurements']
		if 'createTime' in kwargs:
			self._createTime = kwargs['createTime']


	def generate(self, row):
		self._id = row[0]
		self._createTime = row[3]
		self._esp = row[1]
		self._measurements = row[2].split(",")

	@property
	def esp(self):
		return self._esp

	@property
	def measurements(self):
		return self._measurements


	def printStr(self):
		print('id=', self._id, ',esp=', self._esp, ',measurements=', self._measurements, ',createTime=', self._createTime)
	
	
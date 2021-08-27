import sqlite3
from flask import g
import sys
# from model.BaseEntity import *
# from model.espData import *

def getDB():
	db = getattr(g,  '_database', None)
	if db is None:
		db = g._database = SQliteBridge()
	return db

def closeDB():
	db = getattr(g,  '_database', None)
	if db is not None:
		db.close()


class SQliteBridge:
	def __init__(self):
		self.db = sqlite3.connect('esp-rssi-measurements-sqlite.db')

	def initDB(self, SQL):
		cursor = self.db.cursor()
		cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='rssi_measurements'")
		ret = cursor.fetchone()
		print("tables: ", ret)
		if not ret[0]:
			print("Table is not existed.")
			self.db.executescript(SQL)

	def close(self):
		self.db.close()
		pass


	def selectAllbyTableName(self, tableName):
		cursor = self.db.cursor()
		cursor.execute('select * from '+tableName+';')
		rows = cursor.fetchone()
		entities = []
		for row in rows:
			print(row)
			entity = espData()
			print('entity', entity)
			entity.generate(row)
			entities.append(entity)
		if len(entities) != 0:
			return entities
		else:
			return None

	def selectOnebyTableName(self, tableName, *args, **kwargs):
		cursor = self.db.cursor()
		queryString = "SELECT * FROM "+tableName
		if len(kwargs) > 0:
			queryString += 'WHERE'
			for index, (key, value) in enumerate(kwargs.items()):
				queryString += " " + key + "='" + str(value) + "'"
				if index != len(kwargs.items())-1:
					queryString += ' AND'


		queryString += ';'
		print("queryString: ", queryString)
		cursor.execute(queryString)
		self.db.commit()
		row = cursor.fetchone()
		if row != None:
			print("row: ", row)
			entity = espData()
			print('entity: ', entity)
			entity.generate(row)
			return entity
		else:
			return None

	def savebyTableName(self, tableName, obj):
		cursor = self.db.cursor()
		print(obj)
		objDict = obj.__dict__
		print("objDict: ", objDict)

		cursor.execute("SELECT * FROM "+tableName+";")
		lastID = len(cursor.fetchall())
		print("db rows: ", lastID)

		queryString = "INSERT INTO "+tableName+"("
		for index, (key, value) in enumerate(objDict.items()):
			key = key[1:]
			queryString += "" + key + ""
			if index == len(objDict.items())-1:
				queryString += ")"
			else:
				queryString += ","

		queryString += " values ("
		for index, (key, value) in enumerate(objDict.items()):
			print(value)
			if key == "_id":
				queryString += str(lastID+1)+","
				print("_id setting: ", queryString)
			else:
				if type(value) is int:
					queryString += str(value)
				if type(value) is bool:
					if value:
						queryString += "1"
					else:
						queryString += "0"
				if type(value) is str:
					queryString += "'" + value + "'"
				if type(value) is list:
					queryString += "'"+",".join(value)+"'"

				if index == len(objDict.items())-1:
					queryString += ")"
				else:
					queryString += ","
		queryString += ";"

		print("queryString: ", queryString)
		try:
			cursor.execute(queryString)
			self.db.commit()
			obj.ID=cursor.lastrowid
			return obj
		except sqlite3.Error as er:
			print('SQLite error: %s' % (' '.join(er.args)))
			print("Exception class is: ", er.__class__)
			print('SQLite traceback: ')
			exc_type, exc_value, exc_tb = sys.exc_info()
			import traceback
			print(traceback.format_exception(exc_type, exc_value, exc_tb))
			return None

	def deletebyTableName(self, tableName, *args, **kwargs):
		cursor = self.db.cursor()
		queryString += "DELETE FROM "+tableName
		if len(kwargs) > 0:
			queryString += "WHERE"
			for index, (key, value) in enumerate(kwargs.items()):
				queryString += " " + key + "='" + value + "'"
				if index == len(kwargs.items())-1:
					queryString += " AND"

		queryString += ";"

		print("queryString: ", queryString)
		try:
			cursor.execute(queryString)
			self.db.commit()
			return True
		except sqlite3.Error:
			return None

	def updatebyTableName(self, tableName, updateColumn, *args, **kwargs):
		cursor = self.db.cursor()
		queryString += "UPDATE " + tableName + " SET"
		for index, (key, value) in enumerate(updateColumn.items()):
			print(value)
			if type(value) is int:
				queryString += " " + key + "=" + str(value)
			if type(value) is bool:
				if value:
					queryString += " " + key + "=1"
				else:
					queryString += " " + key + "=0"
			if type(value) is str:
				queryString += " " + key + "='" + value + "'"
			if type(value) is list:
				queryString += " " + key + "='" + ",".join(value) + "'"
			if value is None:
				queryString += " " + key + "=" + "null" + ""

			if index == len(kwargs.items()):
				queryString += ","

		if len(kwargs) > 0:
			queryString += "WHERE"
			for index, (key, value) in enumerate(updateColumn.items()):
				print(value)
				if type(value) is int:
					queryString += " " + key + "=" + str(value)
				if type(value) is bool:
					if value:
						queryString += " " + key + "=1"
					else:
						queryString += " " + key + "=0"
				if type(value) is str:
					queryString += " " + key + "='" + value + "'"
				if value is None:
					queryString += " " + key + "=" + "null" + ""

				if index == len(kwargs.items()):
					queryString += " AND"

		queryString += ";"
		print("queryString: ", queryString)
		try:
			cursor.execute(queryString)
			self.db.commit()
			print(cursor.fetchall())
			return True
		except sqlite3.Error:
			return None
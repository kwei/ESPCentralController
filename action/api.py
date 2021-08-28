from flask import Flask, render_template, Blueprint, make_response, request
import requests, json
from datetime import datetime
from util.ResponseData import ResponseData
import random
import pickle
import json
import os
from ESPMonitor.monitor import MonitorService

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50)
session.mount('http://', adapter)

# http://0.0.0.0:5000/requestRSS/espHandle

api = Blueprint('api', __name__, url_prefix = "/")

ip_table = None
uploadFlag = False
with open('espConfig.json', newline='') as espConfig:
	configData = json.load(espConfig)
	ip_table = configData['espTable']
	uploadFlag = configData['uploadFlag']

print("\nip_table: ", json.dumps(ip_table, indent=4, sort_keys=True))
print("uploadFlag: ", uploadFlag, "\n")

monitorService = MonitorService()

def createResponse(data, status = 200):
	res = ResponseData()
	res.message = data
	res.status = ResponseData.STATUS_OK
	res = make_response(res.toJSON(), 200)
	res.mimetype = 'application/json'
	return res


def testingData(espName):
	data = ""
	for (ssid, ip) in ip_table.items():
		if espName != ssid:
			randRSS = 40 + 30*random.random()
			data += ssid + ":-"+str(int(randRSS))+"dBm,"
	data = data.split(",")
	data.remove("")
	return data


def dataPreprocess(data):
	data = data.text.split(",")
	while("" in data) : 
		data.remove("")
	scanResult = data.copy()
	for item in data:
		if item == "" or "ESP" not in item:
			scanResult.remove(item)
	return scanResult

@api.route('/getAlreadyESPFile', methods=['GET'])
def getAlreadyESPFile():
	return monitorService.getExist()

@api.route('/getOnline', methods=['GET'])
def getOnline():
	return monitorService.getOnline()

@api.route('/requestRSS/espHandle', methods=['GET'])
def espHandlePage():
	return render_template('espHandlePage.html')

@api.route('/monitor', methods=['GET'])
def espMonitorPage():
	return render_template('monitor.html')

@api.route('/requestUpload/id/<regex(".*"):deviceID>', methods=['GET'])
def uploadCode(deviceID = None):
	monitorService.setOnline(deviceID)
	print("\nUpload flag for device: ", deviceID, ", flag: ", uploadFlag, "\n")
	return uploadFlag 

@api.route('/requestRSS/id/<regex(".*"):deviceID>/TargetSSID/<regex(".*"):TargetID>/sendRSS', methods=['POST'])
def rss(deviceID = None, TargetID = None):
	print("\nDevice {} ---> {}.".format(deviceID, TargetID))

	espList = list (ip_table.keys())
	if espList.index(TargetID)+1 == len(espList):
		nextTargetID = espList[0]
	else:
		nextTargetID = espList[espList.index(TargetID)+1]

	isExist = True
	while(1):
		isExist = os.path.isfile('./rssMeasurements/esp{}/RSS_{}_to_{}.pkl'.format(int (deviceID.split("ESP")[1]), deviceID, nextTargetID))
		if isExist or deviceID == nextTargetID:
			monitorService.setExist(deviceID,nextTargetID,True)
			print('Exist: rssMeasurements/esp{}/RSS_{}_to_{}.pkl'.format(int (deviceID.split("ESP")[1]), deviceID, nextTargetID))
			if espList.index(nextTargetID)+1 >= len(espList):
				nextTargetID = espList[0]
				break
			else:
				nextTargetID = espList[espList.index(nextTargetID)+1]
		else:
			break


	if not deviceID == TargetID:
		data = request.data
		data = data.decode("utf-8")

		if not data == "":
			monitorService.setExist(deviceID,TargetID,True)
			rssList = data.split(",")[:-1]
			print("Data content: ", rssList)
			f = open("RSS_{}_to_{}.pkl".format(deviceID, TargetID), "wb")
			pickle.dump(rssList, f)
			f.close()
		else:
			monitorService.setExist(deviceID,TargetID,False)
			print("Data content: ", "Null")
	
	print("Next target device: ", nextTargetID, "\n")
	return nextTargetID





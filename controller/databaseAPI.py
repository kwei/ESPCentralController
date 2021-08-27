from flask import Flask, render_template, Blueprint, redirect, make_response, request, jsonify
from model.sqlite import SQliteBridge, getDB
from model.espData import *
from util.ResponseData import ResponseData
import json, ast
from types import SimpleNamespace


databaseAPI = Blueprint('databaseAPI', __name__, url_prefix = "/espMeasurements")


@databaseAPI.route('/', methods=['GET'], strict_slashes=False)
def getMeasurements():
	data = request.args
	db = getDB()
	espName = data.get('espName')
	espData = db.selectOnebyTableName('rssi_measurements', esp = espName)
	resData = ResponseData()
	if espData != None:
		resData.result=espData
		resData.status=ResponseData.STATUS_OK
		res = make_response(resData.toJSON(), 200)
	else:
		resData.status=ResponseData.STATUS_FAIL
		res = make_response(resData.toJSON(), 200)

	res.mimetype = 'application/json'
	return res


@databaseAPI.route('/', methods=['POST'], strict_slashes=False)
def newMeasurements():
	reqData = ast.literal_eval(request.data.decode("utf-8"))
	print(type(reqData), reqData)
	espData = EspData(**reqData)
	print(espData.printStr())
	db = getDB()
	espData = db.savebyTableName('rssi_measurements', espData)
	resData = ResponseData()
	if espData != None:
		resData.result=espData
		resData.status=ResponseData.STATUS_OK
		res = make_response(resData.toJSON(), 200)
	else:
		resData.status=ResponseData.STATUS_FAIL
		res = make_response(resData.toJSON(), 200)

	res.mimetype = 'application/json'
	return res

@databaseAPI.route('/', methods=['DELETE'], strict_slashes=False)
def deleteMeasurements():
	data = request.args
	db = getDB()
	espName = data.get('espName')
	isDeleted = db.deletebyTableName('rssi_measurements', esp = espName)
	resData = ResponseData()
	if isDeleted == True:
		resData.status=ResponseData.STATUS_OK
		res = make_response(resData.toJSON(), 200)
	else:
		resData.status=ResponseData.STATUS_FAIL
		res = make_response(resData.toJSON(), 200)

	res.mimetype = 'application/json'
	return res
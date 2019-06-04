# -*- coding:utf-8 -*-
import json
import logging
import logging.config

import configparser
import os

from klein import Klein
from twisted.internet.defer import inlineCallbacks, returnValue, maybeDeferred

from wallet import Wallet
from transaction import Transaction

def get_request_params(request):
	if request.method.decode('utf-8', 'strict') == 'GET':
		request_params = {key.decode('utf-8', 'strict'): value[0].decode('utf-8', 'strict') for key, value in request.args.items()}
	else:
		request_params = {key.decode('utf-8', 'strict'): value[0].decode('utf-8', 'strict') for key, value in request.args.items()}

	return request_params

# get parameter int value, if not exists, return default value
def get_param_int(request_params, key, default=1):
	value = default if key not in request_params.keys() else int(request_params[key])
	return value

# get parameter float value, if not exists, return default value
def get_param_float(request_params, key, default=1.0):
	value = default if key not in request_params.keys() else float(request_params[key])
	return value

# get parameter str value, if not exists, return default value
def get_param_str(request_params, key, default=2):
	value = default if key not in request_params.keys() else str(request_params[key])
	return value

# check param_value is valid, otherwise return the default one in options
def check_valid_option(param_value, options, default_idx=0):
	param_value = options[default_idx] if param_value not in options else param_value
	return param_value

# check key exist
def check_key_exist(request_params, keys, mode="dev"):
	key = keys.split(":")
	
	try:
		if len(key) == 1:
			request_params[key[0]] # try to access
		else:
			# transverse
			for k in key[:-1]:
				elem = request_params[k]
				
			elem[key[-1]] # try to access
			
	except:
		error_message = "Missing key"
		if mode == "dev":
			error_message += " - " + str(" >> ".join(key))
		return False, json.dumps({"error" : error_message})
	return True, None


class WebApp():
	app = Klein()
	
	def __init__(self):
		# get the config settings
		self.config = configparser.ConfigParser()
		curr_dir = os.path.dirname(__file__)
		config_file = os.path.join(curr_dir, "./config/config.ini")
		self.config.read(config_file)
		self.mode = self.config['status']['mode']

		#create instance
		self.wallet = Wallet()
		self.transaction = Transaction()
		

	@app.route("/", methods=['GET'])
	def hello(self, request):
		return "hello"

	# get balance from wallet
	@app.route("/api/wallet", methods=["GET"])
	@inlineCallbacks
	def get_balance(self, request):
		request_params =get_request_params(request)
		
		# check if compulsory key exist
		flag_exist, error_message_json = check_key_exist(request_params, "account", self.mode)
		if not flag_exist:
			request.setResponseCode(400)
			returnValue(error_message_json)	

		# get account
		account = get_param_str(request_params, "account", "") # 0x23945D32a86F89C456f77a5d0b91Ec238c00F1EA
		
		try:
			results = yield(self.wallet.get_balance(account))
		except:
			request.setResponseCode(500)
			returnValue(json.dumps({"error": "Something went wrong. Please try again later."}))
		
		if results == "error_conn_infura":
			request.setResponseCode(400)
			returnValue(json.dumps({"error": "Cannot connect Infura"}))	
		elif results == "error_in_account":
			request.setResponseCode(400)
			returnValue(json.dumps({"error": "Problem in accessing the account"}))	
		else:
			request.setResponseCode(200)
			returnValue(json.dumps(results))
	
		
	# create wallet in bulk
	@app.route("/api/wallet", methods=["POST"])
	@inlineCallbacks
	def create_wallet(self, request):
		request_params =get_request_params(request)
		
		num_of_wallet = get_param_int(request_params, "num_of_wallet", 1)
		
		try:
			results = yield(self.wallet.create_wallet(num_of_wallet))
		except:
			request.setResponseCode(500)
			returnValue(json.dumps({"error": "Something went wrong. Please try again later."}))
		
	
		request.setResponseCode(201)
		returnValue(json.dumps(results))
		
	# issue certiciate
	@app.route("/api/certificate", methods=["POST"])
	@inlineCallbacks
	def issue_certificate(self, request):
		request_params =get_request_params(request)

		# check if compulsory key exist
		flag_exist, error_message_json = check_key_exist(request_params, "to_addr", self.mode)
		if not flag_exist:
			request.setResponseCode(400)
			returnValue(error_message_json)	
		flag_exist, error_message_json = check_key_exist(request_params, "message", self.mode)
		if not flag_exist:
			request.setResponseCode(400)
			returnValue(error_message_json)	

		# get parameter value
		to_addr = get_param_str(request_params, "to_addr", None) # 0x1FB6b70FF9671fc0447D3e55205c702983Ad4787
		message = get_param_str(request_params, "message", None)
		print(to_addr, message)

		try:
			results = yield(self.transaction.send_transaction(to_addr, message))
		except:
			request.setResponseCode(500)
			returnValue(json.dumps({"error": "Something went wrong. Please try again later."}))
		
		if results == "error_conn_infura":
			request.setResponseCode(400)
			returnValue(json.dumps({"error": "Cannot connect Infura"}))	
		elif results == "error_in_transaction":
			request.setResponseCode(400)
			returnValue(json.dumps({"error": "Problem in sending transaction"}))	
		else:
			request.setResponseCode(200)
			returnValue(json.dumps(results))


	# check status
	@app.route("/api/transaction", methods=["GET"])
	@inlineCallbacks
	def check_status(self, request):
		request_params =get_request_params(request)

		# check if compulsory key exist
		flag_exist, error_message_json = check_key_exist(request_params, "tx_hash", self.mode)
		if not flag_exist:
			request.setResponseCode(400)
			returnValue(error_message_json)	

		# get parameter value
		tx_hash = get_param_str(request_params, "tx_hash", None)

		try:
			results = yield(self.transaction.check_status(tx_hash))
		except:
			request.setResponseCode(500)
			returnValue(json.dumps({"error": "Something went wrong. Please try again later."}))
		
		if results == "error_conn_infura":
			request.setResponseCode(400)
			returnValue(json.dumps({"error": "Cannot connect Infura"}))	
		else:
			request.setResponseCode(200)
			returnValue(json.dumps(results))
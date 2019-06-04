# -*- coding:utf-8 -*-
import os

import configparser

from web3 import Web3, HTTPProvider

from lib.mysql import Connection

class Transaction:
	def __init__(self):
		self.config = configparser.ConfigParser()
		curr_dir = os.path.dirname(__file__)
		config_file = os.path.join(curr_dir, "./config/config.ini")
		self.config.read(config_file)

		self.w3 = Web3(HTTPProvider(self.config["infura"]["url"] + self.config["infura"]["project_id"]))


	def send_transaction(self, to_addr, message='opencert hub in ropsten'):
		# check if it is fine to connect infura
		connected = self.w3.isConnected()
		print("connected: " + str(connected))

		if connected:
			# prepare the transaction
			try:
				signed_txn = self.w3.eth.account.signTransaction(
								dict(
									nonce = self.w3.eth.getTransactionCount(self.config["iks"]["main_acct"]),
									gasPrice = self.w3.eth.gasPrice,
									gas=100000,
									to=to_addr,
									data=Web3.toHex(text=message),
									value=Web3.toWei(0.001, 'ether')
								),
								self.config["iks"]["key"]
							)

				
			except Exception as e:
				print(str(e))
				return "error_in_transaction"

			# get the TxHash
			tx_hash_in_byte = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
			tx_hash = tx_hash_in_byte.hex()

			result = {}
			result["tx_hash"] = tx_hash
			return result
		else: # error in connecting infura
			return "error_conn_infura"

	def check_status(self, tx_hash):
		print("123")
		# check if it is fine to connect infura
		connected = self.w3.isConnected()
		print("connected: " + str(connected))
		
		if connected:
			# check transaction receipt
			receipt_return = self.w3.eth.getTransactionReceipt(tx_hash)

			if receipt_return is not None:
				result = {}
				result["status"] = "Done"
				return result
			else:
				result = {}
				result["status"] = "Processing"
				return result

		else: # error in connecting infura
			return "error_conn_infura"
		
		
		

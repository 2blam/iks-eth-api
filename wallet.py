# -*- coding:utf-8 -*-
import os

import configparser

from ecdsa import SigningKey, SECP256k1
import sha3

from lib.mysql import Connection

from web3 import Web3, HTTPProvider

class Wallet:
	def __init__(self):
		self.config = configparser.ConfigParser()
		curr_dir = os.path.dirname(__file__)
		config_file = os.path.join(curr_dir, "./config/config.ini")
		self.config.read(config_file)
		self.w3 = Web3(HTTPProvider(self.config["infura"]["url"] + self.config["infura"]["project_id"]))
		
	def checksum_encode(self, addr_str): # Takes a hex (string) address as input
	    keccak = sha3.keccak_256()
	    out = ''
	    addr = addr_str.lower().replace('0x', '')
	    keccak.update(addr.encode('ascii'))
	    hash_addr = keccak.hexdigest()
	    for i, c in enumerate(addr):
	        if int(hash_addr[i], 16) >= 8:
	            out += c.upper()
	        else:
	            out += c
	    return '0x' + out


	# get balance
	def get_balance(self, account):
		# check if it is fine to connect infura
		connected = self.w3.isConnected()
		print("connected: " + str(connected))

		if connected:
			# check the balance
			print("!!@#")
			try:
				balance = self.w3.eth.getBalance(account)
			except Exception as e:
				return "error_in_account"
			

			result = {}
			result["account"] = account
			result["balance_in_wei"] = balance
			result["balance_in_eth"] = balance * 0.000000000000000001
			return result
		else: # error in connecting infura
			return "error_conn_infura"

	# bulk generate a number of wallet
	def create_wallet(self, num_of_wallet=1):
		
		result = {}

		meta = {}
		meta["num_of_wallet"] = num_of_wallet

		wallets = []
		
		
		for i in range(num_of_wallet):
			# create the wallet information
			keccak = sha3.keccak_256()

			pri = SigningKey.generate(curve=SECP256k1)
			pub = pri.get_verifying_key().to_string()
			keccak.update(pub)
			address = keccak.hexdigest()[24:]

			pri_in_hex = pri.to_string().hex()
			pub_in_hex = pub.hex()
			acct_addr = self.checksum_encode(address)

			wallet_info = {}
			wallet_info["pri_key"] = pri_in_hex
			wallet_info["pub_key"] = pub_in_hex
			wallet_info["address"] = acct_addr

			wallets.append(wallet_info)



		result["wallet"] = wallets
		result["meta"] = meta
		return result
		

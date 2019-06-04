from web3 import Web3, HTTPProvider

from configparser import ConfigParser
import codecs

# load the config.yml file
config = ConfigParser()
config.read('./config/config.ini')

# PROJECT ID
w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/" + config["infura"]["project_id"]))

# check if the connection succeeded
connected = w3.isConnected()
print(connected)

if connected:
	# first - print the current balance in the account
	print(w3.eth.getBalance(config["iks"]["main_acct"]))
	
	# prepare the transaction
	signed_txn = w3.eth.account.signTransaction(
					dict(
						nonce=w3.eth.getTransactionCount(config["iks"]["main_acct"]),
						gasPrice = w3.eth.gasPrice,
						gas=100000,
						to='0x1FB6b70FF9671fc0447D3e55205c702983Ad4787',
						data=Web3.toHex(text='opencert hub in ropsten'),
						value=Web3.toWei(0.001, 'ether')
					),
					config["iks"]["key"]
		)

	# get the TxHash
	tx_hash_in_byte = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
	tx_hash = tx_hash_in_byte.hex()




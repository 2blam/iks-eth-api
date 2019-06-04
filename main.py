# -*- coding:utf-8 -*-
import sys
import logging
import logging.config
import os

from webapp import WebApp

if __name__ == '__main__':
	if len(sys.argv) > 1 :
		port = sys.argv[1]
		try:
			port = int(port)
		except ValueError:
			print ("commnad line argument, port, error")
	else:
		port = 8181

	curr_dir = os.path.dirname(__file__)
	logging_config_file = os.path.join(curr_dir, "./config/logging.ini")

	logging.config.fileConfig(logging_config_file)
	logger = logging.getLogger('root')


	# start Klein web app
	logger.info("start web engine with port: " + str(port))
	web_app = WebApp()
	web_app.app.run('0.0.0.0', port=port)

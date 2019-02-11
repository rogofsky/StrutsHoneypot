#!/usr/bin/env python

import os
import sys
import socket
import click
import datetime
import json
import base64


class hpflogger:
	def __init__(self, hpfserver, hpfport, hpfident, hpfsecret, hpfchannel, serverid):
		self.hpfserver = hpfserver
		self.hpfport = hpfport
		self.hpfident = hpfident
		self.hpfsecret = hpfsecret
		self.hpfchannel = hpfchannel
		self.serverid = serverid
		self.hpc = None
		if (self.hpfserver and self.hpfport and self.hpfident and self.hpfport and self.hpfchannel and self.serverid):
			import hpfeeds
			try:
				self.hpc = hpfeeds.new(self.hpfserver, self.hpfport, self.hpfident, self.hpfsecret)
				self.status = "Logging to hpfeeds using server: {0}, channel {1}.".format(self.hpfserver, self.hpfchannel)
			except (hpfeeds.FeedException, socket.error, hpfeeds.Disconnect):
				self.status = "hpfeeds connection not successful"
	def log(self, message):
		if self.hpc:
			message['serverid'] = self.serverid
			self.hpc.publish(self.hpfchannel, json.dumps(message))


if __name__ == '__main__':

	@click.command()
	@click.option('-m', '--msg')
	def start(msg):

		# hpfeeds options
		environreq = [
			'HPFEEDS_SERVER',
			'HPFEEDS_PORT',
			'HPFEEDS_IDENT',
			'HPFEEDS_SECRET',
			'HPFEEDS_CHANNEL',
			'SERVERID',
			]
		if all(var in os.environ for var in environreq):
			hpfserver = os.environ.get('HPFEEDS_SERVER')
			hpfport = os.environ.get('HPFEEDS_PORT')
			hpfident = os.environ.get('HPFEEDS_IDENT')
			hpfsecret = os.environ.get('HPFEEDS_SECRET')
			hpfchannel = os.environ.get('HPFEEDS_CHANNEL')
			serverid = os.environ.get('SERVERID')

			hpfl = hpflogger(hpfserver, hpfport, hpfident, hpfsecret, hpfchannel, serverid)

			# submit log
			hpfl.log(json.loads(base64.b64decode(msg)))

			sys.stdout.write(hpfl.status + "\n")
			sys.stdout.flush()
			sys.exit(0)

	start()

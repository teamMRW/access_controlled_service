#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import sys
import requests
import json
from flask import Flask, request, redirect, url_for, abort, jsonify
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from requests_oauthlib import OAuth1Session
from datetime import datetime as dt

app = Flask(__name__)
api = Api(app)

class Response(Resource):
	def get(self):
		return "Server Connected"

class Tweet(Resource):
	def post(self):
		if request.headers['Content-Type'] == 'application/json':
			self.message = request.json['message']
			self.tweet()
		return self.message

	def tweet(self):
		consumer_key = " "
		consumer_secret = " "
		access_token = " "
		access_secret = " "

		twitter = OAuth1Session(consumer_key,consumer_secret,access_token,access_secret)

		now = dt.now().strftime('%m/%d %H:%M:%S')
		params = {"status": self.message + "\n\n" + now}
		req = twitter.post("https://api.twitter.com/1.1/statuses/update.json",params = params)

class Line(Resource):
	def post(self):
		if request.headers['Content-Type'] == 'application/json':
			self.message = request.json['message']
			self.lineNotify()
		return self.message

	def lineNotify(self):
		s = requests.session()
		url = "https://notify-api.line.me/api/notify"

		data = {
			"message": self.message,
		}
		headers = {'Authorization': 'Bearer '+'[PUT LINE TOKEN]'}
		r = s.post(url, data=data, headers=headers)
		text = r.text
		text = json.loads(text)
		print(text)

class Slack(Resource):
	def post(self):
		if request.headers['Content-Type'] == 'application/json':
			self.message = request.json['message']
			self.slack()
		return self.message

	def slack(self):
		now = dt.now().strftime('%m/%d %H:%M:%S')
		data = {
			"text": self.message + "\n\n" + now,
			"username":'bot_desuyo',
			"icon_emoji":"grin",
			"channel":'#bot_room',
			}
		url = " "
		req = requests.post(url, data=json.dumps(data))


api.add_resource(Response, '/')
api.add_resource(Tweet, '/api/tweet')
api.add_resource(Line, '/api/line')
api.add_resource(Slack, '/api/slack')

if __name__ == '__main__':
	ip = socket.gethostbyname(socket.gethostname())
	app.debug=True
	app.run(host=ip)

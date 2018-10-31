#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi;
import cgitb;cgitb.enable()
import urllib, urllib2
import os
import json

print "Content-Type: text/html; charset=utf-8\n\n";

tgToken = "" # Telegram bot token 
sphKey = "" # Google spreadsheet key (example: https://i.imgur.com/TX4gKmT.png)
apiUrl = "https://api.telegram.org/bot{}/".format(token)
chatID = 162034153 # Your chat it, to limit other peoples from using your bot :3

def getGoogleData():
	# Example: https://goo.gl/G1KEF3
	url = "https://spreadsheets.google.com/feeds/cells/{}/od6/public/values?alt=json&min-row=2&max-row=8&min-col=7&max-col=7".format(shKey)

	req = urllib2.Request(url)
	response = urllib2.urlopen(req)

	data = json.loads(response.read())

	btc = float(data["feed"]["entry"][0]["content"]["$t"].replace(',', '.'))
	krb =  float(data["feed"]["entry"][1]["content"]["$t"].replace(',', '.'))
	xem = float(data["feed"]["entry"][2]["content"]["$t"].replace(',', '.'))
	bch = float(data["feed"]["entry"][3]["content"]["$t"].replace(',', '.'))
	eth = float(data["feed"]["entry"][4]["content"]["$t"].replace(',', '.'))
	uah = float(data["feed"]["entry"][5]["content"]["$t"].replace(',', '.'))

	return {'btc': btc, 'krb': krb, 'xem': xem, 'bch': bch, 'eth': eth, 'uah': uah}

def getPrice(currency):
	url = "https://www.cryptopia.co.nz/api/GetMarket/{}_BTC".format(currency)

	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	data = json.loads(response.read())

	return float(data["Data"]["AskPrice"])

def getUsd():
	url = "http://preev.com/pulse/units:btc+usd/sources:bitstamp"

	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	data = json.loads(response.read())

	return float(data["btc"]["usd"]["bitstamp"]["last"])

def tSendMessage(user, message):
	url = apiUrl + 'sendMessage'
	values = {'chat_id' : user,
			  'text' : message,
			  'parse_mode' : "html",
			  'reply_markup' : '{"keyboard":[[{"text":"/stats"}]], "resize_keyboard": true}'
 			 }

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)

	response = urllib2.urlopen(req)

	return

def tSendImage(user, photo='http://i.imgur.com/LiEajw2.png', caption='', button='{}'):
	url = apiUrl + 'sendPhoto'

	values = {'chat_id' : user,
			  'photo' : photo,
			  'reply_markup' : button,
			  'caption' : caption
			 }

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)

	response = urllib2.urlopen(req)

	return

if "CONTENT_TYPE" in os.environ:

	telegramData = json.loads(cgi.FieldStorage().value)
	userID = telegramData["message"]["chat"]["id"]
	text = telegramData["message"]["text"]

	if userID == chatID:
		cryptoData = getGoogleData()
		priceBtc = round((cryptoData["btc"] * getUsd()), 2)
		priceKrb = round((getPrice("krb") * cryptoData["krb"] * getUsd()), 2)
		priceXem = round((getPrice("xem") * cryptoData["xem"] * getUsd()), 2)
		priceEth = round((getPrice("eth") * cryptoData["eth"] * getUsd()), 2)
		priceTotal = priceBtc + priceKrb + priceXem + priceEth
		priceUah = cryptoData["uah"]

		if text == "/stats":
			message = """<b>Status:</b>\n BTC: {} 	({} <b>$</b>)\n KRB: {} 	({} <b>$</b>)\n XEM: {} 	({} <b>$</b>)\n ETH: {} 	({} <b>$</b>)\n<b>Total:</b>\n USD: {}\n UAH: {}
			""".format(
					cryptoData["btc"], 
					priceBtc,
					cryptoData["krb"],
					priceKrb,
					cryptoData["xem"],
					priceXem,
					cryptoData["eth"],
					priceEth,
					priceTotal,
					(priceTotal * priceUah)
				)
			tSendMessage(userID, message)
		else:
			tSendMessage(userID, "Wut?" )

	else:
		tSendImage(user = userID, caption = 'Nice try, but nope :3')

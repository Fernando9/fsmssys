from flask import Flask, request, abort, Response
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
from flask_cors import CORS, cross_origin
import json
import os
import configparser

config = configparser.ConfigParser()
config.read('twiexample.config')
account_sid = config['DEFAULT']['account_sid']
auth_token = config['DEFAULT']['auth_token']
from_ = config['DEFAULT']['from_']

app = Flask(__name__)
CORS(app)

@app.route('/')
def api_route():
    data = {
        'Status':'Server is Running'
    }
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/sms', methods=['POST'])
def send_message():
    data = request.get_json()
    if not request.json:
        abort(400)
    data = request.get_json()
    to = data["to"]
    body = data["body"]
    client = TwilioRestClient(account_sid, auth_token)
    try:
        message_response = client.messages.create(to=to, from_=from_, body=body)
        reply_dict = {}
        reply_dict['msg_type'] = 'Message Sent'
        reply_dict['account_sid'] = message_response.sid
        reply_dict['date_sent'] = str(message_response.date_created)
        reply_dict['status'] = 'Success'
        js = json.dumps(reply_dict)
        resp = Response(js, status=200, mimetype='application/json')
    except TwilioRestException as e:
        jse = json.dumps(e.msg)
        resp = Response(jse, status=404, mimetype='application/json')
    return resp


@app.route('/response', methods=['GET'])
def reply_message():
    resp = twilio.twiml.Response()
    resp.message("Hello There!!!!")
    return str(resp)

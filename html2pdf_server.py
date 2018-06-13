#!/usr/bin/python

import os, tempfile, subprocess

import flask
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, fields, marshal
import werkzeug
from werkzeug import secure_filename

app = Flask(__name__, static_url_path="")
api = Api(app)

WKHTML2PDF_PATH = '/home/hossein/work/wkhtmltox/bin/wkhtmltopdf'

class MyAPIRes(Resource):
	@classmethod
	def get(cls):
		f=open('page.pdf')
		response = flask.make_response(f.read())
		response.headers['content-type'] = 'application/octet-stream'
		return response

api.add_resource(MyAPIRes, '/html2pdf/test.pdf')

class HTML2PDF(Resource):
	def get(self):
		pass

	def put(self):
		pass
	
	def post(self):
		parse = reqparse.RequestParser()
		parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
		args = parse.parse_args()
		f = args['file']
		if f:
			t_input = tempfile.mktemp()+'.html'
			print '++++++IN: '+t_input
			t_output = 'tmp/out.pdf'
			os.remove(t_output)  ###### remove this line later
			print '++++++OUT: '+t_output
			
			f.save(t_input)
			try:
				subprocess.check_call( [ WKHTML2PDF_PATH, 'page', t_input, t_output ] )
			except:
				pass
				#correct this later
			os.remove(t_input)
			try:
				of = open(t_output)
			except:
				return jsonify (['Error occured'])
			response = flask.make_response(of.read())
			response.headers['content-type'] = 'application/octet-stream'
			of.close()
			os.remove(t_output)
			return response
		else:
			return jsonify(['False'])

api.add_resource(HTML2PDF, '/html2pdf/convert', endpoint='convert')

@app.route('/test')
def test():
	print request.method
	return jsonify(['False'])

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

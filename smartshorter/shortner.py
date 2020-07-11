from flask import Blueprint, render_template, jsonify, request
from werkzeug.exceptions import NotFound
from pymongo import MongoClient
from mongoframes import *
from .models import *
from .utils import *



# Create a blueprint object to be registered in run.py
shortner = Blueprint('shortner', __name__)


# Connect MongoFrames to the database
Frame._client = MongoClient('mongodb+srv://m_gamal:polar147@task.npwty.azure.mongodb.net/task?retryWrites=true&w=majority')


@shortner.route('/')
def index():
	return render_template('shortner.html')

@shortner.route('/shortlinks', methods=['GET'])
def list_shortlinks():

	shortlinks = [
		{
			"slug": obj.slug,
			"ios": obj.ios,
			"android": obj.android,
			"web": obj.web
		} 
		for obj in ShortLink.many()
	]

	return jsonify({'shortlinks': shortlinks})

@shortner.route('/shortlinks', methods=['POST'])
def create_shortlink():
	data = request.get_json()

	slug = data.get('slug')

	if not slug:
		slug = make_slug()
	else:
		slug_exists = ShortLink.one(Q.slug == slug)
		if slug_exists:
			slug = make_slug()
	
	shortlink = ShortLink(
		slug=slug,
		web=data.get('web')
	)
	shortlink.ios = {
		'primary': data['ios'].get('primary'),
		'fallback': data['ios'].get('fallback'),
	}
	shortlink.android = {
		'primary': data['android'].get('primary'),
		'fallback': data['android'].get('fallback'),
	}
	shortlink.insert()

	return jsonify({
		"status": "successful",
		"slug": slug,
		"message": "created successfully"
	}), 201

@shortner.route('/shortlinks/<string:slug>', methods=['PUT'])
def update_shortlink(slug):

	shortlink = ShortLink.one(Q.slug == slug)
	if not shortlink:
		# This returns the default Flask html/text 404 error page, not the one defined in errors.py
		# return NotFound()
		
		return jsonify({"status": "failed", "message": "not found"}), 404

	data = request.get_json()
	# Updating the shortlink data
	shortlink.web = data.get('web', shortlink.web)
	if data.get('ios'):
		for attr in data.get('ios'):
			shortlink.ios[attr] = data['ios'].get(attr, shortlink.ios[attr])
	if data.get('android'):
		for attr in data.get('android'):
			shortlink.android[attr] = data['android'].get(attr, shortlink.android[attr])
	shortlink.update()

	return jsonify({
		"status": "successful",
		"message": "updated successfully"
	}), 201

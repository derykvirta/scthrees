import os
from flask import render_template
from flask import send_from_directory
from rest_service import app

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/static/css/<path:filename>')
def serve_css(filename):
  return send_from_directory(os.path.join(os.getcwd(), 'static', 'css'), filename)

@app.route('/static/js/<path:filename>')
def serve_js(filename):
  return send_from_directory(os.path.join(os.getcwd(), 'static', 'js'), filename)

@app.route('/static/img/<path:filename>')
def serve_img(filename):
  return send_from_directory(os.path.join(os.getcwd(), 'static', 'img'), filename)
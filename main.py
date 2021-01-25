import datetime
import uuid
import json

from flask import Flask, render_template, request, jsonify
from google.cloud import datastore


app = Flask(__name__)

@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times)

@app.route('/new', methods=['POST'])
def new():
    data = request.json

    client = datastore.Client()
    key = client.key("Object", data['key'])
    ent = datastore.Entity(key)
    ent['location'] = data['location']
    ent['channel'] = data['channel']
    ent['position'] = data['position']
    ent['rotation'] = data['rotation']
    ent['scale'] = data['scale']
    ent['url'] = data['url']
    client.put(ent)
    return 'Success'

@app.route('/update', methods=['POST'])
def update():
    data = request.json

    client = datastore.Client()
    key = client.key("Object", data['key'])
    ent = client.get(key)
    ent['location'] = data['location']
    ent['channel'] = data['channel']
    ent['position'] = data['position']
    ent['rotation'] = data['rotation']
    ent['scale'] = data['scale']
    ent['url'] = data['url']
    client.put(ent)
    return 'Success'

@app.route('/lists', methods=['GET'])
def lists():
    location = request.args.get('location')
    channel = request.args.get('channel')

    client = datastore.Client()
    query = client.query(kind="Object")
    query.add_filter("location", "=", location)
    query.add_filter("channel", "=", channel)
    
    resultlist = list(query.fetch())

    results = {}
    for result in resultlist:
        result["key"] = result.key.name
        results[result.key.name] = result

    return jsonify(results)

@app.route('/delete', methods=['GET'])
def delete():
    client = datastore.Client()
    key = client.key("Object", request.args.get('key'))
    client.delete(key)
    return 'Success'

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

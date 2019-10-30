import os
import redis
import flask
import json
import config
import pymongo
from flask import Flask, Response, request, render_template, abort
from flask_caching import Cache
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# enabling caching
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

app.config['CORS_HEADERS'] = 'Content-Type'
redis_handle = redis.Redis('localhost')
mongo_client = pymongo.MongoClient('127.0.0.1:27017/')
mongo_db_handle = mongo_client['instances']
mongo_handle = mongo_db_handle['instances']
requiredFields = ("id", "itype","details")  # fields required for user object


@app.route('/')
@cross_origin()
@cache.cached(timeout=500)
def hello():
    return 'Hello World!'


@app.route('/itype/<itype_id>', methods=['GET'])
@cross_origin()
@cache.cached(timeout=500)
def get_user(itype_id):
    response = {}
    # user_id = request.args.get("id")
    user = redis_handle.get(user_id)
    if not user:
        response["msg"] = "no user found"
        return Response(json.dumps(response), status=404, mimetype="application/json")
    return user


@app.route('/itype', methods=['POST'])
@cross_origin()
def save_user():
    data = request.get_json(force=True)
    response = {}
    if all(field in data for field in requiredFields):
        _id = mongo_handle.insert(data)
        # redis_handle.set(data["id"], json.dumps(data))
        return Response(status=201)
    else:
        missing_key = str([val for val in requiredFields if val not in dict(data).keys()])
        response["msg"] = "required key " + missing_key + " not found"
        return Response(json.dumps(response), status=400)


@app.route('/users/<user_id>', methods=['DELETE'])
@cross_origin()
def delete_user(user_id):
    response = {}
    resp = redis_handle.delete(user_id)
    if resp == 0:
        response["msg"] = "no such entity found"
        status = 404
    else:
        response["msg"] = "Delete op is successful"
        status = 200
    return Response(json.dumps(response), status=status)


@app.route('/clear', methods=['GET'])
@cross_origin()
def clear_data():
    redis_handle.flushall()
    return "ok!"


if __name__ == "__main__":
    app.run(debug=True)
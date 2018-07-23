"""Contains all endpoints to manipulate diary information
"""
import datetime
from flask import jsonify, Blueprint, make_response
from flask_restful import Resource, Api, reqparse, inputs
import os

from werkzeug.security import check_password_hash
import jwt

import config
import models 
from .auth import admin_required

class DiaryList(Resource):
    """Contains GET and POST methods"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'diary_no',
            required=True,
            type=int,
            help='kindly provide a diary number',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'to-do',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a valid to-do)',
            location=['form', 'json'])
        super().__init__()

    def post(self):
        """Adds a new diary"""
        args = self.reqparse.parse_args()
        for diary_id in models.all_diaries:
            if models.all_diaries.get(diary_id)["diary_no"] == args.get('diary_no'):
                return jsonify({"message" : "diary with that number already exists"})
        
        result = models.Diary.create_diary(diary_no=args['diary_no'], todo=args['to-do'])
        return make_response(jsonify(result), 201)

    def get(self):
        """Gets all diary nos."""
        return make_response(jsonify(models.all_diaries), 200)


class Diary(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single diary"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'diary_no',
            required=True,
            type=int,
            help='kindly provide a diary no.',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'to-do',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a valid to-do)',
            location=['form', 'json'])
        super().__init__()

    def get(self, diary_id):
        """Get a particular diary"""
        try:
            diary = models.all_diaries[diary_id]
            return make_response(jsonify(diary), 200)
        except KeyError:
            return make_response(jsonify({"message" : "diary no. does not exist"}), 404)

    def put(self, diary_id):
        """Update a particular diary"""
        kwargs = self.reqparse.parse_args()
        result = models.Diary.update_diary(diary_id, **kwargs)
        if result != {"message" : "diary no. does not exist"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)

    def delete(self, diary_id):
        """Delete a particular diary"""
        result = models.Diary.delete_diary(diary_id)
        if result != {"message" : "diary no. does not exist"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)


diaries_api = Blueprint('resources.diaries', __name__)
api = Api(diaries_api) # create the API
api.add_resource(DiaryList, '/diaries', endpoint='diaries')
api.add_resource(Diary, '/diaries/<int:diary_id>', endpoint='diary')




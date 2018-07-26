"""Handles data storage for Users and Entries
"""
# pylint: disable=E1101

import datetime

from flask import make_response, jsonify
from werkzeug.security import generate_password_hash
import psycopg2


import config
from os import getenv

db = config.TestingConfig.db

class User(object):

    @staticmethod
    def create_user(username, email, password, admin=False, **kwargs):
        """Creates a new user and ensures that the email is unique"""
        db_connection = psycopg2.connect(db)
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users")
        users = db_cursor.fetchall()
        for user in users:
            if user[1] == email:
                return make_response(jsonify({"message" : "user with that email already exists"}), 400)

        password = generate_password_hash(password, method='sha256')
        new_user = "INSERT INTO users (username, email, password) VALUES " \
                    "('" + username + "', '" + email + "', '" + password + "')"
        db_cursor.execute(new_user)
        db_connection.commit()
        db_connection.close()
        return make_response(jsonify({"message" : "user has been successfully created"}), 201)
                                    

    @staticmethod
    def update_user(user_id, username, email, password, admin=False, **kwargs):
        db_connection = psycopg2.connect(db)
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users")
        users = db_cursor.fetchall()
        for user in users:
            if user[1] == email:
                return make_response(jsonify({"message" : "user with that email already exists"}), 400)

        for user in users:
            if user[0] == user_id:
                db_cursor.execute("UPDATE users SET username=%s, email=%s, password=%s WHERE user_id=%s",
                                  (username, email, password, user_id))
                return make_response(jsonify({"message" : "user has been successfully updated"}), 200)

        return make_response(jsonify({"message" : "user does not exist"}), 404)


    @staticmethod
    def delete_user(user_id):
        """Deletes a user"""
        db_connection = psycopg2.connect(db)
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users")
        users = db_cursor.fetchall()
        if users != []:
            for user in users:
                if user[0] == user_id:
                    db_cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
                    db_connection.commit()
                    db_connection.close()
                    return make_response(jsonify({"message" : "user has been successfully deleted"}), 200)
        
        return make_response(jsonify({"message" : "user does not exists"}), 404)

    @staticmethod
    def get_user(user_id):
        """Gets a particular user"""
        db_connection = psycopg2.connect(db)
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        user = db_cursor.fetchall()
        if user != []:
            user=user[0]
            info = {user[0] : {"email": user[1],
                                "username": user[2],
                                "entries": user[4],
                               }}
            return make_response(jsonify({"profile" : info}), 200)
        return make_response(jsonify({"message" : "user does not exists"}), 404)


    @staticmethod
    def get_all_users():
        """Gets all users"""
        db_connection = psycopg2.connect(db)
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM users")
        users = db_cursor.fetchall()
        all_users = []
        for user in users:
            info = {user[0] : {"email": user[1],
                                "username": user[2],
                                "entries": user[4],
                             }}
            all_users.append(info)
        return make_response(jsonify({"All users" : all_users}), 200)

class Entries(object):
    """Contains entry columns and methods to add, update and delete an entry"""


    @staticmethod
    def create_entry(ride, driver_id, departuretime, cost, maximum, status="pending"):
        """Creates a new entry"""
        db_connection = psycopg2.connect(db)
        db_cursor = db_connection.cursor()
        new_ride = "INSERT INTO entries (entry, user_id) VALUES" \
                    "('" + entry + "', '" + user_id + "')"
        db_cursor.execute(new_entry)
        db_connection.commit()
        db_connection.close()
        return make_response(jsonify({"message" : "entry has been successfully created"}), 201)


    @staticmethod
    def update_entry(entry_id, entry, user_id):
        """Updates entry information"""
        db_connection = psycopg2.connect(db)
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM entries")
        rides = db_cursor.fetchall()
        for entry in entries:
            if entry[0] == entry_id:
                db_cursor.execute("UPDATE entries SET entry=%s, user_id=%s WHERE entry_id=%s",
                                  (entry, user_id, entry_id))
                return make_response(jsonify({"message" : "entry has been successfully updated"}), 200)
        return make_response(jsonify({"message" : "entry does not exist"}), 404)


    @staticmethod
    def start_entry(entry_id, user_id):
        db_connection = psycopg2.connect(db)
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM entries WHERE entry_id=%s", (entry_id,))
        ride = db_cursor.fetchall()
        if entry != []:
            entry = entry[0]
            if int(entry[2]) == user_id:
                db_cursor.execute("UPDATE entries SET status=%s WHERE entry_id=%s", ("given", entry_id))
                db_connection.commit()
                db_connection.close()
                return {"message" : "entry has started"}

            return {"message" : "The entry you want to start is not yours."}

        return {"message" : "entry does not exist"}

    @staticmethod
    def delete_entry(entry_id):
        db_connection = psycopg2.connect(db)
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM entries")
        rides = db_cursor.fetchall()
        for entry in entries:
            if entry[0] == entry_id:
                db_cursor.execute("DELETE FROM entries WHERE entry_id=%s", (entry_id,))
                db_connection.commit()
                db_connection.close()
                return make_response(jsonify({"message" : "entry has been successfully deleted"}), 200)
        return make_response(jsonify({"message" : "user does not exists"}), 404)


    @staticmethod
    def get_entry(entry_id):
        db_connection = psycopg2.connect(db)
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM entries WHERE entry_id=%s", (entry_id,))
        entry = db_cursor.fetchall()
        if entry != []:
            entry=entry[0]
            info = {entry[0] : {"entry": entry[1],
                                "user_id": entry[2],}}
            return make_response(jsonify({"entry" : info}), 200)
        return make_response(jsonify({"message" : "entry does not exists"}), 404)
        
    
    @staticmethod
    def get_all_entries():
        db_connection = psycopg2.connect(db)
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM entries")
        entries = db_cursor.fetchall()
        all_entries = []
        for entry in entries:
            info = {entry[0] : {"entry": entry[1],
                                "user_id": entry[2],}}
            all_entries.append(info)
        return make_response(jsonify({"All entries" : all_entries}), 200)


def tables_creation():
    tables = ("""CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, email VARCHAR(150) NOT NULL UNIQUE,
                                                   username VARCHAR(100) NOT NULL, password VARCHAR(450) NOT NULL)""",
              """ CREATE TABLE IF NOT EXISTS entries (entry_id SERIAL PRIMARY KEY, entry VARCHAR(155) NOT NULL,
                                                    user_id INTEGER(50) NOT NULL, to-do VARCHAR(100) NOT NULL,
                                                    date VARCHAR(100) NOT NULL)"""
            

    conn = psycopg2.connect(db)
    cur = conn.cursor()
    for table in tables:
        cur.execute(table)
    cur.close()
    conn.commit()
    try:
        User.create_user(username="admin", email="admin@gmail.com", password="admin1234")
    except:
        pass
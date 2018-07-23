"""Handles data storage for Users and Diaries
"""

all_users = {}
user_count = 1

all_diaries = {}
diary_count = 1


class User(object):
    """Contains methods to add, update and delete a user"""


    @staticmethod
    def create_user(username, email, password, admin=False, **kwargs):
        """Creates a new user and appends his information to the all_users dictionary"""
        global all_users
        global user_count
        all_users[user_count] = {"id": user_count, "username" : username,
                                 "email" : email, "password" : password, "admin" : admin}
        new_user = all_users[user_count]
        user_count += 1
        return new_user

    @staticmethod
    def update_user(user_id, username, email, password, admin=False, **kwargs):
        """Updates user information"""
        if user_id in all_users.keys():
            all_users[user_id] = {"id" : user_id, "username" : username, "email" : email,
                                  "password" : password, "admin" : admin}
            return all_users[user_id]
        return {"message" : "user does not exist"}

    @staticmethod
    def delete_user(user_id):
        """Deletes a user"""
        try:
            del all_users[user_id]
            return {"message" : "user successfully deleted"}
        except KeyError:
            return {"message" : "user does not exist"}


class Diary(object):
    """Contains methods to add, update and delete a diary"""


    @staticmethod
    def create_diary(diary_no, todo):
        """Creates a new diary_no and appends this information to the all_diaries dictionary"""
        global all_diaries
        global diary_count
        all_diaries[diary_count] = {"id": diary_count, "diary_no" : diary_no, "to-do": todo}
        new_diary = all_diaries[diary_count]
        diary_count += 1
        return new_diary

    @staticmethod
    def update_diary(diary_id, diary_no, todo, **kwargs):
        """Updates diary no's information"""
        if diary_id in all_diaries.keys():
            all_diaries[diary_id] = {"id": diary_id, "diary_no" : diary_no, "to-do" : todo}
            return all_diaries[diary_id]
        return {"message" : "diary_no does not exist"}

    @staticmethod
    def delete_diary(diary_id):
        """Deletes a diary"""
        try:
            del all_diaries[diary_id]
            return {"message" : "diary number successfully deleted"}
        except KeyError:
            return {"message" : "diary number does not exist"}






"""Handles data storage for Users and Diaries
"""

all_users = {}
user_count = 1

all_entries = {}
entry_count = 1


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


class Entry(object):
    """Contains methods to add, update and delete an entry"""


    @staticmethod
    def create_entry(user_id, todo):
        """Creates a new date and appends this information to the all_entries dictionary"""
        global all_entries
        global entry_count
        all_entries[entry_count] = {"id": entry_count, "to-do": todo}
        new_entry = all_entries[entry_count]
        entry_count += 1
        return new_entry

    @staticmethod
    def update_entry(email, date, todo, **kwargs):
        """Updates entries' dates information"""
        if email in all_entries.keys():
            all_entries[email] = {"user_idl": user_id, "date" : date, "to-do" : todo}
            return all_entries[user_id]
        return {"message" : "id with that entry does not exist"}

    @staticmethod
    def delete_entry(user_id):
        """Deletes an entry"""
        try:
            del all_entries[user_id]
            return {"message" : "entry with that id is successfully deleted"}
        except KeyError:
            return {"message" : "entry with that id does not exist"}






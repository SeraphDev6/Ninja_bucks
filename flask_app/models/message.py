from flask_app.models.sensei import Sensei
from flask_app.config.mysqlconnection import connectToMySQL
class Message:
    def __init__(self,data):
        self.id = data['id']
        self.ninja_buck_change = data['ninja_buck_change']
        self.message_text = data['message_text']
        self.ninja_id = data['ninja_id']
        self.sensei = Sensei.get_by_id({"id":data['sensei_id']}).name
        self.created_at = data["created_at"].strftime("%m/%d/%Y")
        self.updated_at = data["updated_at"]
    def delete(self):
        data={'id':self.id}
        query = "DELETE FROM messages WHERE id=%(id)s;"
        return connectToMySQL('Ninja_bucks').query_db(query,data)
    @classmethod
    def get_all_messages_for_ninja(cls,data):
        query = "SELECT * FROM messages WHERE ninja_id = %(ninja_id)s ORDER BY created_at DESC"
        messages_from_db = connectToMySQL('Ninja_bucks').query_db(query,data)
        messages = []
        for message in messages_from_db:
            messages.append(cls(message))
        return messages
    @classmethod
    def save(cls,data):
        query="INSERT INTO messages(ninja_buck_change, message_text, ninja_id, sensei_id, created_at, updated_at) VALUES(%(ninja_buck_change)s , %(message_text)s , %(ninja_id)s, %(sensei_id)s, NOW(), NOW());"
        message_id = connectToMySQL('Ninja_bucks').query_db(query,data)
        return message_id
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM messages WHERE id=%(id)s;"
        message = connectToMySQL('Ninja_bucks').query_db(query,data)
        return cls(message[0])
    @classmethod
    def delete_all_messages_for_ninja(cls,data):
        query = "DELETE FROM messages WHERE ninja_id=%(ninja_id)s;"
        return connectToMySQL('Ninja_bucks').query_db(query,data)

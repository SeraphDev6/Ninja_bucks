from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Ninja:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.user_name = data['user_name']
        self.ninja_bucks = data['ninja_bucks']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'].strftime("%m/%d/%Y, %I:%M %p")
    def add_ninja_bucks(self,amount):
        self.ninja_bucks += int(amount)
        data={
            'id':self.id,
            'ninja_bucks':self.ninja_bucks
        }
        query = "UPDATE ninjas SET ninja_bucks=%(ninja_bucks)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL('Ninja_bucks').query_db(query,data)
    def can_afford(self,amount):
        if self.ninja_bucks + int(amount) > 0:
            return True
        flash(f"{self.name} doesn't have enough Ninja Bucks!")
        return False
    def update(self,data):
        query = 'UPDATE ninjas SET name=%(name)s, user_name=%(user_name)s, updated_at=NOW() WHERE id=%(ninja_id)s'
        return connectToMySQL('Ninja_bucks').query_db(query,data)
    def delete_self(self):
        data={'id':self.id}
        query = "DELETE FROM ninjas WHERE id=%(id)s;"
        return connectToMySQL('Ninja_bucks').query_db(query,data)
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM ninjas"
        ninjas_from_db = connectToMySQL('Ninja_bucks').query_db(query)
        ninjas = []
        for ninja in ninjas_from_db:
            ninjas.append(cls(ninja))
        return ninjas
    @classmethod
    def save(cls, data):
        query = "INSERT INTO ninjas (name, user_name, ninja_bucks, created_at, updated_at) VALUES(%(name)s, %(user_name)s, 0, NOW(), NOW());"
        ninja_id = connectToMySQL('Ninja_bucks').query_db(query,data)
        return ninja_id
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM ninjas WHERE id=%(id)s;"
        ninja_from_db =  connectToMySQL('Ninja_bucks').query_db(query,data)
        return cls(ninja_from_db[0])
    @classmethod
    def has_username(cls,data):
        query = "SELECT id FROM ninjas WHERE user_name = %(user_name)s;"
        results = connectToMySQL('Ninja_bucks').query_db(query,data)
        if len(results)<1:
            flash("User Name not found. Please see a Sensei for assistance.")
            return False
        return results[0]['id']
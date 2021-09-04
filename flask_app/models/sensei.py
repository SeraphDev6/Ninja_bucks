from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
class Sensei:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.user_name = data['user_name']
        self.password = data['password']
        self.authority = data['authority']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    def delete_self(self):
        data={'id':self.id}
        query="DELETE FROM senseis WHERE id=%(id)s"
        return connectToMySQL('Ninja_bucks').query_db(query,data)
    @classmethod
    def valid_login(cls,data):
        query = "SELECT * FROM senseis WHERE user_name = %(user_name)s;"
        results = connectToMySQL('Ninja_bucks').query_db(query,data)
        if len(results)<1:
            flash("User Name or Password Incorrect. Please try again.")
            return False
        sensei = cls(results[0])
        if not bcrypt.check_password_hash(sensei.password,data['password']):
            flash("User Name or Password Incorrect. Please try again.")
            return False
        return sensei
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM senseis WHERE id=%(id)s;"
        senseis = connectToMySQL("Ninja_bucks").query_db(query,data)
        return cls(senseis[0])
    @classmethod
    def save(cls,data):
        new_data=Sensei.hash_password(data)
        query = "INSERT INTO senseis (name, user_name, password, authority, created_at, updated_at) VALUES(%(name)s, %(user_name)s, %(password)s, %(authority)s, NOW(), NOW());"
        sensei_id = connectToMySQL('Ninja_bucks').query_db(query,new_data)
        return sensei_id
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM senseis WHERE authority < 4;"
        senseis_from_db = connectToMySQL('Ninja_bucks').query_db(query)
        senseis = []
        for sensei in senseis_from_db:
            senseis.append(cls(sensei))
        return senseis
    @classmethod
    def update(cls,data):
        new_data=Sensei.hash_password(data)
        query="UPDATE senseis SET name=%(name)s, user_name=%(user_name)s, password=%(password)s, authority=%(authority)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL('Ninja_bucks').query_db(query,new_data)
    @staticmethod
    def validate_reg(data):
        if len(data['user_name'])<4:
            flash("Username must be at least 4 characters")
            return False
        if data['password'] != data['confirm-password']:
            flash("Passwords do not match")
            return False
        return True
    @staticmethod
    def hash_password(data):
        new_data= {
            'name':data['name'],
            'user_name':data['user_name'],
            'password':bcrypt.generate_password_hash(data['password']),
            'authority':data['authority']
        }
        if 'id' in data:
            new_data['id']=data['id']
        return new_data
    @staticmethod
    def any_senseis():
        query = "SELECT * FROM senseis"
        results = connectToMySQL('Ninja_bucks').query_db(query)
        return len(results)>0
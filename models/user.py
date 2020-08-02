# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 20:16:27 2020

@author: Sofian Fadli
"""

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
import psycopg2
import urllib.parse as urlparse
import os

class UserModel():
    
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):
        conn = None
        try:
            url = urlparse.urlparse(os.environ['DATABASE_URL'])
            dbname = url.path[1:]
            user = url.username
            password = url.password
            host = url.hostname
            port = url.port
                
            conn = psycopg2.connect(
                                        host=host, 
                                        dbname=dbname, 
                                        user=user, 
                                        password=password,
                                        port=port
                                        )
            cur = conn.cursor()
            cur.execute("""
                        select * from users where username = '{}';
                        """.format(username))
            row = cur.fetchone()
            if row:
                user = cls(*row)
            else:
                user = None
            cur.close()
            return user
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    
    @classmethod
    def find_by_id(cls, id):
        conn = None
        try:
            url = urlparse.urlparse(os.environ['DATABASE_URL'])
            dbname = url.path[1:]
            user = url.username
            password = url.password
            host = url.hostname
            port = url.port
                
            conn = psycopg2.connect(
                                        host=host, 
                                        dbname=dbname, 
                                        user=user, 
                                        password=password,
                                        port=port
                                        )
            cur = conn.cursor()
            cur.execute("""
                        select * from users where id_user = {};
                        """.format(id))
            row = cur.fetchone()
            if row:
                user = cls(*row)
                print(user)
            else:
                user = None
            cur.close()
            return user
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    
    @classmethod
    def insert_user(cls, username, user_password):
        """ insert new user into users """
        sql = """
            INSERT INTO users(
                                        username,
                                        password
                                    ) 
            VALUES(%s, %s)
            RETURNING id_user
        """
        conn = None
        try:
            url = urlparse.urlparse(os.environ['DATABASE_URL'])
            dbname = url.path[1:]
            user = url.username
            password = url.password
            host = url.hostname
            port = url.port
                
            conn = psycopg2.connect(
                                        host=host, 
                                        dbname=dbname, 
                                        user=user, 
                                        password=password,
                                        port=port
                                        )
            cur = conn.cursor()
            cur.execute(sql, (username, user_password))
            conn.commit()
            result = cur.fetchone()[0]
            cur.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

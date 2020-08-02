# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
import psycopg2
import urllib.parse as urlparse
import os

class StoreModel():
    
    """
    def __init__(self, id_store, store_name, id_user):
        self.id_store = id_store
        self.store_name = store_name
        self.id_user = id_user
    """
    def json(self):
        return {
                'id_store': self.id_store,
                'store_name': self.store_name,
                'id_user' : self.id_user
                }

    @classmethod
    def get_store_by_id_user(cls, id_user):
        """ 
            Mendapatkan store berdasarkan id_user
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
            cur.execute("""
                        select * from stores where id_user = {};
                        """.format(id_user))
            result = cur.fetchone()
            if result:
                cls.id_store = result[0]
                cls.store_name = result[1]
                cls.id_user = result[2]
            cur.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def get_store_by_name(cls, store_name):
        """ 
            Mendapatkan store berdasarkan name
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
            cur.execute("""
                        select * from stores where store_name = '{}';
                        """.format(store_name))
            result = cur.fetchone()
            if result:
                cls.id_store = result[0]
                cls.store_name = result[1]
                cls.id_user = result[2]
            cur.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def insert_store(cls, store_name, id_user):
        """ Create a new store for user  """
        sql = """
            INSERT INTO stores(
                                        store_name,
                                        id_user
                                    ) 
            VALUES(%s, %s)
            RETURNING id_store
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
            # create a new cursor
            cur = conn.cursor()
            cur.execute(sql, ( 
                              store_name,
                              id_user
                              )
                        )
            # commit the changes to the database
            conn.commit()
            results = cur.fetchone()[0]
            # close communication with the database
            cur.close()
            return results
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

# store = StoreModel()
# result = store.get_store_by_id_user(1)
# print(result[0])

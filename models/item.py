# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
import psycopg2
import urllib.parse as urlparse
import os

class ItemModel():

    def json(self):
        return {
                'id_item': self.id_item,
                'name': self.name,
                'price' : self.price,
                'descriptions' : self.descriptions,
                'id_store' : self.id_store
                }
    
    @classmethod
    def get_item_by_id(cls, id_item):
        """ 
            Mendapatkan item berdasarkan id
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
                        select * from items where id_item = {};
                        """.format(id_item))
            result = cur.fetchone()
            if result:
                cls.id_item = result[0]
                cls.name = result[1]
                cls.price = result[2]
                cls.descriptions = result[3]
                cls.id_store = result[4]
            cur.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def get_item_by_name(cls, name):
        """ 
            Mendapatkan item berdasarkan name
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
                        select * from items where name = '{}';
                        """.format(name))
            result = cur.fetchone()
            if result:
                cls.id_item = result[0]
                cls.name = result[1]
                cls.price = result[2]
                cls.descriptions = result[3]
                cls.id_store = result[4]
            cur.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    @classmethod
    def insert_item(cls, name, price, descriptions, id_store):
        """ insert new data into items  """
        sql = """
            INSERT INTO items(
                                        name,
                                        price,
                                        descriptions,
                                        id_store
                                    ) 
            VALUES(%s, %s ,%s, %s)
            RETURNING id_item
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
                              name,
                              price,
                              descriptions,
                              id_store
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
                
    @classmethod
    def delete_item(cls, id_item, id_store):
        """ 
            Menghapus item
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
                        delete from items where id_item = {} and id_store = {};
                        """.format(id_item, id_store))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    
    @classmethod
    def update_item(cls, id_item, name, price, descriptions, id_store):
        """ update item into items table  """
        sql = """
            UPDATE "items" SET name = %s, price = %s, descriptions = %s WHERE id_item = %s AND id_store = %s
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
            # Data lama dihapus terlebih dahulu
            cur.execute(sql, (name, price, descriptions, id_item, id_store))
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

class ItemList():
    
    @classmethod
    def create_json(cls, results):
        keys = ["id_item", "name", "price", "descriptions", "id_store"]
        dict_result = {}
        for key, result in zip(keys,results):
            dict_result[key] = result
        return dict_result
    
    def json(self):
        return list(map(self.create_json, self.results))

    @classmethod
    def get_items_by_id_store(cls, id_store):
        """ 
            Mendapatkan items berdasarkan id_store
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
                        select * from items where id_store = {};
                        """.format(id_store))
            results = cur.fetchall()
            if results:
                cls.results = results
            cur.close()
            return results
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    

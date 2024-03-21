from pymongo import MongoClient, errors
import pandas as pd

class MongoDBManager:
    def __init__(self, uri, db_name, user, passwd):
        self.uri = uri
        self.db_name = db_name
        self.user = user
        self.passwd = passwd
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri,
                                      username=self.user,
                                      password=self.passwd,
                                      authSource=self.db_name)
            self.db = self.client[self.db_name]
            # 데이터베이스 서버에 연결 시도
            self.client.admin.command('ping')
        except errors.ConnectionFailure as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
        return True, "Connection successful"

    def check_connection(self):
        if self.client is not None:
            try:
                # 서버에 ping을 보내 연결 상태 확인
                self.client.admin.command('ping')
            except:
                # 연결 상태에 문제가 있을 경우, client를 None으로 설정
                self.client = None
        if self.client is None:
            return self.connect()
        return True, "Connection is already established"

    def insert(self, collection_name, document):
        connected, msg = self.check_connection()
        if not connected:
            return False, msg
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            return True, result.inserted_id
        except Exception as e:
            return False, str(e)

    def insert_many(self, collection_name, documents):
        connected, msg = self.check_connection()
        if not connected:
            return False, msg
        try:
            collection = self.db[collection_name]
            result = collection.insert_many(documents)
            return True, result.inserted_ids
        except Exception as e:
            return False, str(e)

    def update(self, collection_name, query, new_values, upsert=True):
        connected, msg = self.check_connection()
        if not connected:
            return False, msg
        try:
            collection = self.db[collection_name]
            result = collection.update_one(query, {'$set': new_values}, upsert=upsert)
            return True, result.modified_count if result.modified_count > 0 else "Inserted new document"
        except Exception as e:
            return False, str(e)

    def delete(self, collection_name, query):
        connected, msg = self.check_connection()
        if not connected:
            return False, msg
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            return True, result.deleted_count
        except Exception as e:
            return False, str(e)

    def delete_all(self, collection_name):
        connected, msg = self.check_connection()
        if not connected:
            return False, msg
        try:
            result = self.db[collection_name].delete_many({})
            return True, result.deleted_count
        except Exception as e:
            return False, str(e)

    def select(self, collection_name, query):
        connected, msg = self.check_connection()
        if not connected:
            return False, msg
        try:
            collection = self.db[collection_name]
            result = collection.find(query)
            return True, list(result)
        except Exception as e:
            return False, str(e)

    def select_first_one(self, collection_name):
        connected, msg = self.check_connection()
        if not connected:
            return False, msg
        try:
            collection = self.db[collection_name]
            result = collection.find().limit(1)
            return True, list(result)
        except Exception as e:
            return False, str(e)

    def upsert(self, collection_name, key_column, document):
        connected, msg = self.check_connection()
        if not connected:
            return False, msg
        try:
            collection = self.db[collection_name]
            # key_column의 값이 document에 있는 해당 값과 일치하는 문서를 찾아 업데이트합니다.
            # 해당하는 문서가 없을 경우, 새로운 문서를 삽입합니다.
            result = collection.update_one({key_column: document[key_column]}, {"$set": document}, upsert=True)
            if result.upserted_id:
                return True, f"Inserted a new document with id: {result.upserted_id}"
            else:
                return True, f"Updated existing document(s), matched count: {result.matched_count}"
        except Exception as e:
            return False, str(e)

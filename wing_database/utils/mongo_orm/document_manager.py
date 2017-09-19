from bson.objectid import ObjectId


class DocumentManager(object):
    def __init__(self, document_class):
        self.klass = document_class

    def all(self):
        return map(lambda x: self.klass(**x), self.klass.__collection__.find())

    def insert(self, data):
        _id = self.klass.__collection__.insert_one(data).inserted_id
        data['_id'] = _id

    def update(self, data):
        ndata = {}
        ndata.update(data)
        _id = ndata.pop('_id')
        self.klass.__collection__.update_one(dict(_id=_id), {'$set': ndata})

    def delete(self, _id):
        self.klass.__collection__.delete_one(dict(_id=_id))

    def clear(self):
        self.klass.__collection__.remove()

    def find_one(self, **kwargs):
        if '_id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['_id'])

        res = self.klass.__collection__.find_one(kwargs)
        if res:
            return self.klass(**res)

        return None

    def find(self, **kwargs):
        if '_id' in kwargs:
            kwargs['_id'] = ObjectId(kwargs['_id'])

        res = self.klass.__collection__.find(kwargs)
        if res:
            return map(lambda x: self.klass(**x), res)

        return []

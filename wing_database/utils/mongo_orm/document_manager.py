from bson.objectid import ObjectId


class Find(object):
    def __init__(self, collection, query, klass):
        self.collection = collection
        self.query = query
        self.klass = klass

    def count(self):
        return self.collection.find(self.query).count()

    def sort(self, *args):
        return map(
            lambda x: self.klass(**x),
            self.collection.find(self.query).sort(*args)
        )

    def __iter__(self):
        return iter(
            map(
                lambda x: self.klass(**x),
                self.collection.find(self.query)
            )
        )


class DocumentManager(object):
    def __init__(self, document_class):
        self.klass = document_class

    def all(self):
        return self.find()

    def insert(self, data):
        _id = self.klass.__collection__.insert_one(data).inserted_id
        data['_id'] = _id

    def update(self, data):
        ndata = {}
        ndata.update(data)
        _id = ndata.pop('_id')
        self.klass.__collection__.replace_one(dict(_id=_id), ndata)

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

        return Find(
            self.klass.__collection__,
            kwargs,
            self.klass
        )

from .document_manager import DocumentManager

import six


class DocumentMeta(type):
    def __init__(self, name, bases, fields):
        super(DocumentMeta, self).__init__(name, bases, fields)
        self.objects = DocumentManager(self)


@six.add_metaclass(DocumentMeta)
class Document(object):
    __collection__ = None

    __version__ = '1.0.0'
    __fields__ = []
    __resolve__ = {}
    __reverse__ = {}
    __autos__ = {}

    __attr_exceptions = ('_data', '_dirty')
    __attr_allow = ('_id', '__ver')

    @classmethod
    def set_collection(cls, collection):
        cls.__collection__ = collection

    def __init__(self, **kwargs):
        self._data = {}
        self._data['__ver'] = self.__version__
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._dirty = '_id' not in kwargs

    def __getattr__(self, name):
        if name in self.__attr_exceptions:
            return super(Document, self).__getattr__(name)

        if name in self.__fields__ or name in self.__attr_allow:
            return self._data.get(name)

        elif name in self.__resolve__:
            fld, klass = self.__resolve__[name]
            if fld in self._data:
                return klass.objects.find_one(_id=self._data[fld])
            else:
                return None

        elif name in self.__reverse__:
            fld, klass = self.__reverse__[name]
            klass = klass()
            return klass.objects.find(**{fld: self._id})

        return super(Document, self).__getattr__(name)

    def __setattr__(self, name, value):
        if name in self.__attr_exceptions:
            return super(Document, self).__setattr__(name, value)

        if name in self.__fields__ or name in self.__attr_allow:
            self._data[name] = value
            self._dirty = True
        elif name in self.__resolve__:
            fld, klass = self.__resolve__[name]
            if not isinstance(value, klass):
                raise ValueError
            self._data[fld] = value._id
        else:
            raise AttributeError

    def __repr__(self):
        return '%s(**%s)' % (self.__class__.__name__, repr(self._data))

    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs).save(force_create=True)

    def delete(self):
        self.objects.delete(self._id)

    def save(self, force=False, force_create=False, skip_autos=False):
        if not skip_autos:
            for k, v in self.__autos__.items():
                self._data[k] = v()

        if '_id' in self._data and not force_create:
            if not self._dirty and not force:
                return self
            self.objects.update(self._data)
        else:
            self.objects.insert(self._data)

        self._dirty = False

        return self

    def json(self, resolve=None, exclude=None):
        result = {}
        result.update(self._data)
        result.pop('__ver')

        if resolve:
            for fld in resolve:
                result[fld] = getattr(self, fld).json()

        if exclude:
            for fld in exclude:
                if fld in result:
                    result.pop(fld)

        return result


class MiniDocument(object):
    __collection__ = None

    __fields__ = []
    __resolve__ = {}
    __reverse__ = {}
    __autos__ = {}

    __attr_exceptions = ('_data', '_dirty')
    __attr_allow = ('_id', '__ver')

    def __init__(self, **kwargs):
        self._data = {}
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._dirty = '_id' not in kwargs

    def __getattr__(self, name):
        if name in self.__attr_exceptions:
            return super(Document, self).__getattr__(name)

        if name in self.__fields__ or name in self.__attr_allow:
            return self._data.get(name)

        elif name in self.__resolve__:
            fld, klass = self.__resolve__[name]
            if fld in self._data:
                return klass.objects.find_one(_id=self._data[fld])
            else:
                return None

        elif name in self.__reverse__:
            fld, klass = self.__reverse__[name]
            klass = klass()
            return klass.objects.find(**{fld: self._id})

        return super(Document, self).__getattr__(name)

    def __setattr__(self, name, value):
        if name in self.__attr_exceptions:
            return super(Document, self).__setattr__(name, value)

        if name in self.__fields__ or name in self.__attr_allow:
            self._data[name] = value
            self._dirty = True
        elif name in self.__resolve__:
            fld, klass = self.__resolve__[name]
            if not isinstance(value, klass):
                raise ValueError
            self._data[fld] = value._id
        else:
            raise AttributeError

    def __repr__(self):
        return '%s(**%s)' % (self.__class__.__name__, repr(self._data))

    def json(self, resolve=None, exclude=None):
        result = {}
        result.update(self._data)

        if resolve:
            for fld in resolve:
                result[fld] = getattr(self, fld).json()

        if exclude:
            for fld in exclude:
                if fld in result:
                    result.pop(fld)

        return result

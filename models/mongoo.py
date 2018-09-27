import time
from pymongo import MongoClient

from utils import log

mongoo = MongoClient()


def timestamp():
    return int(time.time())


def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }

    doc = mongoo.db['data_id']

    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id


class Mongoo(object):
    @classmethod
    def valid_names(cls):
        names = [
            '_id',
            ('id', int, -1),
            ('deleted', bool, False),
        ]
        return names

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    @classmethod
    def new(cls, form=None, **kwargs):
        name = cls.__name__
        m = cls()
        names = cls.valid_names().copy()
        names.remove('_id')
        if form is None:
            form = {}

        for f in names:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                setattr(m, k, v)

        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError

        m.id = next_id(name)
        ts = int(time.time())
        m.created_time = ts
        m.updated_time = ts
        m.deleted = False
        m.save()
        return m

    @classmethod
    def _new_with_bson(cls, bson):

        m = cls()
        names = cls.valid_names().copy()

        names.remove('_id')
        for f in names:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                setattr(m, k, v)

        setattr(m, '_id', bson['_id'])
        return m

    @classmethod
    def all(cls):
        # 按照 id 升序排序
        # name = cls.__name__
        # ds = mongua.db[name].find()
        # l = [cls._new_with_bson(d) for d in ds]
        # return l
        return cls._find()

    # TODO, find(name, **kwargs)
    @classmethod
    def _find(cls, **kwargs):
        name = cls.__name__
        kwargs['deleted'] = False

        ds = mongoo.db[name].find(kwargs)

        l = [cls._new_with_bson(d) for d in ds]
        return l

    @classmethod
    def find_by(cls, **kwargs):
        return cls.find_one(**kwargs)

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def find(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def get(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def find_one(cls, **kwargs):
        kwargs['deleted'] = False
        l = cls._find(**kwargs)
<<<<<<< HEAD

=======
>>>>>>> 5f024ad043a6a596ec480e2fbbcab5cddc02d981
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    def search(cls, query):
        name = cls.__name__
        ds = mongoo.db[name].find({'title': {'$regex': '.*' + query + '.*'}})
        l = [cls._new_with_bson(d) for d in ds]
        result = filter(lambda x: x.deleted is False, l)
        return result

    def save(self):
        name = self.__class__.__name__
        mongoo.db[name].save(self.__dict__)

    @classmethod
    def delete(cls, id):
        name = cls.__name__
        query = {
            'id': id,
        }
        values = {
            "$set": {
                'deleted': True,
            },
        }
        mongoo.db[name].update_one(query, values)

    def blacklist(self):
        b = [
            '_id',
        ]
        return b

    def json(self):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        return d

from datetime import datetime
from sqlalchemy import func

from storyweb.core import db
from storyweb.model.user import User


class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Unicode)
    type = db.Column(db.Unicode)

    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author = db.relationship(User, backref=db.backref('entities',
                             lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Entity(%r,%r)>' % (self.id, self.label)

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'type': self.type,
            #'created_at': self.created_at,
            #'updated_at': self.updated_at,
        }

    @classmethod
    def by_label(cls, label, type=None):
        if label is None:
            return None
        q = db.session.query(cls)
        q = q.filter(func.trim(func.lower(cls.label)) ==
                     label.lower().strip())
        if type is not None:
            q = q.filter(cls.type == type)
        return q.first()

    @classmethod
    def lookup(cls, label, author, type=None):
        entity = cls.by_label(label, type=type)
        if entity is None:
            entity = cls()
            entity.label = label
            entity.type = type
            entity.author = author
            db.session.add(entity)
        return entity

from datetime import datetime

from tmi.core import db
from tmi.model.user import User


class Reference(db.Model):
    doc_type = 'reference'

    id = db.Column(db.Integer, primary_key=True)
    citation = db.Column(db.Unicode)
    url = db.Column(db.Unicode)
    source = db.Column(db.Unicode)
    soruce_url = db.Column(db.Unicode)

    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author = db.relationship(User, backref=db.backref('references',
                             lazy='dynamic'))

    card_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    card = db.relationship(User, backref=db.backref('references',
                           lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Reference(%r,%r,%r)>' % (self.id, self.citation, self.url)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.citation,
            'text': self.url,
            'date': self.source,
            'author': self.soruce_url,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

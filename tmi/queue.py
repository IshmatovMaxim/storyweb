import logging

from tmi.core import celery as app
from tmi.extract import extract_entities
from tmi.model import Card, Link, db
#from tmi import spiders

log = logging.getLogger(__name__)


@app.task
def extract(card_id):
    parent = Card.by_id(card_id)
    log.info('Extracting entities from "%s"...', parent.title)
    try:
        for offset, child in extract_entities(parent.text):
            data = {
                'offset': offset,
                'child': child
            }
            link = Link.find(parent, child)
            if link is None:
                link = Link()
            else:
                data['status'] = link.status
            link.save(data, parent, child.author)
        db.session.commit()
    except Exception, e:
        log.exception(e)


def lookup_all(card_id):
    pass
    #for spider_name in spiders.SPIDERS:
    #    lookup.delay(card_id, spider_name)


@app.task
def lookup(card_id, spider_name):
    try:
        card = Card.by_id(card_id)
        #spiders.lookup(card, spider_name)
        db.session.commit()
    except Exception, e:
        log.exception(e)

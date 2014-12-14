import dateutil.parser
from werkzeug.exceptions import Gone
from flask import Blueprint, g, request
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from restpager import Pager

from storyweb import authz
from storyweb.model import db, Card, Link
from storyweb.util import jsonify, obj_or_404, request_data


blueprint = Blueprint('links_api', __name__)


@blueprint.route('/api/1/cards/<parent_id>/links', methods=['GET'])
def index(parent_id):
    authz.require(authz.logged_in())
    card = obj_or_404(Card.by_id(parent_id))
    links = db.session.query(Link)
    links = links.filter(Link.parent == card)
    links = links.order_by(Link.offset.asc())
    pager = Pager(links, parent_id=parent_id)
    return jsonify(pager, index=True)


@blueprint.route('/api/1/cards/<parent_id>/links', methods=['POST', 'PUT'])
def create(parent_id):
    authz.require(authz.logged_in())
    card = obj_or_404(Card.by_id(parent_id))
    reference = Link().save(request_data(), card, g.user)
    db.session.commit()
    return jsonify(reference, status=201)


@blueprint.route('/api/1/cards/<parent_id>/links/_refresh')
def refresh(parent_id):
    authz.require(authz.logged_in())
    card = obj_or_404(Card.by_id(parent_id))
    link = aliased(Link)
    links = db.session.query(link.id)
    links = links.filter(link.parent == card)
    response = {'status': 'ok'}

    try:
        since = request.args.get('since')
        if since is not None:
            since = dateutil.parser.parse(since)

            child = aliased(Card)
            links = links.join(child, link.child)
            links = links.filter(or_(link.updated_at > since,
                                     child.updated_at > since))
    except (AttributeError, ValueError), e:
        response['status'] = 'ok'
        response['error'] = unicode(e)

    response['updated'] = [l.id for l in links]
    return jsonify(response)


@blueprint.route('/api/1/cards/<parent_id>/links/<id>', methods=['GET'])
def view(parent_id, id):
    authz.require(authz.logged_in())
    link = obj_or_404(Link.by_id(id, parent_id=parent_id))
    return jsonify(link)


@blueprint.route('/api/1/cards/<parent_id>/links/<id>', methods=['POST', 'PUT'])
def update(parent_id, id):
    authz.require(authz.logged_in())
    link = obj_or_404(Link.by_id(id, parent_id=parent_id))
    link.save(request_data(), link.parent, g.user)
    db.session.commit()
    return jsonify(link)


@blueprint.route('/api/1/cards/<parent_id>/links/<id>', methods=['DELETE'])
def delete(parent_id, id):
    authz.require(authz.logged_in())
    link = obj_or_404(Link.by_id(id, parent_id=parent_id))
    db.session.delete(link)
    db.session.commit()
    raise Gone()

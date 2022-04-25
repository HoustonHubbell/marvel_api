from flask import Blueprint, request, jsonify
from hero_inventory.helpers import token_required
from hero_inventory.models import db, User, Hero, hero_schema, heroes_schema


api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return{'some': 'value'}


@api.route('/heroes', methods=['POST'])
@token_required
def create_hero(current_user_token):
    name = request.json['name']
    backstory = request.json['backstory']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    powers = request.json['powers']
    weaknesses = request.json['weaknesses']
    foes = request.json['foes']
    lives_saved = request.json['lives_saved']
    spouse = request.json['spouse']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    hero  = Hero(name, backstory, first_name, last_name, powers, weaknesses, foes, lives_saved, spouse, user_token = user_token)

    db.session.add(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)

@api.route('/heroes', methods = ['GET'])
@token_required
def get_heroes(current_user_token):
    owner = current_user_token.token
    heroes = Hero.query.filter_by(user_token = owner).all()
    response = heroes_schema.dump(heroes)
    return jsonify(response)


@api.route('/heroes/<id>', methods = ['GET'])
@token_required
def get_hero(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        hero = Hero.query.get(id)
        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401


@api.route('/heroes/<id>', methods = ['POST', 'PUT'])
@token_required
def update_hero(current_user_token, id):
    hero = Hero.query.get(id)

    hero.name = request.json['name']
    hero.backstory = request.json['backstory']
    hero.first_name = request.json['first_name']
    hero.last_name = request.json['last_name']
    hero.powers = request.json['powers']
    hero.weaknesses = request.json['weaknesses']
    hero.foes = request.json['foes']
    hero.lives_saved = request.json['lives_saved']
    hero.spouse = request.json['spouse']
    hero.user_token = current_user_token.token

    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)

@api.route('/heroes/<id>', methods = ['DELETE'])
@token_required
def delete_hero(current_user_token, id):
    hero = Hero.query.get(id)
    db.session.delete(hero)
    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)


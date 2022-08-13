from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    pokedex_number = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String, nullable = False)
    type_one = db.Column(db.String, nullable=False)
    type_two = db.Column(db.String, nullable = True)
    ability = db.Column(db.String, nullable = True)
    weakness_one = db.Column(db.String, nullable = False)
    weakness_two = db.Column(db.String, nullable = True)

    def __init__(self, image_url, name, pokedex_number, description, type_one, type_two, ability, weakness_one, weakness_two):
        self.image_url = image_url
        self.name = name
        self.pokedex_number = pokedex_number
        self.description = description
        self.type_one = type_one
        self.type_two = type_two
        self.ability = ability
        self.weakness_one = weakness_one
        self.weakness_two = weakness_two
 
class PokemonSchema(ma.Schema):
    class Meta:
        fields = ( 'image_url', 'name', 'pokedex_number', 'description', 'type_one', 'type_two', 'ability', 'weakness_one', 'weakness_two')

pokemon_schema = PokemonSchema()
multiple_pokemon_schema = PokemonSchema(many = True)

@app.route('/pokemon/add', methods = ['POST'])
def add_movie():
    post_data = request.get_json()
    image_url = post_data.get('image_url')
    name = post_data.get('name')
    pokedex_number = post_data.get('pokedex_number')
    description = post_data.get('description')
    type_one = post_data.get('type_one')
    type_two = post_data.get('type_two')
    ability = post_data.get('ability')
    weakness_one = post_data.get('weakness_one')
    weakness_two = post_data.get('weakness_two')

    new_pokemon = Pokemon(image_url, name, pokedex_number, description, type_one, type_two, ability, weakness_one, weakness_two)
    db.session.add(new_pokemon)
    db.session.commit()

    return jsonify('You have added a new pokemon')

@app.route('/pokemon/get', methods = ['GET'])
def get_pokemon():
    pokemon = db.session.query(Pokemon).all()
    return jsonify(multiple_pokemon_schema.dump(pokemon))

@app.route('/pokemon/get/<pokedex_number>', methods = ['GET'])
def get_one_pokemon(pokedex_number):
    pokemon = db.session.query(Pokemon).filter(Pokemon.pokedex_number == pokedex_number).first()
    return jsonify(pokemon_schema.dump(pokemon))

@app.route('/pokemon/delete/<pokedex_number>', methods = ['DELETE'])
def remove_pokemon(pokedex_number):
    pokemon = db.session.query(Pokemon).filter(Pokemon.pokedex_number == pokedex_number).first()
    db.session.delete(pokemon)
    db.session.commit()

    return jsonify('Goodbye Pokemon')

@app.route('/pokemon/update/<pokedex_number>', methods = ['PUT'])
def update_pokemon(pokedex_number):
    post_data = request.get_json()
    image_url = post_data.get('image_url')
    name = post_data.get('name')
    pokedex_number = post_data.get('pokedex_number')
    description = post_data.get('description')
    type_one = post_data.get('type_one')
    type_two = post_data.get('type_two')
    ability = post_data.get('ability')
    weakness_one = post_data.get('weakness_one')
    weakness_two = post_data.get('weakness_two')

    pokemon = db.session.query(Pokemon).filter(Pokemon.pokedex_number == pokedex_number).first()

    pokemon.image_url = image_url
    pokemon.name = name
    pokemon.pokedex_number = pokedex_number
    pokemon.description = description
    pokemon.type_one = type_one
    pokemon.type_two = type_two
    pokemon.ability = ability
    pokemon.weakness_one = weakness_one
    pokemon.weakness_two = weakness_two

  

    db.session.commit()
    return jsonify("Your Pokemon has been updated")


if __name__ == "__main__":
    app.run(debug=True)
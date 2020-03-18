from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os , psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:tectoro123@192.168.20.57:5432/test"
db = SQLAlchemy(app)
ma = Marshmallow(app)


class users(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    profession = db.Column(db.String(100))
    qualification = db.Column(db.String(100))


class usersSchema(ma.Schema):
    class Meta():
        fields = ('name','profession','location','qualification')


user_schema = usersSchema()
users_schema = usersSchema(many=True)


@app.route("/add", methods=["POST"])
def add_user():
    name = request.json['name']
    location = request.json['location']
    profession = request.json['profession']
    qualification = request.json['qualification']

    new_user = users(name,location,profession,qualification)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user)


@app.route("/user", methods=["GET"])
def get_user():
    all_users = users.query.all()
    return users_schema.jsonify(all_users)


@app.route("/user/<text>", methods=["GET"])
def user_detail(text):
    user = users.query.filter((users.name == text)|(users.profession == text)|(users.location == text)|(users.qualification == text))
    return users_schema.jsonify(user)


@app.route("/update/<id>", methods=["PUT"])
def user_update(id):
    user=users.query.get(id)
    name = request.json['name']
    location = request.json['location']
    profession = request.json['profession']
    qualification = request.json['qualification']

    user.name = name
    user.location = location
    user.profession = profession
    user.qualification = qualification

    db.session.commit()
    return user_schema.jsonify(user)


@app.route("/delete/<id>", methods=["DELETE"])
def user_delete(id):
    user = users.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)

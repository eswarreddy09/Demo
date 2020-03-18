from flask import Flask , request , jsonify 
from flask_sqlalchemy import SQLAlchemy
import random , string


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:tectoro123@192.168.20.57:5432/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class users(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10))
    location = db.Column(db.String(10))
    profession = db.Column(db.String(10))
    qualification = db.Column(db.String(10))
    address=db.relationship ('userdetails', backref='users')

class userdetails(db.Model):
    plotno = db.Column(db.Integer,primary_key=True)
    landmark = db.Column(db.String(50))
    city = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id') )

db.create_all()


@app.route('/add', methods=['POST'])
def add_user():
    name = request.json['name']
    location = request.json['location']
    profession = request.json['profession']
    qualification = request.json['qualification']

    new_user = users(name,location,profession,qualification)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user)   

@app.route('/')
def get():
    result = list(db.session.execute(" select * from users"))
    return jsonify({'data':[dict(res) for res in result],'status':'success'}),200

@app.route('/user/<uid>')
def get_user(uid):
    args= request.args.to_dict()
    query=""" 
        select * from users where user_id = :uid 
    """

    if args.get('profession'):
        query += ' and trim(profession) = :profession'

    if args.get('location'):
        query += ' and trim(location) = :location'

    if args.get('name'):
        query += ' and trim(name) = :name'

    if args.get('qualification'):
        query +=' and trim(qualification) = :qualification'

    result = list(db.session.execute(query,{'uid':uid , **args  }))
    return jsonify({'data':[dict(res) for res in result],'status':'success'}),200



@app.route('/update', methods=['PUT'])
def update():
    body= request.get_json()
    sql_update_query = """update users set location = :location  , profession = :profession , name = :name , qualification = :qualification where user_id = :user_id"""
    db.session.execute(sql_update_query, body)
    db.session.commit()
    return jsonify({'status':'success'}),200

@app.route('/add', methods=['POST'])
def add():
    body= request.get_json()
    sql_update_query = """insert into users values location = :location  , profession = :profession , name = :name , qualification = :qualification"""
    db.session.execute(sql_update_query, body)
    db.session.commit()
    return jsonify({'status':'success'}),200

@app.route('/delete/<user_id>', methods=['DELETE'])
def delete(user_id):
    #body= request.get_json()
    sql_update_query = """delete from users where user_id = :user_id"""
    db.session.execute(sql_update_query,{'user_id':user_id} )
    db.session.commit()
    return jsonify({'status':'success'}),200


@app.route('/users/<text>')
def usersdetails(text):
    sql_update_query = """SELECT * FROM users t1 INNER JOIN userdetails t2 ON t1.user_id = t2.user_id where name=:text """
    result = list(db.session.execute(sql_update_query,{'text':text} ))
    return jsonify({'data':[dict(res) for res in result],'status':'success'}),200


if __name__ == '__main__':
    app.run(debug=True)

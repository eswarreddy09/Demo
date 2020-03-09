from flask import Flask , request , jsonify 
from flask_sqlalchemy import SQLAlchemy
import random , string


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:tectoro123@192.168.20.57:5432/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)



class users(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    profession = db.Column(db.String(100))
    qualification = db.Column(db.String(100))

    def __init__(self,name,location,profession,qualification):
        self.name = name
        self.location = location
        self.profession = profession
        self.qualification = qualification

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

    if args.get('profession') :
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
    sql_update_query = """update users set location = :location  , profession = :profession , name = :name where user_id = :user_id"""
    db.session.execute(sql_update_query, body)
    db.session.commit()
    return jsonify({'status':'success'}),200

@app.route('/delete', methods=['DELETE'])
def delete():
    body= request.get_json()
    sql_update_query = """delete from users where user_id = :user_id"""
    db.session.execute(sql_update_query, body)
    db.session.commit()
    return jsonify({'status':'success'}),200


# to create random string

"""for i in range(4):
    s= string.ascii_lowercase
    text = ''.join(random.sample(s,6))"""

if __name__ == '__main__':
    app.run(debug=True)

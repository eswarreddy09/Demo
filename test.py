from flask import Flask , request , jsonify 
from flask_sqlalchemy import SQLAlchemy
import random , string ,json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:tectoro123@192.168.20.57:5432/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)


class test(db.Model):
    
    data = db.Column(db.String(10),primary_key=True)

def data():
    for i in range(10):
        s= string.ascii_lowercase
        text = ''.join(random.sample(s,6))
        db.session.add(test(data=text))
    db.session.commit()
    return True

if __name__ == '__main__':
    #app.run(debug=True)
    data()

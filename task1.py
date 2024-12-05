# Rename file to app.py to run

from flask import Flask
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.String(required=True)
    age = fields.String(required=True)
    
    class Meta:
        fields = ('name', 'age')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)


# @app.route('/')
# def home():
#     return "Fitness Center Database"

# if __name__=='__main__':
#     app.run(debug=True)
from flask import Flask, jsonify, request
from flask_orator import Orator
from flask_restful import Resource, Api, reqparse
from urllib.request import urlopen
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
import requests
import simplejson 
import json
import csv
import sys

app = Flask(__name__)
app.config['ORATOR_DATABASES'] = {
    'mysql': {
        'driver': 'mysql',
        'host': 'wecalldb.cf7gurlbq7az.ap-south-1.rds.amazonaws.com',
        'database': 'wecalldb',
        'user': 'omkar',
        'password': 'omkar',
        'prefix': ''
    }
}

db = Orator(app)
api = Api(app)

parser = reqparse.RequestParser()

# MODELS FOR DATABASE
class UserLogin(db.Model):
    __primary_key__ = 'user_id'
    __table__ = 'user_login'
    __fillable__ = 'user_email_address'
    __timestamps__ = False

class Doctor(db.Model):
    __primary_key__ = 'doc_id'
    __table__ ='doctor'
    __fillable__ = 'doc_email_address'
    __timestamps__ = False

class SalesRep(db.Model):
    __primary_key__ = 'sales_rep_id'
    __table__ ='sales_rep'
    __fillable__ = 'sales_rep_email_address'
    __timestamps__ = False

# FLASK_RESTFUL RESOURCES
class SalesRepFetch(Resource):
    def get(self, sales_rep_id):
        salesRep = SalesRep.select('sales_rep_full_name','sales_rep_email_address').where('sales_rep_id', sales_rep_id).get()
        return salesRep.serialize()

class DoctorFetch(Resource):
    def get(self, doc_id):
        doctors = Doctor.select('doc_full_name','doc_email_address').where('doc_id', doc_id).get()
        return doctors.serialize()

class v_token(Resource):
    def get(self):
        # Get credentials for environment variables
        account_sid = 'ACcc27c6e3201c860c96b9fb1c101b6502'
        api_key = 'SKf91b87c2a5c8838402492faa48303032'
        api_secret = 'BjoC1paXjX6OrFD3bemFwCCd3LzxXcvJ'
        # Create an Access Token
        token = AccessToken(account_sid, api_key, api_secret)
        # Set the Identity of this token
        identity = request.values.get('identity') or 'infocision'
        roomName = "WeCall_test"
        token.identity = identity
        # Grant access to Video
        grant = VideoGrant()
        grant.room = roomName
        token.add_grant(grant)
        # Return token
        #return token.to_jwt()
        value = {"identity": identity, "roomName": roomName, "token": token.to_jwt().decode('utf-8')}
        # Dictionary to JSON Object using dumps() method
        # Return JSON Object
        print(value)
        return jsonify(value)

class DoctorUpsert(Resource):
    def post(self):
        try:
            parser.add_argument('doc_email_address', type=str, required=True)
            parser.add_argument('doc_dob', type=str, required=True)
            parser.add_argument('doc_mobile_no', type=str, required=True)
            parser.add_argument('doc_speciality', type=str, required=True)
            parser.add_argument('doc_full_name', type=str, required=True)
            parser.add_argument('doc_mdl_no', type=str, required=True)
            parser.add_argument('doc_qualification', type=str, required=True)
            parser.add_argument('doc_hq', type=str, required=True)
            parser.add_argument('doc_status', type=str, required=True)

            args = parser.parse_args()
            user = UserLogin.first_or_create(
                user_email_address=args['doc_email_address'])
            user.user_password = '12345'
            user.user_roles = 'doctor'
            user.user_created_by ='1'
            user.save()
            doctor = Doctor.first_or_create(
                doc_email_address=args['doc_email_address'])
            doctor.doc_dob = args['doc_dob']
            doctor.doc_mobile_no = args['doc_mobile_no']
            doctor.doc_speciality = args['doc_speciality']
            doctor.doc_full_name = args['doc_full_name']
            doctor.doc_mdl_no = args['doc_mdl_no']
            doctor.doc_qualification = args['doc_qualification']

            doctor.doc_hq = args['doc_hq']
            doctor.doc_status = args['doc_status']
            doctor.doc_uid = user.user_id
            doctor.save()
            return {'status': '200', 'message': 'Doctor created successfully'}
        except Exception as e:
            return {'status': '500', 'message': str(e)}

class UserLoginFetch(Resource):
    def post(self):
        parser.add_argument('user_email_address', type=str, required=True)
        parser.add_argument('user_password', type=str, required=True)
        args = parser.parse_args()
        users = UserLogin.select('user_id').where("user_email_address" ,"=" ,args['user_email_address']).where("user_password" ,"=", args['user_password']).get()
        user = users.serialize()
        try:
            if(user):
                return {'status': '200', 'message': 'Login Done'}
            else:
                return {'status': '400', 'message': 'Login not Done'}
        except Exception as e:
            return {'status': '403', 'message': str(e)}
        # users = UserLogin.select('user_email_address').where('user_id', user_id).get()
        # return users.serialize()


class UserLoginUpsert(Resource):
    def post(self):
        parser.add_argument('user_email_address', type=str, required=True)
        parser.add_argument('user_password', type=str, required=True)
        parser.add_argument('user_roles', type=str, required=True)
        parser.add_argument('user_created_by', type=int, required=True)

        # val_user_email_address = args['user_email_address'] if args['user_email_address'] != None else ""
        # val_user_password = args['user_password'] if args['user_password'] != None else ""
        # user_roles = args['user_roles'] if args['user_roles'] != None else ""
        # user_created_by = args['user_created_by'] if args['user_created_by'] != None else ""
        # user_modified_by = args['user_modified_by'] if args['user_modified_by'] != None else ""

        args = parser.parse_args()
        user = UserLogin.first_or_create(
            user_email_address=args['user_email_address'])
        user.user_password = args['user_password']
        user.user_roles = args['user_roles']
        user.user_created_by = args['user_created_by']
        user.user_modified_by = args['user_modified_by']
        user.save()
        return {'status': '200', 'message': 'User created successfully'}

class SalesRepUpsert(Resource):
    def post(self):
        try:
            parser.add_argument('sales_rep_email_address', type=str, required=True)
            parser.add_argument('sales_rep_emp_code', type=str, required=True)
            parser.add_argument('sales_rep_mobile_no', type=str, required=True)
            parser.add_argument('sales_rep_designation', type=str, required=True)
            parser.add_argument('sales_rep_full_name', type=str, required=True)
            parser.add_argument('sales_rep_hq', type=str, required=True)
            parser.add_argument('sales_rep_status', type=str, required=True)

            args = parser.parse_args()
            user = UserLogin.first_or_create(
                user_email_address=args['sales_rep_email_address'])
            user.user_password = '12345'
            user.user_roles = 'rep'
            user.user_created_by ='1'
            user.save()
            print(args)
            sales_rep = SalesRep.first_or_create(
                sales_rep_email_address=args['sales_rep_email_address'])
            sales_rep.sales_rep_emp_code = args['sales_rep_emp_code']
            sales_rep.sales_rep_mobile_no = args['sales_rep_mobile_no']
            sales_rep.sales_rep_designation = args['sales_rep_designation']
            sales_rep.sales_rep_full_name = args['sales_rep_full_name']
            sales_rep.sales_rep_hq = args['sales_rep_hq']
            sales_rep.sales_rep_status = args['sales_rep_status']
            sales_rep.sales_rep_comp_id = "1"
            sales_rep.sales_rep_uid = user.user_id
            sales_rep.save()
            return {'status': '200', 'message': 'Sales Representative created successfully'}
        except Exception as e:
            return {'status': '500', 'message': str(e)}

@app.route('/')
def index():
    return('infocision.in')

# @app.route('/csv')
# def csv_db():
#     uri = "http://127.0.0.1:2000/"
#     try:
#         response = urlopen(uri)
#         data_json = json.loads(response.read())
#         return (data_json)
#     except requests.ConnectionError:
#         return "Connection Error"

api.add_resource(UserLoginFetch, '/user')
api.add_resource(SalesRepFetch, '/salesrep/<int:sales_rep_id>')
api.add_resource(DoctorFetch, '/doctor/<int:doc_id>')
api.add_resource(UserLoginUpsert, '/adduser')
api.add_resource(DoctorUpsert, '/adddoctor')
api.add_resource(SalesRepUpsert, '/addsalesrep')
api.add_resource(v_token, '/token/')

if __name__ == '__main__':
    app.run(debug = True, port="2000")
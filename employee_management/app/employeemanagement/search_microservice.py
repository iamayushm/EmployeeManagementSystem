from employeemanagement.models import Employee
from employeemanagement import Resource, api, bcrypt
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
from flask import jsonify

'''
 Api which returns details of a particular employee based on username and password
'''

@auth.verify_password
def verify(email, password):
    if not (email and password):
        return False
    employee = Employee.query.filter_by(email=email).first()

    if employee and bcrypt.check_password_hash(employee.password, password) and employee.isAdmin:
        # app.logger.info('%s logged in successfully', employee.FirstName + " " + employee.LastName
        return True

    return False

class Info(Resource):

    decorators = [auth.login_required]

    def get(self, name, lname, address):


        users = Employee.query.filter_by(FirstName=name, LastName=lname, address=address).all()
        if not users:
            return jsonify({})
        employee_info = {}
        count = 1
        for user in users:
            card = {}
            card['id'] = user.id
            card["FirstName"] = user.FirstName
            card["LastName"] = user.LastName
            card["email"] = user.email
            card["phone"] = user.phone
            card["dob"] = user.dob
            card["address"] = user.address
            employee_info["user" + str(count)] = card
            count = count+1
        return jsonify(employee_info)

api.add_resource(Info, '/info/<string:name>/<string:lname>/<string:address>')

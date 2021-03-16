from employeemanagement import app, bcrypt, db, login_manager, api, Resource, mail
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from employeemanagement.forms import (RegistrationForm, LoginForm, UpdateForm, SearchForm, ChangePassword,
                                      NewAnnouncement, UpdateAnnouncement, RequestResetForm, ResetPasswordForm)
from employeemanagement.models import Employee, Announcement
from flask_login import login_user, logout_user, login_required, current_user
import requests
from flask_mail import Message
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@app.route("/")
@app.route("/home")
def home():
    announcements = Announcement.query.all()
    return render_template('home.html', announcements=announcements)


'''
    Register route so that a new employee can register himself
'''

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Your account has been created', 'success')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        employee = Employee(FirstName=form.FirstName.data,
                            LastName=form.LastName.data,
                            email=form.email.data,
                            phone=form.phone.data,
                            dob=form.dob.data,
                            address=form.address.data,
                            password=hashed_password
                            )
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('authentication/register.html', form=form)

# -----------------------------------------------------------------------------------------------------------------

'''
    Routes which enable user to login and logout . I have used flask-login for this purpose.
'''

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        # name = employee.FirstName + " " + employee.LastName
        if employee and bcrypt.check_password_hash(employee.password, form.password.data):

            # app.logger.info('%s logged in successfully', employee.FirstName + " " + employee.LastName)
            login_user(employee)
            return redirect(url_for('home'))
        else:
            # app.logger.info('%s failed to log in', form.email.data)
            flash('login unsuccessful,please check email and password', 'danger')

    return render_template('authentication/login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# -----------------------------------------------------------------------------------------------------------------

'''
    route for user to see his details when is logged in .
'''

@app.route("/details")
@login_required
def details():
    return render_template('details.html')

# -----------------------------------------------------------------------------------------------------------------

'''
    Route for Admin to see information of each user and also a search form is being created which uses an api to search
    for an user based on name and address
'''
import sys
@app.route("/master", methods=['GET', 'POST'])
@login_required
def master():
    if not current_user.isAdmin:
        flash("Please login as admin to access this page")
        logout_user()
        return redirect(url_for('login'))
    employ = Employee.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        name = form.name.data
        lname = form.lname.data
        address = form.address.data
        try:
            p = requests.get(f"http://127.0.0.1:5000/info/{name}/{lname}/{address}", auth=(current_user.email, 'root'))
            if len(p.json()) != 0:
                return render_template("admin/employee_search.html", posts=p.json())
            else :
                flash("No data found", 'info')
                return redirect(url_for('master'))
        except :
            flash("Invalid input : error ", 'info')
            return render_template("admin/EmployeeMaster.html", posts=employ, form=form)

    return render_template("admin/EmployeeMaster.html", posts=employ, form=form)

# ----------------------------------------------------------------------------------------------------------------


''' 
    Route so that user can update his password
'''

@app.route("/employee/<int:employee_id>/update_password", methods = ['GET', 'POST'])
@login_required
def update_password(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = ChangePassword()
    if form.validate_on_submit():

        if bcrypt.check_password_hash(employee.password, form.NewPassword.data):
            flash("Your old password and new password cannot be same", 'danger')
            return redirect(url_for('update_password', employee_id=employee.id))

        if bcrypt.check_password_hash(employee.password, form.OldPassword.data):
            hashed_password = bcrypt.generate_password_hash(form.NewPassword.data).decode("utf-8")
            employee.password = hashed_password
            db.session.commit()
            flash("Your password has been updated", 'success')
            return redirect(url_for('details'))
    return render_template("authentication/UpdatePassword.html", form=form)

# -------------------------------------------------------------------------------------------------------------

'''
    routes for updating or delete user from Employee database
'''

@app.route("/employee/<int:employee_id>/update", methods = ['GET', 'POST'])
@login_required
def update_employee(employee_id):

    if current_user.id != employee_id and current_user.isAdmin == False:
        flash("you don't have permission to access this page", 'warning')
        logout_user()
    employee = Employee.query.get_or_404(employee_id)
    form = UpdateForm()
    if form.validate_on_submit():
        employee.FirstName = form.FirstName.data
        employee.LastName = form.LastName.data
        if employee.email == form.email.data:
            employee.email = form.email.data
        else:
            user = Employee.query.filter_by(email=form.email.data).first()
            if user:
                flash("email already taken, Please enter different email id", 'danger')
                return redirect(url_for('update_employee',employee_id=employee_id))
            else:
                employee.email = form.email.data
        employee.phone = form.phone.data
        employee.dob = form.dob.data
        employee.address = form.address.data
        db.session.commit()
        flash("your details has been updated", 'success')
        if current_user.isAdmin:
            return redirect(url_for('master'))
        else:
            return redirect(url_for('details'))
    elif request.method == 'GET':
        form.FirstName.data = employee.FirstName
        form.LastName.data = employee.LastName
        form.email.data = employee.email
        form.phone.data = employee.phone
        form.dob.data = employee.dob
        form.address.data = employee.address
    return render_template('employee_detail.html', form=form)


@app.route("/employee/<int:employee_id>/delete", methods = ['GET', 'POST'])
def delete_employee(employee_id):
    data = Employee.query.get_or_404(employee_id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('master'))

# ---------------------------------------------------------------------------------

'''
    Routes form adding ,deleting and updating announcement
    Only Admin can add,update and delete an announcement
'''

@app.route("/announcement/add", methods=['GET', 'POST'])
@login_required
def add_announcement():
    if current_user.isAdmin==False:
        flash("login as admin to access this page", 'info')
        logout_user()
    form = NewAnnouncement()
    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data, content=form.content.data)
        db.session.add(announcement)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('announcement/update_announcement.html', form=form)

@app.route("/announcement/<int:announcement_id>/update", methods=['GET', 'POST'])
@login_required
def update_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    form = UpdateAnnouncement()
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.content = form.content.data
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = announcement.title
        form.content.data = announcement.content
    return render_template("announcement/update_announcement.html", form=form)

@app.route("/announcement/<int:announcement_id>/delete", methods=['GET','POST'])
@login_required
def delete_announcement(announcement_id):
    if current_user.isAdmin==False:
        flash("login as admin to access this page", 'info')
        logout_user()
    announcement = Announcement.query.get_or_404(announcement_id)
    db.session.delete(announcement)
    db.session.commit()
    return redirect(url_for('home'))

# ----------------------------------------------------------------------------------------------------------

'''
    If user forgets his password he will get a password reset link on his email
'''

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
This token will expire in 30 minutes
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Employee.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('ResetPassword/reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    employee = Employee.verify_reset_token(token)
    if employee is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        employee.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('ResetPassword/reset_token.html', title='Reset Password', form=form)

# ----------------------------------------------------------------------------------------------------------

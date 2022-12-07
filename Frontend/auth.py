from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.scrape'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("Login.html", user=current_user)


@auth.route("/ManageAccount", methods=['GET', 'POST'])
@login_required
def manageAccount():
    # Funktionalität fehlt noch
    if request.method == 'POST':
        user = current_user

        # get the current password and the new password from the request
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        new_password2 = request.form['new_password2']
        # verify that the current password is correct
        if check_password_hash(user.password, current_password):
            if new_password != new_password2:
                flash("New passwords do not match")

            else:

                if len(new_password) < 7:
                    flash('Password must be at least 7 characters.', category='error')
                else:
                    # if the current password is correct, hash the new password and update the user's password
                    user.password = generate_password_hash(new_password)
                    db.session.commit()
                    return redirect(url_for('views.scrape'))

        # the current password is incorrect
        flash("Current password does not match")
        return redirect(url_for('auth.manageAccount'))
    else:
        return render_template("/ManageAccount.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        print("in sighup")
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            print("EXISTS ALRDY")
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')


        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            print("COMMITED TO DB")
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.scrape'))

    return render_template("Signup.html", user=current_user)


@auth.route('/delete-account', methods=['GET'])
def delete_account():
    db.session.delete(current_user)
    db.session.commit()

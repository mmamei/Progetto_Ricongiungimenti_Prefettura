import os.path

from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, registerable, \
    roles_required, current_user
from flask_mail import Mail

from dbcode.db import *

# Create app
app = Flask(__name__)
app.config.from_pyfile('config_flask.py')
mail = Mail(app)
db = SQLAlchemy(app)
app.view_functions['static'] = login_required(app.send_static_file)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    ente = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with

from config import base_users

@app.before_first_request
def create_user():
    if not os.path.isfile('instance/users.db'):
        db.create_all()
        for u in base_users:
            registerable.register_user(email=u['email'], password=u['password'], ente=u['ente'])
            user_datastore.find_or_create_role(name=u['role'], description=u['role'])
            db.session.commit()
            user_datastore.add_role_to_user(u['email'], u['role'])
            db.session.commit()


#########################################
# Users operations

@app.route("/register_user", methods=['GET','POST'])
@login_required
@roles_required('super')
def register_user():
    if current_user.ente == 'prefettura':
        if request.method == 'GET':
            return render_template('security/register_user.html')
        else:
            email = request.form.get('email')
            password = request.form.get('password')
            ente = request.form.get('ente')
            ruolo = request.form.get('ruolo')
            try:
                registerable.register_user(email=email, password=password, ente=ente)
                user_datastore.find_or_create_role(name=ruolo)
                db.session.commit()
                user_datastore.add_role_to_user(email, ruolo)
                db.session.commit()
                flash('Utente registrato correttamente')
                return redirect('/')
            except:
                flash('Problemi nella registrazione')
                return redirect('/')
    else:
        flash('Operazione non consentita')
        return redirect('/')



@app.route("/remove_user", methods=['GET','POST'])
@login_required
@roles_required('super')
def remove_user():
    if current_user.ente == 'prefettura':
        if request.method == 'GET':
            return render_template('security/remove_user.html')
        else:
            try:
                email = request.form.get('email')
                u = user_datastore.find_user(email=email)
                user_datastore.delete_user(u)
                db.session.commit()
                flash('Utente eliminato correttamente')
                return redirect('/')
            except:
                flash('Problemi nell eliminazione')
                return redirect('/')

    else:
        flash('Operazione non consentita')
        return redirect('/')





#########################################
#Main operations

@app.route('/')
@app.route('/index')
@login_required
def home():
    migranti = select_migranti()
    return render_template('index.html',migranti=migranti)



@app.route('/migranti')
@login_required
def migranti():
    migranti = select_migranti()
    return render_template('migranti.html', migranti=migranti)


@app.route('/addfile',methods=['GET','POST'])
@login_required
def addfile():
    if current_user.ente == 'prefettura':
        if request.method == 'GET':
            return render_template('addfile.html')
        else:
            nome = request.form['nome']
            cognome = request.form['cognome']
            file = request.files['file']
            #print(file.filename)
            save_file(nome,cognome,file)
            flash('Operazione eseguita con successo')
            return redirect('/')
    else:
        flash('Operazione non consentita')
        return redirect('/')

@app.route('/getfiles',methods=['POST'])
@login_required
def getfiles():
    nome = request.form['nome']
    cognome = request.form['cognome']
    files = get_files(nome,cognome)
    #print(files)
    return render_template('files.html', nome=nome, cognome=cognome, files=files)

if __name__ == '__main__':
    app.run()
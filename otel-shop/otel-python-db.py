# pip install flask
# pip install -U Flask-SQLAlchemy
# pip install sqlalchemy
# pip install sqlalchemy.orm

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

# make the app and the db
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ruff.db"

class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# user db table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)

# couch db table
class Couch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)

# actually make the tables
with app.app_context():
    db.create_all()

##############################################
            # USER ENDPOINTS #
##############################################
@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars().all()
    return [{
        'name': user.username,
        'email': user.email,
    } for user in users]
    
@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("user/create.html")

@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return  {'name': user.username, 'email': user.email}

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete_by_id(id):
    user = db.get_or_404(User, id)

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("user_list"))

@app.route("/users/delete", methods=["GET"])
def user_delete():
    return render_template("user/delete.html")

##############################################
            # COUCH ENDPOINTS #
##############################################
@app.route("/couches")
def couch_list():
    couches = db.session.execute(db.select(Couch).order_by(Couch.item_name)).scalars().all()
    return [{
        'item_name': couch.item_name,
        'description': couch.description,
    } for couch in couches]
    
@app.route("/couches/create", methods=["GET", "POST"])
def couch_create():
    if request.method == "POST":
        couch = Couch(
            item_name=request.form["item_name"],
            description=request.form["description"],
        )
        db.session.add(couch)
        db.session.commit()
        return redirect(url_for("couch_detail", id=couch.id))

    return render_template("couch/create.html")

@app.route("/couch/<int:id>")
def couch_detail(id):
    couch = db.get_or_404(Couch, id)
    return  {'name': couch.item_name, 'email': couch.description}

@app.route("/couch/<int:id>/delete", methods=["GET", "POST"])
def couch_delete_by_id(id):
    couch = db.get_or_404(Couch, id)

    db.session.delete(couch)
    db.session.commit()
    return redirect(url_for("couch_list"))

@app.route("/couches/delete", methods=["GET"])
def couch_delete():
    return render_template("couch/delete.html")

# call this if you want brand new stuffs
# only call it on fresh DBs or you'll get an error
    # this also is an easy way to get errors tho :)
@app.route("/bootstrap")
def bootstrap():

    def bootstrap(thing):
        db.session.add(thing)
        db.session.commit()

    bootstrap_users = [
        User(username="Matt Ruyffelaert", email="matt.ruyffelaert@datadoghq.com"),
        User(username="Sean Diamond", email="sean.diamond@datadoghq.com"),
        User(username="Jansen Wenberg", email="jansen.wenberg@datadoghq.com"),
    ]

    for user in bootstrap_users:
        bootstrap(user)

    bootstrap_couches = [
        Couch(item_name="Model P", description="it is purple"),
        Couch(item_name="Model B", description="it is blue"),
        Couch(item_name="Model R", description="it is red"),
    ]

    for couch in bootstrap_couches:
        bootstrap(couch)

    return "Bootstrapped!"

from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create a Flask Instance
app = Flask(__name__)

# add a database
# old slqlite db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

# new MySQL db
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/our_users"

# secret key
app.config["SECRET_KEY"] = "mysupersecretkey"

# initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return "<Name %r>" % self.name


# create a form class
class NameForm(FlaskForm):
    name = StringField("What is your name!", validators=[DataRequired()])
    submit = SubmitField("Submit")


# user form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")


# @app.route("/")
# def sidebar():
#     return render_template("index.html")


@app.route("/")
def first_page():
    flash("Welcome")
    return render_template("firstpage.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/flasher")
def flasher_page():
    flash("welcome")
    return render_template("flasher.html")


@app.route("/forms", methods=["GET", "POST"])
def forms():
    name = None
    form = NameForm()
    # Validate form
    if form.validate_on_submit():
        flash("Form submitted succesfully!")

        name = form.name.data
        form.name.data = ""
    return render_template("form_template.html", name=name, form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


@app.route("/test")
def test_page():
    return render_template("test.html")


@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        # check if there are users with the email in database.
        user = Users.query.filter_by(email=form.email.data).first()
        # if aren't
        if user is None:
            # add user to database
            user = Users(
                name=form.name.data,
                email=form.email.data,
                favorite_color=form.favorite_color.data,
            )
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        form.favorite_color.data = ""
        flash("user added successfully successfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


# update database record
@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form[
            "name"
        ]  # almost the same as validation_on_submit
        name_to_update.email = request.form["email"]
        name_to_update.favorite_color = request.form["favorite_color"]

        try:
            db.session.commit()
            flash("User update successfully!")
            return render_template(
                "update.html", form=form, name_to_update=name_to_update
            )
        except:
            flash("Error")
            return render_template(
                "update.html", form=form, name_to_update=name_to_update
            )
    else:
        return render_template(
            "update.html", form=form, name_to_update=name_to_update, id=id
        )


@app.route("/delete/<int:id>")
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully")
        our_users = Users.query.order_by(Users.date_added)
        return render_template(
            "add_user.html", form=form, name=name, our_users=our_users
        )

    except:
        flash("Problem")
        return render_template(
            "add_user.html", form=form, name=name, our_users=our_users
        )

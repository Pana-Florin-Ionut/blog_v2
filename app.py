from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysupersecretkey"

# create a form class
class NameForm(FlaskForm):
    name = StringField("What is your name!", validators=[DataRequired()])
    submit = SubmitField("Submit")


# @app.route("/")
# def sidebar():
#     return render_template("index.html")


@app.route("/")
def first_page():
    return render_template("firstpage.html")


@app.route("/forms", methods=["GET", "POST"])
def forms():
    name = None
    form = NameForm()
    # Validate form
    if form.validate_on_submit():
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

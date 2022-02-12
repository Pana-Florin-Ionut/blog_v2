from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)


# @app.route("/")
# def sidebar():
#     return render_template("index.html")


@app.route("/")
def first_page():
    return render_template("firstpage.html")


@app.route("/forms")
def forms():
    return render_template("form_template.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

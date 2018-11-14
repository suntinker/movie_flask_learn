# coding:utf8

from . import home
from flask import render_template, redirect, url_for


@home.route("/")
def index():
    return render_template("home/index.html")


@home.route("/login/")
def login():
    return render_template("home/login.html")


@home.route("/logout/")
def logout():
    return redirect(url_for("home.login"))  #url_for()的参数是函数，而不是路径名，home.login等同于home下的# def login()

from flask import Blueprint, flash, redirect, render_template, session, url_for

home = Blueprint("home", __name__)

@home.route("/")
def index():
    if 'user' not in session:
        flash("Login to access this page", "warning")
        return redirect(url_for("auth.login"))
    
    return render_template("index.html")

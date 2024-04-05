from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from FirebaseUtils import create_user, upload_file, get_user_using_email, user_login

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        status, result = user_login(email, password)

        if status:
            print(result)
            session['user'] = result
            return redirect(url_for("home.index"))
        
        else:
            flash(result, "danger")
            return redirect(url_for("auth.login"))
    
    if 'user' in session:
        return redirect(url_for("home.index"))

    return render_template("auth/login.html")

@auth.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        display_name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        photo = request.files.get("profile")

        if get_user_using_email(email):
            flash("Email already in use", "danger")
            return redirect(url_for("auth.register"))
        
        else:
            file_name = email.split("@")[0].lower()
            photo_url = upload_file(photo.read(), name="profile_pics/"+file_name+".jpg")

            status, reason = create_user(display_name, email, password, photo_url)

            if status:
                flash("Account created successfully", "success")
                return redirect(url_for("auth.login"))
            
            else:
                flash(reason, "danger")
                return redirect(url_for("auth.register"))  


    return render_template("auth/register.html")

@auth.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))

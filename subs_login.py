# -*- coding: utf-8 -*-
"""
@author: António Brito / Carlos Bragança
(2024)
#objective: subs_login.py

"""""


from flask import render_template, request, session, redirect, url_for
from classes.userlogin import Userlogin

def login():
    return render_template("login.html", user="", password="", ulogin=session.get("user"), resul="")

def logoff():
    session.pop("user", None)
    return redirect(url_for('index'))

def chklogin():
    user = request.form["user"]
    password = request.form["password"]
    resul = Userlogin.chk_password(user, password)
    if resul == "Valid":
        session["user"] = user
        return check_usergroup(user)
    return render_template("login.html", user=user, password=password, ulogin=session.get("user"), resul=resul)

def check_usergroup(user):
    user_data = Userlogin.obj.get(user)
    if user_data:
        usergroup = user_data.usergroup
        if usergroup == "Patient":
            return redirect(url_for("patient_profile"))
        elif usergroup == "Employee":
            return redirect(url_for("employee_profile"))
        elif usergroup == "Dentist":
            return redirect(url_for("dentist_profile"))
        else:
            return render_template("error.html", message="Perfil de usuário desconhecido")
    return render_template("error.html", message="Usuário não encontrado")



    


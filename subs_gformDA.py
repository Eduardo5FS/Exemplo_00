# -*- coding: utf-8 -*-
"""
Created on Mon May 27 16:33:32 2024

@author: Eduardo Silva
"""

from flask import Flask, render_template, request, session
from classes.dentist import Dentist
from classes.employee import Employee
from classes.patient import Patient
from classes.administrador import Administrador
from classes.horarios_appointment import Appointment
from classes.userlogin import Userlogin
prev_option = ""

def gformDA(cname='', submenu=""):
    global prev_option
    ulogin = session.get("user")
    if ulogin is not None:
        cl = eval(cname)
        butshow = "enabled"
        butedit = "disabled"
        option = request.args.get("option")
        if prev_option == 'insert' and option == 'save':
            if cl.auto_number == 1:
                strobj = "None"
            else:
                strobj = request.form[cl.att[0]]
            for i in range(1, len(cl.att)):
                if cl.att[i] != 'password':  # Excluir o campo de senha
                    strobj += ";" + request.form[cl.att[i]]
            obj = cl.from_string(strobj)
            cl.insert(getattr(obj, cl.att[0]))
            cl.last()
        elif prev_option == 'edit' and option == 'save':
            obj = cl.current()
            for i in range(cl.auto_number, len(cl.att)):
                att = cl.att[i]
                if att != 'password':  # Excluir o campo de senha
                    setattr(obj, att, request.form[att])
            cl.update(getattr(obj, cl.att[0]))
        else:
            if option == "edit":
                butshow = "disabled"
                butedit = "enabled"
            elif option == "delete":
                obj = cl.current()
                cl.remove(obj.code)
                if not cl.previous():
                    cl.first()
            elif option == "insert":
                butshow = "disabled"
                butedit = "enabled"
            elif option == 'cancel':
                pass
            elif option == "first":
                cl.first()
            elif option == "previous":
                cl.previous()
            elif option == "next":
                cl.nextrec()
            elif option == "last":
                cl.last()
            elif option == 'exit':
                return render_template("index.html", ulogin=session.get("user"))
        prev_option = option
        obj = cl.current()
        if option == 'insert' or len(cl.lst) == 0:
            obj = dict()
            display_attributes = [att for att in cl.att if att != 'password']
            for att in cl.att:
                obj[att] = ""
        return render_template("lista_dentistas_admin.html", butshow=butshow, butedit=butedit,
                               cname=cname, obj=obj, att=cl.att, header=cl.header, des=cl.des,
                               ulogin=session.get("user"), auto_number=cl.auto_number,
                               submenu=submenu)
    else:
        return render_template("index.html", ulogin=ulogin)
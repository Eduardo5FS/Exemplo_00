from flask import Flask, render_template, request, session, redirect, url_for, g
from datafile import filename

import os

from classes.dentist import Dentist
from classes.employee import Employee
from classes.patient import Patient
from classes.horarios_appointment import Appointment
from classes.userlogin import Userlogin

import sqlite3
import random

app = Flask(__name__)

# Defina o caminho para o banco de dados
DATABASE = os.path.join(os.path.dirname(__file__), 'data', 'clinica.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

Dentist.read(DATABASE)
Employee.read(DATABASE)
Patient.read(DATABASE)
Appointment.read(DATABASE)
Userlogin.read(DATABASE)

prev_option = ""
submenu = ""
app.secret_key = 'BAD_SECRET_KEY'

upload_folder = os.path.join('static', 'ProductFotos')
app.config['UPLOAD'] = upload_folder


import subs_login as lsub
import subs_gform as gfsub
import subs_gformT as gfTsub
import subs_hform as gfhsub
import subs_subform as gfsubsub
import subs_productFoto as productFotosub
import subs_mapaOrderform as mapasub


@app.route("/")
def index():
    return render_template("index.html", ulogin=session.get("user"))
    
@app.route("/login")
def login():
    return lsub.login()

@app.route("/logoff")
def logoff():
    return lsub.logoff()

@app.route("/chklogin", methods=["post","get"])
def chklogin():
    return lsub.chklogin()

@app.route("/submenu", methods=["post","get"])
def getsubm():
    global submenu
    submenu = request.args.get("subm")
    ulogin=session.get("user")
    return render_template("index.html", ulogin=ulogin, usergroup = Userlogin.obj[ulogin].usergroup, submenu=submenu)

@app.route("/gform/<cname>", methods=["post","get"])
def gform(cname=''):
    submenu = request.args.get("subm")
    return gfsub.gform(cname,submenu)

@app.route("/gformT/<cname>", methods=["post","get"])
def gformT(cname=''):
    submenu = request.args.get("subm")
    return gfTsub.gformT(cname,submenu)

@app.route("/hform/<cname>", methods=["post","get"])
def hform(cname=''):
    submenu = request.args.get("subm")
    return gfhsub.hform(cname)


        
@app.route("/subform/<cname>", methods=["post","get"])
def subform(cname=""):
    submenu = request.args.get("subm")
    return gfsubsub.subform(cname,submenu)


@app.route("/productform", methods=["post","get"])
def productFoto():
    submenu = request.args.get("subm")
    cname = 'Product'
    return productFotosub.productFoto(app,cname,submenu)

@app.route("/order/mapa", methods=["post","get"])
def ordermapa():
    submenu = request.args.get("subm")
    cname = ''
    return mapasub.mapaOrderform(app,cname,submenu)

@app.route("/uc", methods=["post","get"])
def uc():
    return render_template("uc.html", ulogin=session.get("user"),submenu=submenu)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Receber dados do formulário de registro
        id_patient = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        telefone = request.form['telefone']
        email = request.form['email']
        sexo = request.form['sexo']
        password = request.form['password']
        
        # Criar instância de paciente com os dados recebidos
        new_patient = Patient(id_patient, firstname, lastname, birthdate, telefone, email, sexo, password)
        
        # Inserir novo paciente no banco de dados 'Patients'
        new_patient.insert(id_patient)
        
        # Criar instância de Userlogin para o novo paciente
        new_user = Userlogin(id_patient, "Patient", Userlogin.set_password(password))
        
        # Inserir novo usuário de login no banco de dados 'Userlogin'
        new_user.insert(id_patient)  # Aqui você pode usar o ID do paciente como identificador
        return redirect(url_for("login"))
    else:
        # Se a solicitação for GET, renderize o template do formulário de registro
        return render_template('register.html')
    

@app.route("/dentist_profile")
def dentist_profile():
    if "user" in session:
        ulogin = session.get("user")
        user = Userlogin.obj.get(ulogin)  # Use .get() para evitar KeyError
        if user and user.usergroup == "Dentist":
            dentist = Dentist.obj.get(ulogin)
            if dentist:
                return render_template("dentist_profile.html", dentist=dentist)
    return redirect(url_for('index'))


@app.route("/patient_profile")
def patient_profile():
    if "user" in session:
        ulogin = session.get("user")
        user = Userlogin.obj.get(ulogin)
        if user and user.usergroup=="Patient":
            patient = Patient.obj.get(ulogin)
            if patient:
                return render_template("patient_profile.html", patient=patient)
    return redirect(url_for("index"))

@app.route("/employee_profile")
def employee_profile():
    if "user" in session:
        ulogin = session.get("user")
        user = Userlogin.obj.get(ulogin)
        if user and user.usergroup=="Employee":
            employee = Employee.obj.get(ulogin)
            if employee:
                return render_template("employee_profile.html",employee=employee)
    return redirect(url_for("index"))


@app.route("/marcacao", methods=["post","get"])
def agenda():
    objh={}
    obj={}
    lista_dentistas = Dentist.get_dentist_names()
    return render_template("marcacao.html", obj=obj,objh=objh,horarios=horarios_disponiveis, lista_dentistas=lista_dentistas)

horarios_disponiveis = [
    "09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00", "18:00"
]


@app.route('/marcar_consulta', methods=['POST'])
def marcar_consulta():
    if request.method == 'POST':
        id_patient = request.form.get('id_patient')
        cedula_prof = request.form.get('_medico')
        date = request.form.get('_data')
        time = request.form.get('_hora')
        motivo = request.form.get('_motivo')

        try:
            # Conecte-se ao banco de dados SQLite e obtenha um cursor
            conn = get_db()
            cur = conn.cursor()

            # Insira os dados na tabela Appointment
            cur.execute('''INSERT INTO Appointment (date, time, id_patient, cedula_prof, motivo) VALUES (?, ?, ?, ?, ?)''',
                        (date, time, id_patient, cedula_prof, motivo))
            
            # Commit para salvar as alterações
            conn.commit()
        except sqlite3.Error as e:
            # Lide com erros de banco de dados
            print("Erro ao salvar consulta no banco de dados:", e)
            return "Erro ao salvar consulta no banco de dados: " + str(e)
        finally:
            # Feche a conexão com o banco de dados
            conn.close()

        # Redirecione de volta para a página de marcação de consulta
        return redirect('/marcacao')


@app.route('/save', methods=['POST'])
def save_appointment():
    if request.method == 'POST':
        id_patient = request.form.get('id_patient')
        cedula_prof = request.form.get('_medico')
        date = request.form.get('date')
        time = request.form.get('time')
        motivo = request.form.get('motivo')

        try:
            # Conecte-se ao banco de dados SQLite e obtenha um cursor
            conn = get_db()
            cur = conn.cursor()

            # Insira os dados na tabela Appointment
            cur.execute('''INSERT INTO Appointment (date, time, id_patient, cedula_prof, motivo) VALUES (?, ?, ?, ?, ?)''',
                        (date, time, id_patient, cedula_prof, motivo))
            
            # Commit para salvar as alterações
            conn.commit()
        except sqlite3.Error as e:
            # Lide com erros de banco de dados
            print("Erro ao salvar consulta no banco de dados:", e)
            return "Erro ao salvar consulta no banco de dados: " + str(e)
        finally:
            # Feche a conexão com o banco de dados
            conn.close()

        # Redirecione de volta para a página de marcação de consulta
        return redirect('/marcacao')

    
    
@app.route('/get_cedula_profissional')
def get_cedula_profissional():
    # Obter o nome do dentista da solicitação
    nome_dentista = request.args.get('_medico')
    
    # Consultar a base de dados Dentist para obter a cédula profissional [pelo nome do dentista
    cedula_profissional = Dentist.get_cedula_profissional_por_nome(nome_dentista)
    
    return cedula_profissional


    
if __name__ == '__main__':
    print(Userlogin.set_password("1100"))
    app.run(debug=True,port=6001)
    #app.run()

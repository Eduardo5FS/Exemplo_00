from flask import Flask, render_template, request, session, redirect, url_for,g
from datafile import filename

import os

from classes.dentist import Dentist
from classes.employee import Employee
from classes.patient import Patient
from classes.administrador import Administrador
from classes.horarios_appointment import Appointment
from classes.userlogin import Userlogin

import sqlite3
import random
import datetime as dt

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
Administrador.read(DATABASE)
Userlogin.read(DATABASE)

prev_option = ""
submenu = ""
app.secret_key = 'BAD_SECRET_KEY'

upload_folder = os.path.join('static', 'ProductFotos')
app.config['UPLOAD'] = upload_folder


import subs_login as lsub
import subs_gform as gfsub
import subs_gformT as gfTsub
import subs_subform as gfsubsub
import subs_gformE as gfsubE
import subs_gformP as gfsubP


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
       
@app.route("/subform/<cname>", methods=["post","get"])
def subform(cname=""):
    submenu = request.args.get("subm")
    return gfsubsub.subform(cname,submenu)


@app.route("/gformE/<cname>", methods=["post","get"])
def gformE(cname=''):
    submenu = request.args.get("subm")
    return gfsubE.gformE(cname,submenu)

@app.route("/gformP/<cname>", methods=["post","get"])
def gformP(cname=''):
    submenu = request.args.get("subm")
    return gfsubP.gformP(cname,submenu)

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

@app.route("/admin_profile")
def admin_profile():
    if "user" in session:
        ulogin = session.get("user")
        user = Userlogin.obj.get(ulogin)
        if user and user.usergroup=="Administrador":
            administrador = Administrador.obj.get(ulogin)
            if administrador:
                return render_template("admin_profile.html",administrador=administrador)
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
        nome_medico = request.form.get('_medico')
        cedula_prof = obter_cedula_medico(nome_medico)  # Obter a cédula do médico
        date = request.form.get('_data')
        time = request.form.get('_hora')
        motivo = request.form.get('_motivo')

        # Verificar se todos os campos obrigatórios estão preenchidos
        if not all([id_patient, cedula_prof, date, time, motivo]):
            return "Erro: Todos os campos devem ser preenchidos."

        print(f"Dados Recebidos: id_patient={id_patient}, cedula_prof={cedula_prof}, date={date}, time={time}, motivo={motivo}")

        try:
            conn = get_db()
            cur = conn.cursor()

            cur.execute('''INSERT INTO Appointment (date, time, id_patient, cedula_prof, motivo) VALUES (?, ?, ?, ?, ?)''',
                        (date, time, id_patient, cedula_prof, motivo))
            
            conn.commit()
        except sqlite3.Error as e:
            print("Erro ao salvar consulta no banco de dados:", e)
            return "Erro ao salvar consulta no banco de dados: " + str(e)
        finally:
            conn.close()

        return redirect('/marcacao')


def obter_cedula_medico(nome_medico):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT cedula_prof FROM Dentist WHERE firstname  ||' '||  lastname = ?", (nome_medico,))
        resultado = cur.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None
    except sqlite3.Error as e:
        print("Erro ao buscar cédula no banco de dados:", e)
        return None
    finally:
        conn.close()
        

@app.route('/save', methods=['POST'])
def save_appointment():
    if request.method == 'POST':
        code =  random.randint(100, 999)
        id_patient = session.get("user")
        nome_medico = request.form.get('_medico')
        cedula_prof =  obter_cedula_medico(nome_medico)  # Obter a cédula do médico
        date = request.form.get('_data')
        time = request.form.get('_hora')
        motivo = request.form.get('_motivo')
       
        # Verificar se todos os campos obrigatórios estão preenchidos
        if not all([code, id_patient, cedula_prof, date, time, motivo]):
            return "Erro: Todos os campos devem ser preenchidos."

        # Verificar se a data é posterior à data atual
        current_date = dt.datetime.today().date()
        appointment_date = dt.datetime.strptime(date, "%Y-%m-%d").date()
        if appointment_date <= current_date:
            return "Impossível marcar consulta: A data da consulta deve ser posterior à data atual."

        try:
            conn = get_db()
            cur = conn.cursor()

            # Verificar se já existe uma marcação para o mesmo dentista naquele dia e hora
            cur.execute('''SELECT * FROM Appointment WHERE cedula_prof = ? AND date = ? AND time = ?''',
                        (cedula_prof, date, time))
            existing_appointment = cur.fetchone()
            if existing_appointment:
                return f"Já existe uma marcação para o(a) dentista {nome_medico}, no dia {date} às {time}h."

            # Inserir a nova marcação
            cur.execute('''INSERT INTO Appointment (code, date, time, id_patient, cedula_prof, motivo) VALUES (?, ?, ?, ?, ?, ?)''',
                        (code, date, time, id_patient, cedula_prof, motivo))
            
            conn.commit()
        except sqlite3.Error as e:
            print("Erro ao salvar consulta:", e)
            return "Erro ao salvar consulta: " + str(e)
        finally:
            conn.close()

        return redirect('/marcacao')

    
@app.route("/proximas_consultas_patient")
def proximas_consultas_patient():
    if "user" in session:
        ulogin = session.get("user")
        user = Userlogin.obj.get(ulogin)
        if user and user.usergroup == "Patient":
            appointments = get_appointments_by_patient_id(ulogin)
            return render_template("proximas_consultas_patient.html", appointments=appointments)
    return redirect(url_for("index"))

@app.route("/proximas_consultas_dentist")
def proximas_consultas_dentist():
    if "user" in session:
        ulogin = session.get("user")
        user = Userlogin.obj.get(ulogin)
        if user and user.usergroup == "Dentist":
            appointments = get_appointments_by_cedula_prof(ulogin)
            return render_template("proximas_consultas_dentist.html", appointments=appointments)
    return redirect(url_for("index"))

@app.route("/consultas_employee")
def consultas_employee():
    if "user" in session:
        ulogin = session.get("user")
        user = Userlogin.obj.get(ulogin)  # Chame o método get() diretamente na classe Userlogin
        if user and user.usergroup == "Employee":
            appointments = get_all_appointments()
            return render_template("consultas_employee.html", appointments=appointments)
    return redirect(url_for("index"))
    

def get_all_appointments():
    # Função para obter todas as consultas de todos os pacientes
    conn = get_db()
    cur = conn.cursor()
    query= '''SELECT code, date, time, id_patient, cedula_prof, motivo
    FROM Appointment
    ORDER BY date, time'''
    cur.execute(query)
    appointments = cur.fetchall()
    conn.close()
    return [dict(code=row[0], date=row[1], time=row[2], id_patient=row[3], cedula_prof=row[4], motivo=row[5]) for row in appointments]


def get_appointments_by_cedula_prof(cedula_prof):
    try:
        conn = get_db()
        cur = conn.cursor()
        query = '''
        SELECT code, date, time, id_patient, motivo 
        FROM Appointment 
        WHERE cedula_prof = ? 
        ORDER BY date, time
        '''
        cur.execute(query, (cedula_prof,))
        appointments = cur.fetchall()
        conn.close()
        # Converta os resultados para um formato adequado
        return [dict(code=row[0], date=row[1], time=row[2], id_patient=row[3], motivo=row[4]) for row in appointments]
    except sqlite3.Error as e:
        print(f"Erro ao buscar consultas: {e}")
        return []
    
def get_appointments_by_patient_id(patient_id):
    try:
        conn = get_db()
        cur = conn.cursor()
        # Formata a data e hora atual para comparação
        current_datetime = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
        # Consulta SQL para buscar consultas futuras
        query = '''
        SELECT code, date, time, cedula_prof, motivo 
        FROM Appointment 
        WHERE id_patient = ? AND datetime(date || ' ' || time) > datetime(?) 
        ORDER BY date, time
        '''
        cur.execute(query, (patient_id, current_datetime))
        appointments = cur.fetchall()
        conn.close()
        return [dict(code=row[0], date=row[1], time=row[2], cedula_prof=row[3], motivo=row[4]) for row in appointments]
    except sqlite3.Error as e:
        print(f"Erro ao buscar consultas: {e}")
        return []


@app.route('/lucro', methods=['GET', 'POST'])
def lucro_diario():
    if request.method == 'POST':
        # Receber dados do formulário de registro
        date = request.form['date']
        new_date = str(dt.datetime.strptime(date, "%Y-%m-%d").date())
        lucro_diario=calcular_lucro_diario(new_date)
        return render_template('lucro.html', lucro_diario=lucro_diario, date=new_date)
    else:
        # Se a solicitação for GET, renderize o template do formulário de registro
        return render_template('lucro.html', lucro_diario = "--", date="YYYY-mm-dd")
    
def calcular_lucro_diario(date):
    try:
        conn = sqlite3.connect('clinica.db')
        cur = conn.cursor()

        # Consulta para obter as marcações (consultas) para um determinado dia
        cur.execute('''SELECT motivo FROM Appointment WHERE date = ?''', (date,))
        appointments = cur.fetchall()

        total_lucro = 0

        # Para cada consulta marcada, consultar o preço associado a ela na tabela TypesAppointment e somar ao total
        for appointment in appointments:
            motivo = appointment[5]
            cur.execute('''SELECT preco FROM types_appointment WHERE motivo = ?''', (motivo,))
            preco = cur.fetchone()
            if preco:
                total_lucro += preco[0]  # Adiciona o preço ao total do lucro

        return total_lucro

    except sqlite3.Error as e:
        print("Erro ao calcular lucro diário:", e)
        return 0  # Retorna 0 em caso de erro
    finally:
        conn.close()


if __name__ == '__main__':
    print(Userlogin.set_password("admin999"))
    app.run(debug=True,port=6001)
    #app.run()

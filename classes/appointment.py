#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 23:56:49 2024

@author: guilhermegoncalves
"""

import sqlite3
import datetime
# Import the generic class
from classes.gclass import Gclass
from classes.dentist import Dentist
from classes.patient import Patient

class Appointment(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    auto_number = 1 # = 1 in case of auto number on
    nkey = 1
    # class attributes, identifier attribute must be the first one on the list
    att = ['_code','_date', '_time','_id_patient', '_cedula_prof', '_motivo']
    # Class header title
    header = 'Appointments'
    # field description for use in, for example, in input form
    des = ['Code','Date', 'Time', 'Patient ID', 'Cédula Profissional', 'Motive']
    # Constructor: Called when an object is instantiated
    def __init__(self, code, date, time, id_patient, cedula_prof, motivo):
        super().__init__()
        # Uncomment in case of auto number on
        if code == 'None':
            codes = Appointment.getatlist('_code')
            if codes == []:
                code = str(1)
            else:
                code = str(max(map(int,Appointment.getatlist('_code'))) + 1)
        # Object attributes
        # Check the customer referential integrity
        if id_patient in Patient.lst:
            self._code = code
            self._date = datetime.date.fromisoformat(date)
            self._time = datetime.time.fromisoformat(time)
            self._id_patient = id_patient
            self._cedula_prof = cedula_prof
            self._motivo = motivo
            # Add the new object to the Order list
            Appointment.obj[code] = self
            Appointment.lst.append(code)
        else:
            print('Patient ', id_patient, ' not found')
    # Object properties
    # code property getter method
    @property
    def code(self):
        return self._code
    # date property getter method
    @property
    def date(self):
        return self._date
    # date property setter method
    @date.setter
    def date(self, date):
        self._date = date
    #time property getter method
    @property
    def time(self):
        return self._time
    #time property setter method
    @time.setter
    def time(self, time):
        self._time = time
    # patient property getter method
    @property
    def id_patient(self):
        return self._id_patient 
    # patient property setter method
    @id_patient.setter
    def id_patient(self, id_patient):
        if id_patient in Patient.lst:
            self._id_patient = id_patient
        else:
            print('Patient ', id_patient, ' not found')  
    # dentist property getter method
    @property
    def cedula_prof(self):
        return self._cedula_prof
    # dentist property setter method
    @cedula_prof.setter
    def cedula_prof(self, cedula_prof):
        if cedula_prof in Dentist.lst:
            self._cedula_prof = cedula_prof
        else:
            print('Dentist ', cedula_prof, ' not found') 
    @property
    def motivo(self):
        return self._motivo
    @motivo.setter
    def motivo(self, motivo):
        conn = sqlite3.connect("types_appointment.db")
        cur = conn.cursor()
        
        # Consulta se o motivo existe na coluna 'types' da tabela 'types' do banco de dados
        cur.execute('''SELECT COUNT(*) FROM types WHERE types = ?''', (motivo,))
        count = cur.fetchone()[0]

        # Verifica se o motivo existe
        if count > 0:
            self._motivo = motivo
        else:
            print('Motivo inválido!')
        
        # Fechar a conexão com o banco de dados
        conn.close()
    
    @classmethod
    def lucro_diario(cls, date):
        total_lucro = 0
        
        # Conectando-se ao banco de dados
        conn = sqlite3.connect("types_appointment.db")
        cur = conn.cursor()

        # Iterando sobre os compromissos
        for appointment_code in cls.lst:
            appointment = cls.obj[appointment_code]
            
            # Verificando se o compromisso é na data especificada
            if appointment.date == date:
                # Obtendo o motivo da consulta
                motivo_consulta = appointment.motivo
                
                # Consultando o preço associado ao motivo da consulta no banco de dados
                cur.execute('''SELECT price FROM types WHERE types = ?''', (motivo_consulta,))
                preco = cur.fetchone()

                # Se houver um preço associado ao motivo da consulta, adicionamos ao total de lucro
                if preco is not None:
                    total_lucro += preco[0]

        # Fechando a conexão com o banco de dados
        conn.close()

        return total_lucro
    
    
from classes.appointment import Appointment
import datetime

# Defina a data para a qual deseja calcular o lucro diário
data_especifica = datetime.date(2024, 5, 15)  # Substitua pela data desejada

# Chame o método lucro_diario da classe Appointment
lucro = Appointment.lucro_diario(data_especifica)

# Imprima o resultado
print("O lucro diário para", data_especifica, "foi de:", lucro)

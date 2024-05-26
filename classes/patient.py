# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:58:51 2024

@author: 6834422
"""

from classes.gclass import Gclass
import datetime

class Patient(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    auto_number = 0
    nkey = 1
    att = ['_id_patient','_firstname','_lastname','_birthdate','_telefone','_email','_sexo','_password']
    
    header = 'Patient'
    des = ['Patient ID','Firstname','Lastname','Birthdate','Telefone','Email','Sexo','Password']
    
    def __init__(self, id_patient, firstname, lastname, birthdate, telefone, email, sexo, password):
        super().__init__()
        self._id_patient = id_patient
        self._firstname = firstname
        self._lastname = lastname
        self._birthdate = birthdate
        self._telefone = telefone
        self._email = email
        self._sexo = sexo
        self._password = password
        
        Patient.obj[id_patient] = self
        Patient.lst.append(id_patient)
    # Object properties
    # getter methodes
    # code property getter method
    @property
    def id_patient(self):
        return self._id_patient
    # password property getter method
    @property
    def password(self):
        return self._login
    @property
    def firstname(self):
        return self._firstname
    @property 
    def lastname(self):
        return self._lastname
    @property 
    def birthdate(self):
        return self._birthdate
    @property 
    def telefone(self):
        return self._telefone
    @property 
    def email(self):
        return self._email
    @property 
    def sexo(self):
        return self._sexo
    @id_patient.setter
    def id_patient(self,id_patient):
        self._id_patient = id_patient
    @password.setter
    def password(self, password):
        self._password = password

    @staticmethod          
    def login(id_patient,password):
       verify=False
       for p in Patient.lst:
           if str(password)==Patient.obj[p].password and str(id_patient)==Patient.obj[p].id_patient:
               verify=True
               p_code = Patient.obj[p].id_patient
               return p_code
       if not verify:
           print("User not found!")
           return None
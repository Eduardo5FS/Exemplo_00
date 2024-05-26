# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:56:27 2024

@author: 6834422
"""

from classes.gclass import Gclass
import datetime

class Dentist(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    auto_number = 0
    nkey = 1
    att = ['_cedula_prof','_firstname','_lastname','_birthdate','_telefone','_email','_password']
    
    header = 'Dentist'
    des = ['Cedule Prof.','Firstname','Lastname','Birthdate','Telefone','Email','Password']
    
    def __init__(self, cedula_prof, firstname, lastname, birthdate, telefone, email, password):
        super().__init__()
        self._cedula_prof = cedula_prof
        self._firstname = firstname
        self._lastname = lastname
        self._birthdate = birthdate
        self._telefone = telefone
        self._email = email
        self._password = password
        
        Dentist.obj[cedula_prof] = self
        Dentist.lst.append(cedula_prof)
    # Object properties
    # getter methodes
    # code property getter method
    @property
    def cedula_prof(self):
        return self._cedula_prof
    # password property getter method
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
    def password(self):
        return self._login
    @cedula_prof.setter
    def cedula_prof(self,cedula_prof):
        self._cedula_prof = cedula_prof
    @password.setter
    def password(self, password):
        self._password = password

    @staticmethod          
    def login(cedula_prof,password):
       verify=False
       for d in Dentist.lst:
           if str(password)==Dentist.obj[d].password and str(cedula_prof)==Dentist.obj[d].cedula_prof:
               verify=True
               d_code = Dentist.obj[d].cedula_prof
               return d_code
       if not verify:
           print("User not found!")
           return None
       
    @staticmethod
    def get_dentist_names():
        return [Dentist.obj[cedula_prof].firstname + " " + Dentist.obj[cedula_prof].lastname for cedula_prof in Dentist.lst]
    
    
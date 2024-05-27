#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 16:45:35 2024

@author: guilhermegoncalves
"""

from classes.gclass import Gclass

class Administrador(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    auto_number = 0
    nkey = 1
    att = ['_cod_adm','_firstname','_lastname','_birthdate','_telefone','_email','_password']
    
    header = 'Admin'
    des = ['Cod Admin','Firstname','Lastname','Birthdate','Telefone','Email','Password']
    
    def __init__(self, cod_adm, firstname, lastname, birthdate, telefone, email, password):
        super().__init__()
        self._cod_adm = cod_adm
        self._firstname = firstname
        self._lastname = lastname
        self._birthdate = birthdate
        self._telefone = telefone
        self._email = email
        self._password = password
        
        Administrador.obj[cod_adm] = self
        Administrador.lst.append(cod_adm)
    # Object properties
    # getter methodes
    # code property getter method
    @property
    def cod_adm(self):
        return self._cod_adm
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
    @cod_adm.setter
    def cod_adm(self,cod_adm):
        self._cod_adm = cod_adm
    @password.setter
    def password(self, password):
        self._password = password

    @staticmethod          
    def login(cod_adm,password):
       verify=False
       for d in Administrador.lst:
           if str(password)==Administrador.obj[d].password and str(cod_adm)==Administrador.obj[d].cod_adm:
               verify=True
               d_code = Administrador.obj[d].cod_adm
               return d_code
       if not verify:
           print("User not found!")
           return None
       
    @staticmethod
    def get_admin_names():
        return [Administrador.obj[cod_adm].firstname + " " + Administrador.obj[cod_adm].lastname for cod_adm in Administrador.lst]
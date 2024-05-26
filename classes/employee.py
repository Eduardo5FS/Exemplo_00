# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:56:58 2024

@author: 6834422
"""

from classes.gclass import Gclass

class Employee(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    auto_number = 0
    nkey = 1
    att = ['_id_employee','_firstname','_lastname','_password']
    
    header = 'Employee'
    des = ['Employee ID','Firstname','Lastname','Password']
    
    def __init__(self, id_employee, firstname, lastname, password):
        super().__init__()
        self._id_employee = id_employee
        self._firstname= firstname
        self._lastname = lastname
        self._password = password
        
        Employee.obj[id_employee] = self
        Employee.lst.append(id_employee)
    # Object properties
    # getter methodes
    # code property getter method
    @property
    def id_employee(self):
        return self._id_employee
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
    @id_employee.setter
    def id_employee(self,id_employee):
        self._id_employee = id_employee
    @password.setter
    def password(self, password):
        self._password = password
    @firstname.setter 
    def firstname(self, firstname):
        self._firstname= firstname
    @lastname.setter 
    def lastname(self, lastname):
        self._lastname= lastname

    @staticmethod          
    def login(id_employee,password):
       verify=False
       for e in Employee.lst:
           if str(password)==Employee.obj[e].password and str(id_employee)==Employee.obj[e].id_employee:
               verify=True
               e_code = Employee.obj[e].id_employee
               return e_code
       if not verify:
           print("User not found!")
           return None
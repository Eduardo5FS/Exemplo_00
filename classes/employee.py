#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 23:55:55 2024

@author: guilhermegoncalves
"""

from classes.gclass import Gclass

class Employee(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    auto_number = 0
    nkey = 1
    att = ['_id_employee','_password']
    
    header = 'Employee'
    des = ['Employee ID','Password']
    
    def __init__(self, id_employee, password):
        super().__init__()
        self._id_employee = id_employee
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
    @id_employee.setter
    def id_employee(self,id_employee):
        self._id_employee = id_employee
    @password.setter
    def password(self, password):
        self._password = password

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




            

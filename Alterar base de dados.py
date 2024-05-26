# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:25:50 2024

@author: 6834422
"""

from datafile import filename

from classes.dentist import Dentist

Dentist.read(filename + 'clinica.db')

obj = Dentist.from_string("333333;Paulo;Santos;1967-12-02;966234910;paulosantos@cmd.com;paulosantos.cmd")
print("objeto sem estar gravado ",obj)

Dentist.insert(getattr(obj,Dentist.att[0]))

obj = Dentist.from_string("444444;Carmen;Fernandes;1963-02-12;938652150;carmenfernandes@cmd.com;carmenfernandes.cmd")
Dentist.insert(getattr(obj,Dentist.att[0]))


print("\nLista dos objetos gravados " ,Dentist.lst)


# alterar
obj = Dentist.first()
print ("\nPrimeiro objeto gravado ",obj)
obj.name = "444444"
Dentist.update(getattr(obj, Dentist.att[0]))

Dentist.read(filename + 'clinica.db')

print("\nobjectos gravados")    
for code in Dentist.lst:
    print(Dentist.obj[code])
    
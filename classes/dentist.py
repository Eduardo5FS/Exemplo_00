from classes.gclass import Gclass
import datetime

class Dentist(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    auto_number = 0
    nkey = 1
    att = ['_cedula_prof','_password']
    
    header = 'Dentist'
    des = ['Cedule Prof.','Password']
    
    def __init__(self, cedula_prof, firstname, lastname, birthdate, telefone, email, password):
        super().__init__()
        self._cedula_prof = cedula_prof
        self._firstname = firstname
        self._lastname = lastname
        self._birthdate = datetime.strptime(birthdate,"%Y-%m-%d").date()
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
       
        

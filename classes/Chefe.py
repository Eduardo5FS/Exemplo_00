from classes.gclass import Gclass
import datetime

class Admin(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    auto_number = 0
    nkey = 1
    att = ['_cod_adn','_firstname','_lastname','_birthdate','_telefone','_email','_password']
    
    header = 'Admin'
    des = ['Cod Admin','Firstname','Lastname','Birthdate','Telefone','Email','Password']
    
    def __init__(self, cod_adn, firstname, lastname, birthdate, telefone, email, password):
        super().__init__()
        self._cedula_prof = cod_adn
        self._firstname = firstname
        self._lastname = lastname
        self._birthdate = birthdate
        self._telefone = telefone
        self._email = email
        self._password = password
        
        Admin.obj[cod_adn] = self
        Admin.lst.append(cod_adn)
    # Object properties
    # getter methodes
    # code property getter method
    @property
    def cod_adn(self):
        return self._cod_adn
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
    @cod_adn.setter
    def cod_adn(self,cod_adn):
        self._cod_adn = cod_adn
    @password.setter
    def password(self, password):
        self._password = password

    @staticmethod          
    def login(cod_adn,password):
       verify=False
       for d in Admin.lst:
           if str(password)==Admin.obj[d].password and str(cod_adn)==Admin.obj[d].cod_adn:
               verify=True
               d_code = Admin.obj[d].cod_adn
               return d_code
       if not verify:
           print("User not found!")
           return None
       
    @staticmethod
    def get_admin_names():
        return [Admin.obj[cod_adn].firstname + " " + Admin.obj[cod_adn].lastname for cod_adn in Admin.lst]

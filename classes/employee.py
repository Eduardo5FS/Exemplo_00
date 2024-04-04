from classes.gclass import Gclass

class Employee(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    auto_number = 0
    nkey = 1
    att = ['_employee_id','_password']
    
    header = 'Employee'
    des = ['Employee ID','Password']
    # Constructor: Called when an object is instantiated
    def __init__(self, employee_id, password):
        super().__init__()
        self._employee_id = employee_id
        self._password = password
        
        Employee.obj[employee_id] = self
        Employee.lst.append(employee_id)
    # Object properties
    # getter methodes
    # code property getter method
    @property
    def employee_id(self):
        return self._employee_id
    # password property getter method
    @property
    def password(self):
        return self._login
    @employee_id.setter
    def employee_id(self,employee_id):
        self._employee_id = employee_id
    @password.setter
    def password(self, password):
        self._password = password

    def login(self, employee_id, password):
        if self._employee_id == employee_id and self._password == password:
            return True
        else:
            return False
    
    def view_appointments(self):
        return Appointment.get_all_appointments()

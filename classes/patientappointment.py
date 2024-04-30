#%% Class PatientAppointment
import datetime
from classes.patient import Patient
# Import the generic class
from classes.gclass import Gclass

class PatientAppointment(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    auto_number = 1 # = 1 in case of auto number on
    nkey = 1
    # class attributes, identifier attribute must be the first one on the list
    att = ['_code','_date','_id_patient']
    # Class header title
    header = 'Appointments'
    # field description for use in, for example, in input form
    des = ['Code','Date','Patient ID']
    # Constructor: Called when an object is instantiated
    def __init__(self, code, date, id_patient):
        super().__init__()
        # Uncomment in case of auto number on
        if code == 'None':
            codes = PatientAppointment.getatlist('_code')
            if codes == []:
                code = str(1)
            else:
                code = str(max(map(int,PatientAppointment.getatlist('_code'))) + 1)
        # Object attributes
        # Check the customer referential integrity
        if id_patient in Patient.lst:
            self._code = code
            self._date = datetime.date.fromisoformat(date)
            self._id_patient = id_patient
            # Add the new object to the Order list
            PatientAppointment.obj[code] = self
            PatientAppointment.lst.append(code)
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
    # customer property getter method
    @property
    def id_patient(self):
        return self._id_patient
    # customer property setter method
    @id_patient.setter
    def id_patient(self, id_patient):
        if id_patient in Patient.lst:
            self._id_patient = id_patient
        else:
            print('Patient ', id_patient, ' not found')    
            
    @classmethod
    def lucro_diario:   #ACABAR!
        

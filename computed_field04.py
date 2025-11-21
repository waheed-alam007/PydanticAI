# computed field such a field of pydantic model's in this user did not provide the values .infact you have to use  remaning fields to calculate the  compute_fields.

from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict
from pydantic import AnyUrl

# lets this is the pydantic modle now we want to add the another field BMI in this but we did not take from user because user have to calculate this  instead what we will do is and  user provided the values of hight and weight we will use this and dynamically calculate the BMI.so BMI field dynamically createing with the help of other fields .so we say this BMI field is computed field .
class Patient(BaseModel):
    name: str
    email: EmailStr
    linkedin_url: AnyUrl
    age: int
    weight: float  # kg
    Hight: float   # mtr
    married: bool
    allergies: list[str]
    contact_detail: Dict[str, str]

    # in this we have to create the BMI field but in this field we place in the decorator(@computed_field) and we use another decorator (@property)
    @computed_field()
    @property
    # now we make the method here below 
    def bmi(self) -> float:   # herr the our pydantic' models  we  met instance as input  and we tell him this particular method out ]put will be float.

        # now we use the formula of bmi when wight is kg and hight is mtr then this formula use 
        # use. 
        bmi = round(self.weight / (self.Hight ** 2), 2)  # this we have to write the round 2 decimal places .
        return bmi


def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.email)
    print('BMI', patient.bmi)
    print(patient.linkedin_url)
    print('updated')


patient_info = {
    'name': 'ali',
    'age': 22,
    'weight': 45.3,
    'Hight': 1.76,
    'married': True,
    'linkedin_url': 'http://linkedin.com/123',
    'email': 'alkahr@mcb.com',
    'allergies': ['Pollen', 'Dust'],
    'contact_detail': {'phone': '1234564'}
}  

patient1 = Patient(**patient_info)
update_patient_data(patient1)

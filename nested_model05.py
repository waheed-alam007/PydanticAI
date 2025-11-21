# in this when if you  have to use  in pydantic any one model use as a field in the  other model this is called nested  model
from pydantic import BaseModel


class Address(BaseModel):  #this is the address pydantic model
    city:str
    state:str
    pin:str

class Patient(BaseModel):     #in this patint model  inherient from the BaseModel.
    name:str
    gender:str
    age:int
                                  # below this procees is diffuclt if i need the pin then i  have to alot of time to get the pin actually addres in its self a complex data.so for to avoide this i have to create the another Address model and you can use this model as a field in the patient model as below address:Address.that is why why we called itt nestead model.
                                  # address:"hous no 34,stret 54,mansehra,abbottabad,123".
    address:Address     #here our address is the Address type .

# now we create the patient model pydantic object. but first we have to create for  the Aaddress model pydantic object 
address_dict={'city':'Mansehra','state':'Pakistan','pin':'1234'}
                                               # from this raw dictionary we create the object  of address pydantic model
address1=Address(**address_dict)               #this object address1 has the Address clas this  is use for unpack address_dict (**address_dic)                                  
  
    #  now make the patinet dictionary as below 
patient_dict={'name':'asad','gender':'male','age':23,'address':address1}    #address in dict we pass the valuse pydantic model object we have to create as address1 this will be pass here 

# now make the patient model's object then unpck it 
patient1=Patient(**patient_dict)
# now check in patient1 what has
print(patient1)
# if you want to print  the name ,adres and pin now you can do it easyley
print(patient1.name)
# You can access nested fields as you can access in the patient address and then in the address you access the city,and pin this is called nested model
print(patient1.address.city)
print(patient1.address.pin)
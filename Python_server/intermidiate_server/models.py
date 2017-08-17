from __init__ import db

#class phone(db.EmbeddedDocument):
#		macAddress = db.StringField(max_length = 255)
#		phoneNumber = db.StringField(max_length = 255)

class User(db.Document):
		firstName = db.StringField(max_length=255, required=True)
		lastName = db.StringField(max_length=255, required=True)
		email = db.StringField(max_length=255, required=True)
		physicalDisability = db.StringField(max_length=255)
		language = db.StringField(max_length = 255)
		phoneMacAddress = db.StringField(max_length = 255)
		phoneNumber = db.StringField(max_length = 255)

		
class Store(db.Document):
		physical_address = db.StringField(max_length=511, required=True)
		client_ip = db.StringField(max_length=255, required=True)
		latitudeMin = db.FloatField(required = True)
		latitudeMax = db.FloatField(required = True)
		longitudeMin = db.FloatField(required = True)
		longitudeMax = db.FloatField(required = True)

class RFID_Reader(db.Document):
		tagId = db.StringField(max_length=255, required=True)
		product = db.StringField(max_length=255, required=True)



class missing(db.Document):
		tagId = db.StringField(max_length=255, required=True)
		product = db.StringField(max_length=255, required=True)

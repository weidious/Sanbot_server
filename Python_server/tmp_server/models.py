from __init__ import db

#class phone(db.EmbeddedDocument):
#		macAddress = db.StringField(max_length = 255)
#		phoneNumber = db.StringField(max_length = 255)

class bot(db.Document):
		client_ip = db.StringField(max_length=255, required=True)

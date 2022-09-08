from main import db, User, Provision, bcrypt

db.drop_all()
db.create_all()

'''
Zugangsdaten:
User1 (Administrator): 
Benutzername: Max Mustermann
Passwort: 4CsCe7pAR2s

User2:
Benutzername: Tom Mustermann
Passwort: Er!8ez7Y2K

'''

pw1 = bcrypt.generate_password_hash("4CsCe7pAR2s").decode("utf-8")
pw2 = bcrypt.generate_password_hash("Er!8ez7Y2K").decode("utf-8")

user_1 = User(username="Max Mustermann", password=pw1, user_email="max.muster@gmail.com", is_admin=True)
user_2 = User(username="Tom Mustermann", password=pw2, user_email="tom.muster@gmail.com", is_admin=False)

prov_1 = Provision(user_id=1, value=100, client_name="phillip")
prov_2 = Provision(user_id=1, value=200, client_name="Tomas")
prov_3 = Provision(user_id=3, value=500, client_name="Timon")

db.session.add(user_1)
db.session.add(user_2)
db.session.add(prov_1)
db.session.add(prov_2)
db.session.add(prov_3)
db.session.commit()
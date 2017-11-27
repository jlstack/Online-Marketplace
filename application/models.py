from application import db

class Product(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(128), nullable=False)
    description = db.Column('description', db.TEXT, nullable=False)
    image_path = db.Column('image_path', db.String(128), nullable=True)
    quantity = db.Column('quantity', db.Integer, default=1)
    price = db.Column('price', db.FLOAT, default=0.0)
    
    def __init__(self, name, description, image_path='', quantity=1, price=0.0):
        self.name = name
        self.description = description
        self.image_path = image_path
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return str({'name':self.name, 'description':self.description, 'image_path': self.image_path, 'quantity': self.quantity, 'price': self.price})

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

class Image(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(128), nullable=False)
    image_path = db.Column('image_path', db.String(128), nullable=False) 
    display_number = db.Column('display_number', db.Integer, nullable=False)

    def __init__(self, name, image_path, display_number):
        self.name = name
        self.image_path = image_path
        self.display_number = display_number

    def __repr__(self):
        return str({'name': self.name, 'image_path': self.image_path, 'display_number': self.display_number})

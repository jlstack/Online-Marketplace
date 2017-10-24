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

from flask import Flask, request, render_template
import sys
import os
import base64

errors = []

try:
    from application import db
    from application.models import Product
    db.create_all()
except Exception as err:
    errors.append(err.message)

# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
def index():
    products = Product.query.order_by(Product.id.desc())
    return render_template('products.html', products=products)

@application.route('/dir')
def stuff():
    return str(dir(application))

@application.route('/add', methods=['GET', 'POST'])
def test():
    if str(request.method) == 'POST':
        try:     
	    vals = request.form.to_dict()
            file = request.files['image']
            ext = file.filename.rsplit('.', 1)[1].lower()
            if ext in ['png', 'jpg', 'jpeg']:
                filename = "/static/" + base64.urlsafe_b64encode(file.filename) + "." + ext
                file.save("." + filename)
	        product = Product(vals['name'], vals['description'], filename, int(vals['quantity']), float(vals['price']))
                db.session.add(product)
                db.session.commit()        
                db.session.close()
        except Exception as err:
            db.session.rollback()
    	    return err.message
    return render_template('add_product.html')

@application.route('/errors')
def get_errors():
    return str(errors)

@application.route('/ls')
def get_files():
    return str(os.listdir(os.path.dirname(os.path.realpath(__file__))))

@application.route('/pwd')
def get_pwd():
    return str(os.path.realpath(__file__))

@application.route('/db_dir')
def get_db_dir():
    return str(dir(db))

@application.route('/tables')
def get_tables():
    return str(db.metadata.sorted_tables)

@application.route('/products')
def get_products():
    products = Product.query.order_by(Product.id.desc())
    stuff = [x.name for x in products]
    return str(stuff)
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

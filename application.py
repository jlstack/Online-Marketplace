from flask import Flask, Response, session, flash, request, redirect, render_template, g
import sys
import os
import base64
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user 
import hashlib
from flask_openid import OpenID

errors = []

try:
    from application import db
    from application.models import Product, User, Image
    import yaml

    with open("db.yml") as db_file:
        db_entries = yaml.safe_load(db_file)

    db.create_all()
    for user in db_entries["users"]:    
        usr = User(user["username"], user["password_hash"])
        db.session.add(usr)
        db.session.commit()        

    for project in db_entries["projects"]:
	proj = Product(project["name"], project["description"], project["images"][0], 1, 0)
        db.session.add(proj)
        db.session.commit()        
        for i in range(1, len(project["images"])): 
            img = Image(project['name'], project["images"][i], i)
            db.session.add(img)
            db.session.commit()        
    db.session.close()
except Exception as err:
    errors.append(err.message)

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# config
application.config.update(
    DEBUG = True,
    SECRET_KEY = os.urandom(24) 
)

@application.route("/login", methods=["GET", "POST"])
def login():
    if str(request.method) == 'GET':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            redirect("/")
    username = request.form['username']
    password = request.form['password']
    password = hashlib.sha224(password.encode('utf-8')).hexdigest()        
    user = User.query.filter_by(username=username, password=password).first() 
    if user is not None:
        session['logged_in'] = True
        return redirect("/") 
    return redirect("/login")

@application.route("/logout")
def logout():
    session['logged_in'] = False 
    return redirect('/') 

@application.route('/')
def index():
    return render_template('home.html')

@application.route('/gallery')
def gallery():
    products = Product.query.order_by(Product.id.asc())
    return render_template('products.html', products=products)

@application.route('/about')
def about():
    return render_template('about.html')

@application.route('/contact')
def contact():
    return render_template('contact.html')

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@application.route('/dir')
def stuff():
    return str(dir(Product.id))

@application.route('/add', methods=['GET', 'POST'])
def add():
    if not session.get('logged_in'):
        return render_template('login.html')
    if str(request.method) == 'POST':
        try:     
	    vals = request.form.to_dict()
            files = request.files.getlist("image")
            for i in range(0, len(files)):
                file = files[i]
                ext = file.filename.rsplit('.', 1)[1].lower()
                if ext in ['png', 'jpg', 'jpeg']:
                    filename = "/static/images/" + base64.urlsafe_b64encode(file.filename) + "." + ext
                    file.save("." + filename)
                    if i == 0:
	                product = Product(vals['name'], vals['description'], filename, 1, 0)
                        db.session.add(product)
                        db.session.commit()        
                        db.session.close()
                    else:
                        img = Image(vals['name'], filename, i)
                        db.session.add(img)
                        db.session.commit()        
                        db.session.close()
        except Exception as err:
            db.session.rollback()
    	    return err.message
    return render_template('add_product.html')

@application.route('/errors')
def get_errors():
    return str(errors)

@application.route('/products')
def get_products():
    products = Product.query.order_by(Product.id.desc())
    stuff = [x.name for x in products]
    return str(stuff)

@application.route('/pin/<pin_id>')
def pin_enlarge(pin_id):
    p = Product.query.filter_by(id=pin_id).first()
    images = Image.query.filter_by(name=p.name).order_by(Image.display_number.desc())
    return render_template('pin_focus.html', p=p, images=images)

@application.route('/delete/<pin_id>')
def delete(pin_id):
    Product.query.filter_by(id = pin_id).delete()
    db.session.commit()        
    db.session.close()
    return redirect("/gallery")

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

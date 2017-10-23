from flask import Flask, render_template
import sys
import os


errors = []

try:
    from application import db
except Exception as err:
    errors.append(err.message)

# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
def index():
    return '<h1>Hello World</h1>'

@application.route('/dir')
def stuff():
    return str(dir(application))

@application.route('/add')
def test():
    return render_template('upload_form.html')

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

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

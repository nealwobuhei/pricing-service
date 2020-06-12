from flask import Flask, render_template
from views.alerts import alert_blueprint
from views.stores import store_blueprint
from views.users import user_blueprint
import os
from libs.mailgun import Mailgun

app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)  # flask automatically load the '.env' file, and it will populate 'os.environ' for environment
# you can get any value that is in your '.env' file--with .get

@app.route('/')
def home():
    return render_template('home.html')


app.register_blueprint(alert_blueprint, url_prefix='/alerts')  # gonna make this /items/, '/' is in items blueprint
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")

if __name__ == '__main__':
    app.run(debug=True)  # adding debug, since in case is going to give more info when have problems

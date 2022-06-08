from flask import *
import pandas as pd
from flask_cors import CORS

from flask_mail import Mail, Message


from query_api.articolo_superato.api_articolosuperato import articolo_superato


#from Controllers.ticketController import getTicket as database
from query_articoli import Articoli
from query_api.api_aumenti import api_aumenti
from query_api.api_newsletter import api_newsletter
from query_api.api_magazzino import api_magazzino
from query_api.dashboard.api_agenti import api_dash_agente
from query_api.api_kit import api_gen_kit
from query_api.campioni.api_campioni import api_campioni
from query_api.api_info_articolo import info_articolo
from query_api.api_utenti import utenti
from query_api.api_listini_promozionali import listini_promozionali
from query_api.api_lavorazione import lavorazione
global mail

app = Flask(__name__,
            static_url_path='',
            static_folder='../client',
            template_folder='../client')


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# CONFIGURO SMTP EMAIL
app.config['MAIL_SERVER'] = 'smtps.aruba.it'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sistemi@micromic.com'
app.config['MAIL_PASSWORD'] = 'Micromic$2021'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
# REGISTRO LE API
app.register_blueprint(articolo_superato, url_prefix='/tools/articolo_superato/')
app.register_blueprint(api_aumenti, url_prefix='/tools/aumenti/')
app.register_blueprint(api_newsletter, url_prefix='/tools/newsletter/')
app.register_blueprint(api_magazzino, url_prefix='/tools/statomagazzino/')
app.register_blueprint(api_dash_agente, url_prefix='/dashboard/agenti/')
app.register_blueprint(api_gen_kit, url_prefix='/tools/kit/')
app.register_blueprint(api_campioni, url_prefix='/tools/campioni/')
app.register_blueprint(info_articolo, url_prefix='/tools/info_articolo/')
app.register_blueprint(utenti, url_prefix='/utenti/')
app.register_blueprint(listini_promozionali, url_prefix='/listini_promozionali/')
app.register_blueprint(lavorazione, url_prefix='/officina/lavorazione/')


CORS(app)


def try_login(username):
    try:
        import pymongo
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Portals"]
        mycol = mydb["db_login"]
        x = mycol.find_one({'username': username})
        return x
    except:
        return {}


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if session['logged'] == True:
            return render_template('index.html')
        else:
            return redirect(url_for('logout'))
    except:
        return redirect(url_for('logout'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            import time
            rlogin = str(request.form.get("login"))
            rpassword = str(request.form.get("password"))
            test_login = try_login(rlogin)
            if rpassword != test_login['psw']:
                return redirect(url_for('logout'))
            else:
                session['logged'] = True
                del test_login['psw']
                del test_login['_id']
                session['info'] = test_login
                return redirect(url_for('index'))
        if request.method == 'GET':
            return render_template("component/login/login.html")
    except:
        return redirect(url_for('logout'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        session['logged'] = False
        return render_template("component/login/login.html")


@app.route('/login_service', methods=['GET'])
def loginservices():
    try:
        if session['logged'] == True:
            """ q = {'id_agente': int(session.get('id_agente')), 'username': session.get(
                 'username'), 'role': session.get('role'), 'budget': session.get('budget')}"""
            q = session.get('info')
            print(q)
            return jsonify(q)
    except:
        return redirect(url_for('logout'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555, use_reloader=True)

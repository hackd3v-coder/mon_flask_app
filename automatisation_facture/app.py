from flask import Flask, render_template,request,session, redirect,url_for
from sqlite3 import *
from datetime import datetime
from num2words import num2words

app = Flask("__name__")
app.secret_key = 'cle secret'
app.jinja_env.filters['num_to_words'] = lambda n: num2words(n ,lang='fr')
@app.template_filter('thousands')
def thousands(nombre):
     montant = " ".join(nombre[i:i+3] for i in range(0, len(nombre), 3))
     return montant

@app.route('/')
def index():
     return render_template('index.html')
@app.route('/connection', methods = ['POST','GET'])
def connection():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        session['email'] = email
        conn = connect('ingenierie_services.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM user WHERE email=? AND password=?""",(email,password))
        user = cursor.fetchone()
        conn.close()
        if user :
            return redirect(url_for('insersion'))
        else :
            return render_template('connection.html',erreur = 'Email ou mot de passe incorrect')
    return render_template('connection.html',erreur = '')

@app.route('/insersion',methods= ['POST','GET'])
def insersion() :
        if "email" not  in session  :
             return redirect(url_for('connection'))
        if request.method == "POST":
             da = request.form.get('distributeur')
             mois =request.form.get('mois')
             montant_ttc = request.form.get('montant_ttc')
             montant_ht = request.form.get('montant_ht')
             retenue_tva = request.form.get('retenue_tva')
             retenue_40 =request.form.get('retenue_40')
             net_a_payer = request.form.get('net_a_payer')
             date = datetime.now()
             date = date.strftime("%d/%m/%Y")
             conn = connect('ingenierie_services.db')
             cursor = conn.cursor()
             cursor.execute("""INSERT INTO facture VALUES (?,?,?,?,?,?,?,?,?)""",(None,da,mois,montant_ttc,montant_ht,retenue_tva,retenue_40,net_a_payer,date))
             conn.commit()
             conn.close()
             session['insersion'] = {
                  'da' : da ,
                  'mois' : mois,
                  'montant_ttc' : montant_ttc,
                  'montant_ht' : montant_ht ,
                  'retenue_tva' : retenue_tva ,
                  'retenue_40' : retenue_40 ,
                  'net_a_payer' : net_a_payer,
                  'date' : date

             }
             return redirect(url_for('facture'))

        return render_template('insersion.html')

@app.route('/facture')
def facture() :
    if session.get('insersion') :
        return render_template('facture.html', donnees = session['insersion'])
    return redirect(url_for('insersion'))



if __name__ == "__main__":
    app.run()
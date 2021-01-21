from flask import Flask
from flask import request
from flask import render_template
import os
import dga

app = Flask(__name__)

@app.route('/')
def hello_world():

    return render_template('hello.html')




@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        domain = request.form['dname']
        ip = request.form['ip']
        #print domain,ip

        f = open('maradns/db.lan.txt','a')
        f.write('\n'+domain+'. '+ip+' ~')
        f.close()

        #os.system('start cmd /c ,maradns/run_maradns.bat')
        
    
    return render_template('success.html')



@app.route('/generateDateDGA', methods=['GET', 'POST'])
def generate():

    if request.method == 'POST':
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['date'])
        #hour = int(request.form['hour'])
        #minute = int(request.form['minute'])

        domain = dga.date_dga(year,month,day)
        return render_template('hello.html',domain=domain)



@app.route('/generateTwitterDGA', methods=['GET', 'POST'])
def generateTwitter():

    if request.method == 'POST':
        catg = request.form['category']

        domain = dga.twitter_dga(catg)
        return render_template('hello.html',domain=domain)


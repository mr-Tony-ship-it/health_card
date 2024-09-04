from flask import *
from flask import Blueprint
from database import *
import os
from werkzeug.utils import secure_filename
public = Blueprint('public',__name__)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
#if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@public.route('/register1',methods=['GET','POST'])
def register1():
    if 'submit' in request.form:
        name=request.form['name']
        email=request.form['email']
        phno=request.form['phno']
        dob=request.form['dob']
        gen=request.form['gen']
        password=request.form['password']
        if 'img' not in request.files:
            return "No file part", 400 
    file = request.files.get('img')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        qry4="insert into register values(null,'%s','%s','%s','%s','%s','%s',CURRENT_TIMESTAMP)"%(name,gen,email,dob,phno,password)
        res=insert(qry4)
        if res>0:
            return render_template('login.html')
    return render_template('register1.html')

@public.route('/login',methods=['GET','POST'])
def login():
    if 'submit' in request.form:
        username=request.form['username']
        password=request.form['password']
        qry="select * from register where email='%s' AND pass='%s'"%(username,password)
        n=select(qry)
        if n:
            session['id']= n[0]['id']
            session['name']= n[0]['name']
            session['email']= n[0]['email']
            session['phno']= n[0]['phno']
    # Access values by column names
            qry="insert into login values(null,'%s','%s',CURRENT_TIMESTAMP)"%(username,password)
            log_f=1
            insert(qry)
            return render_template('welcome.html',name=session['name'],id=session['id'])
        else:
            return "No username provided"
    return render_template('login.html')


@public.route('/demo')
def demo():
    return render_template('demo.html')

@public.route('/welcome',methods=['GET','POST'])
def welcome():
    id=session['id']
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Insert image path into database
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        qry="update register set where id=%s"%(id)
        update(qry)
    return render_template('welcome.html')
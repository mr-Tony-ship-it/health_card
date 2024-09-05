from flask import *
from flask import Blueprint
from database import *
import os
from werkzeug.utils import secure_filename
from fpdf import FPDF
import random
import string
import matplotlib.pyplot as plt
import mysql.connector
from bs4 import BeautifulSoup
import requests
import io,base64
from flask import Flask, request, send_file,render_template,jsonify
import pandas as pd
from pandas import DataFrame

public = Blueprint('public',__name__)
app = Flask(__name__)

# Database connection settings
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'healthcard'

# Create a MySQL connection
cnx = mysql.connector.connect(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME
)
cursor = cnx.cursor()

app.config['UPLOAD_FOLDER'] = 'static/uploads/'

@public.route('/admin')
def admins():
    df = pd.read_sql_query("SELECT * FROM users", cnx)

    # Count the number of patients in each category
    category_counts = df['blood_type'].value_counts()

    # Generate the pie chart
    fig, ax = plt.subplots()
    ax.pie(category_counts.values, 
           labels=category_counts.index, 
           autopct='%1.1f%%', 
           startangle=90)
    ax.axis('equal') 
    plt.title('Patient Categories')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image in base64
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    dm = pd.read_sql_query("SELECT * FROM user1", cnx)

    # Count the number of patients in each category
    category_counts = dm['type'].value_counts()

    # Generate the pie chart
    fig, ax = plt.subplots()
    ax.pie(category_counts.values, 
           labels=category_counts.index, 
           autopct='%1.1f%%', 
           startangle=90)
    ax.axis('equal') 
    plt.title('Patient diseses')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image in base64
    plot_url1 = base64.b64encode(img.getvalue()).decode()

    # Render the HTML template with the embedded image
    return render_template("admin.html",plot_url=plot_url,plot_url1=plot_url1)


app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif','pdf','txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@public.route('/upload', methods=['POST', 'GET'])
def upload_file():
    app.config['UPLOAD_FOLDER'] = '/static/upload'
    if request.method == 'POST':
        file = request.files.get('file')  # Use the correct key
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Insert data into database using parameterized query or prepared statement
            db.execute("INSERT INTO register (blood_test, scan_report, other_report) VALUES (?, ?, ?)", blood_test, scan_report, other_report)
            if True:
                return "success"
    return render_template("upload.html")

sql="select * from users"

cursor.execute(sql)
df = DataFrame(cursor.fetchall())

@public.route('/user_view')
def view():
    return render_template('view.html',view=df.to_html())


@public.route('/register1',methods=['GET','POST'])
def register1():
    if 'submit' in request.form:
        name=request.form['name']
        email=request.form['email']
        phno=request.form['phno']
        dob=request.form['dob']
        gen=request.form['gen']
        password=request.form['password']

        qry4="insert into register values(null,'%s','%s','%s','%s','%s','%s',CURRENT_TIMESTAMP)"%(name,gen,email,dob,phno,password)
        res=insert(qry4)
        qry="select * from card where username='%s'"%(email)
        unique_ser=select(qry)
        if res>0:
            return render_template('login.html')
        else:
            return "Registration Unsucessfull"
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
            insert(qry)
            return render_template('welcome.html',name=session['name'],id=session['id'])
        else:
            return "No username provided"
    return render_template('login.html')


@public.route('/welcome',methods=['GET','POST'])
def welcome():
    id=session['id']
        # Insert image path into database
    qry="select * from register where email='%s'"%(session['email'])
    patient_data=select(qry)
    if patient_data:
        pdf_file = create_health_card_pdf(patient_data)
        print(f"Health card PDF created: {pdf_file}")
    else:
        print("No data found for the specified patient.")
        
    return render_template('welcome.html',name=session['name'])

@public.route('/card',methods=['GET','POST'])
def create_health_card_pdf():
    qry="select * from register where email='%s'"%(session['email'])
    patient_data=select(qry)
    # Unpack the patient data
    qry="select * from card where username='%s'"%(session['email'])
    unique_ser=select(qry)
    session['id']= patient_data[0]['id']
    name= patient_data[0]['name']
    dob= patient_data[0]['dob']
    gen= patient_data[0]['gen']
    date= patient_data[0]['date']
    formatted_date = date.strftime('%B %d, %Y')
    
    if not unique_ser:
        prefixes = ["A", "B", "C", "D", "E", "F", "M", "N"]
        suffixes = ["X", "Y", "Z", "G", "H", "I","J", "L","K"]
    
    # Randomly select a prefix and suffix
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        postfix = random.choice(suffixes) 
    
    # Generate the numeric part
        numeric_part = ''.join(random.choices(string.digits, k=5))
        numeric = ''.join(random.choices(string.digits, k=2))
    
    # Combine to form the unique ID
        unique_id = f"{prefix}{numeric_part}{postfix}{numeric}{suffix}"
    # Create instance of FPDF class
        pdf = FPDF()
    
    # Add a page
        pdf.add_page()
    
    # Set title font and size
        pdf.set_font("Arial", size=14)
    
    # Add title
        pdf.cell(200, 10, txt="Health Card", ln=True, align="C")
    
    # Add a line break
        pdf.ln(10)
    
    # Set the font for the rest of the text
        pdf.set_font("Arial", size=12)
    
    # Add the patient's details
        pdf.cell(200, 10, txt=f"CardID: {unique_id}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Name of Patient: {name}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Date of Birth: {dob}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Gender: {gen}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Issued On: {formatted_date}", ln=True, align="L")
    
    
    # Save the PDF with a unique name
        pdf_name = f"health_card_{unique_id}.pdf"
        pdf_output = os.path.join(app.config['UPLOAD_FOLDER'],pdf_name)
        pdf.output(pdf_output)
    # download(pdf_output)
    
        qry="insert into card values(null,'%s','%s','%s')"%(session['email'],unique_id,pdf_output)
        insert(qry)
    else:
        pdf_output=unique_ser[0]['loca']
    qry="select * from card where username='%s'"%(session['email'])
    unique_ser=select(qry)
    session['cardID']=unique_ser[0]['CardID']
    return render_template('card.html',name=session['name'],pdf_output=pdf_output,patient_data=patient_data[0],unique_ser=unique_ser[0])

# Create the health card 


def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

@app.route('/download/<filename>')
def download(filename):
    # Construct the path to the file
    file_path = os.path.join('static', 'uploads', filename)
    # Serve the file for download
    return send_file(file_path, as_attachment=True)




@public.route('/')
def demo():
    return render_template('index.html')


@public.route('/d_register',methods=['GET','POST'])
def d_home():
    if 'submit' in request.form:
        name=request.form['name']
        special=request.form['specialization']
        ln=request.form['license_number']
        cn=request.form['contact_number']
        pas=request.form['password']


        qry4="insert into doc_reg values(null,'%s','%s','%s','%s','%s')"%(name,special,ln,cn,pas)
        res=insert(qry4)
        if res>0:
            return render_template('login.html')
    return render_template('doctor.html')

@public.route('/d_login',methods=['GET','POST'])
def d_login():
    if 'login' in request.form:
        ln=request.form['license_number']
        pas=request.form['password']
        qry="select * from ar where  user='%s' AND pass='%s'"%(ln,pas)
        n=select(qry)
        if n:
            session['doc']=ln
            return render_template('d_welcome.html',doc=session['doc'])
        else:
            return "error in login"
    return render_template('d_login.html')

@public.route('/d_welcome')
def d_welcome():
    # qry="select * from ar where user='%s'"%()
    # unique_ser=select(qry)
    # unique=unique_ser[0]['user']
    

    # Render the HTML template with the embedded image
    return render_template('d_welcome.html')

@public.route('/d_view')
def d_view():
    qry="select * from register"
    unique_ser=select(qry)
    return render_template('d_view.html',unique_ser=unique_ser)

@public.route('/h_login',methods=['GET','POST'])
def h_login():
    if 'login' in request.form:
        ln=request.form['license_number']
        pas=request.form['password']
        qry="select * from ar where user='%s' AND pass='%s'"%(ln,pas)
        n=select(qry)
        if n:
            return render_template('admin.html')
        else:
            return "error in login"
    return render_template('h_login.html')

@public.route('/status')
def display_pie_chart():
    # Connect to the database (replace 'your_database.db' with your actual file)

    # Read the data into a pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM users", cnx)

    # Count the number of patients in each category
    category_counts = df['blood_type'].value_counts()

    # Generate the pie chart
    fig, ax = plt.subplots()
    ax.pie(category_counts.values, 
           labels=category_counts.index, 
           autopct='%1.1f%%', 
           startangle=90)
    ax.axis('equal') 
    plt.title('Patient Categories')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image in base64
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    dm = pd.read_sql_query("SELECT * FROM user1", cnx)

    # Count the number of patients in each category
    category_counts = dm['type'].value_counts()

    # Generate the pie chart
    fig, ax = plt.subplots()
    ax.pie(category_counts.values, 
           labels=category_counts.index, 
           autopct='%1.1f%%', 
           startangle=90)
    ax.axis('equal') 
    plt.title('Patient diseses')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image in base64
    plot_url1 = base64.b64encode(img.getvalue()).decode()

    # Render the HTML template with the embedded image
    return render_template('status.html', plot_url=plot_url,plot_url1=plot_url1)


url = "https://www.healthline.com/nutrition/healthy-tips"

# Function to scrape health-related tips
def scrape_tips():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tips = []
    for tip in soup.find_all('div', class_='tip'):
        title = tip.find('h3', class_='tip-title').text.strip()
        description = tip.find('p', class_='tip-description').text.strip()
        tips.append({'title': title, 'description': description})
    return tips

# Route to handle GET requests
@public.route('/tips', methods=['GET'])
def get_tips():
    tips = scrape_tips()
    return jsonify({'tips': tips})


@public.route('/tretmentHistory')
def tretmentHistory():
    selected_test1= request.form.get('test1')
    selected_test2 = request.form.get('test2')
    selected_test3 = request.form.get('test3')
    selected_test4 = request.form.get('test4')
    selected_test5 = request.form.get('test5')
    file = request.files['img1']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Insert image path into database
        image_path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file = request.files['img2']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Insert image path into database
        image_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file = request.files['img3']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Insert image path into database
        image_path3 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file = request.files['img4']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Insert image path into database
        image_path4= os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file = request.files['img5']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Insert image path into database
        image_path5 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    qry="insert into reports values(null,'%s','%s','%s','%s','%s','%s')"%(image_path1,image_path2,image_path3,image_path4,image_path5)
    insert(qry)
    return render_template('tretmentHistory.html',cardID=session['cardID'])
from flask import Flask, redirect, url_for, render_template, request, send_file
import flask_excel as excel
# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index():
   return render_template("index.html")
   
@app.route('/dashboard', methods = ['POST', 'GET'])
def verify():
    if request.method == 'POST':
       return render_template("dashboard.html")
    else:
       return render_template("dashboard.html")
    
@app.route('/add_admin')
def add_admin():
    return render_template("add_admin.html")
   
@app.route('/add_bulk_data_form')
def add_bulk_data_form():
    return render_template("add_bulk_data_form.html")
     
@app.route('/add_single_data_form')
def add_single_data_form():
    return render_template("add_single_data_form.html")

@app.route('/edit_dr')
def edit_dr():
    return render_template("edit_dr.html")

@app.route('/edit_msr')
def edit_msr():
    return render_template("edit_msr.html")

@app.route('/list_admin')
def list_admin():
    return render_template("list_admin.html")

@app.route('/edit_admin')
def edit_admin():
    return render_template("edit_admin.html")

@app.route('/add_org')
def add_org():
    return render_template("add_org.html")

@app.route('/list_org')
def list_org():
    return render_template("list_org.html")    

@app.route('/edit_org')
def edit_org():
    return render_template("edit_org.html") 

@app.route('/download_dr')
def download_dr():
    p = "Upload Consultant Data.xlsx"
    return send_file(p, as_attachment=True)

@app.route('/download_msr')
def download_msr():
    p = "Upload MSR Data.xlsx"
    return send_file(p, as_attachment=True)

@app.route('/add_pro')
def add_pro():
    return render_template("add_pro.html") 

@app.route('/list_pro')
def list_pro():
    return render_template("list_pro.html") 

@app.route('/edit_pro')
def edit_pro():
    return render_template("edit_pro.html")


if __name__ == '__main__':
    app.run(debug = True)
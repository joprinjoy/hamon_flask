from flask import Flask,render_template,request,redirect,url_for,session,flash,make_response
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = 'qwerty'
users = {}
error_statement = "hi"
users.update({'joprin@gmail.com':'admin','swarag@gmail.com':'user','christo@gmail.com':'christo'})

#route to 
@app.route("/")
def home_page():
     return render_template("index.html")

@app.route("/login_form",methods = ['POST','GET'])
def login_form():
    return render_template("login_form.html") 

@app.route("/login",methods = ['POST','GET'])   
def login():
        
        if request.method == 'POST':
            uname = request.form['uname']
            password = request.form['password']
            for item in users:
                if item in uname:
                    usname = item
                    pswd = users[item]
            # usname = request.cookies.get('username')
            # pswd = request.cookies.get('password')    

            if uname == usname and password == pswd:
                    session['user'] = uname
                    print(session['user'])
                    
                    return render_template('welcome.html')  
            else:
                 error_statement="invalid credentials"
                 #return render_template('error.html',es=error_statement)
                 flash(error_statement)
                 return redirect(url_for('login_form'))
            

@app.route("/register_form")
def register_form():
     app.logger.debug("Register form executed")
     return render_template('register.html')


@app.route('/register',methods = ['POST'])
def register():
     #saving the form input
     uname = request.form['uname']
     passwd = request.form['password']
     
     if uname :
          app.logger.debug(f"username found:{uname}")
     
     if passwd :
          app.logger.debug(f" password found{passwd}")
     #saving the file from form to folder uploads
     pic = request.files['file']
     pic.save(f"/home/joprin/flask_project/uploads/{secure_filename(pic.filename)}")
     users.update({uname:passwd})
     return render_template('register.html')

#cookie usage is commented as login informations are currently handled with dict
    #  resp = make_response(render_template('register.html'))
    #  resp.set_cookie('username',uname)
    #  resp.set_cookie('password',passwd)

    #  return resp


@app.route('/logout')
def logout():
    for key in session:
        session.pop(key,None)
    return render_template('/')
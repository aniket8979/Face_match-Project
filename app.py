from flask import Flask, render_template, request,redirect
import face_recognition
import os
from flask import url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)


# This function image handle file, uploaded from html page
uploaded_image = []

#This Upload file location code will be improved with the use of OS Module 

UPLOAD_FOLDER = 'D:\Education\Code\Mini_project\static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["IMAGE_UPLOADS"] = "D:\Education\Code\Mini_project\static"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG","JPG","JPEG"]

@app.route('/upload.html', methods = ["GET","POST"])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        #######
        file = request.files['file']
        
        #I want this file.filename and a variable in global availaibility
        a = file.filename
        uploaded_image.append(a)


        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
      
        filename = secure_filename(file.filename)
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template("upload.html", filename = filename)
    return render_template('upload.html')

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename = filename), code=301)



# This function handles facial feature
matched = []
def face_match():
    path = 'Faces/Male'
    images = os.listdir(path)    
    print(uploaded_image[0])
    print('My name is anthony')

    for img in images:
    
        user = face_recognition.load_image_file('D:\Education\Code\Mini_project\static\{}' .format(uploaded_image[0]))
        match = face_recognition.load_image_file('Faces/Male/{}' .format(img))


        user_encoding = face_recognition.face_encodings(user)[0]
        match_encoding = face_recognition.face_encodings(match)[0]
    
        result = face_recognition.face_distance([user_encoding], match_encoding)

        res_val = round(result[0],4)

        if res_val <= 0.9000:
            print('Its a match' , img )
            i = img
            matched.append(i)



            

# Registeration is using TXT file for storing username & password.
# Flask get post method not working. Due to some BUG
@app.route('/register.html') #, methods = ['GET','POST'])
def register():
    '''username = input()
    password = input()
    username = ('\n'+username)
    a = ','
    detail = (username+a+password)
    file = open('login.txt','a+')
    file.write(detail)
    file.close'''

    return render_template('register.html')


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/front.html')
def search():
    face_match()
    return render_template('front.html', lady = uploaded_image[0], m1 = matched[0], m2 = matched[1])



# Login Logic is working properly but Flask Get Post method not working
# have to resolve some BUG in GET POST Method.

@app.route('/login.html', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        user1 = request.form['username']
        pass1 = request.form['password']
        pass1 = pass1.rstrip()
        user1 = user1.rstrip()
        file = open('login.txt','r')
        login_info= {}
        a = 'Login Successful'
        b = 'Wrong Password'
        c = 'wrong Username'
        for line in file:
            name,passcode = line.split(',')
        #Dictionary declared, and Username & password stored in dictionary form 
        #so that password can be idetified with username
            login_info[name] = passcode
            if user1 in login_info.keys():
                if login_info[name] == pass1:
                    print(a)
                    return render_template('upload.html', a1 = a)
                else:
                    print(b)
                    return render_template('upload.html', b1 = b)
            else:
                print(c)
                return render_template('upload.html', c1 = c)
    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)
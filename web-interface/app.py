from flask import Flask,render_template,request
import subprocess
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zero_sen import sen_class,completeness
from category import category_predict
from translating import translation_result

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///feedback.db"
app.config['UPLOAD_FOLDER'] = 'uploads/'
db=SQLAlchemy(app)

def run_scripts():
    try:
        # Run Node.js translation script
        subprocess.run(['node', 'translating.js'], check=True)

        # Run Python read script
        result = subprocess.run(['python3', 'translating.py'], check=True, capture_output=True, text=True)

        # Return the result of the final script
        return print("written")

    except subprocess.CalledProcessError as e:
        return print("failure")    
class fb(db.Model): #fb is table
    sno=db.Column(db.Integer,primary_key=True)
    message=db.Column(db.String(200),nullable=False)
    message_en=db.Column(db.String(200),nullable=False)
    category=db.Column(db.String(100),nullable=False)
    complete=db.Column(db.Integer,nullable=False)
    sentiment=db.Column(db.Integer,nullable=False)
    image = db.Column(db.LargeBinary) 
    date=db.Column(db.DateTime,default=datetime.now)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit',methods=['POST'])
def submit():
    msg=request.form['ta']
    # export_message.py
    # Save the message to a file
    with open('message.txt', 'w',encoding='utf-8') as file:
        file.write(msg)
    print("Message exported to message.txt")
    run_scripts()
    msg_en=translation_result() 
    comp=completeness(msg_en)
    sen_c=sen_class(msg_en)
    print(msg,sen_c,comp) 
    categ=category_predict([msg_en]).lower()
    image = request.files.get('image')
    image_data = None
    if image:
        image_data = image.read()
    with app.app_context():
         db.create_all()
         fb_obj=fb(message=msg,category=categ,sentiment=sen_c,complete=comp,message_en=msg_en,image=image_data)
         db.session.add(fb_obj)
         db.session.commit()
    return render_template('submit.html')





def __repr__(self)->str:
    return f"{self.sno}-{self.msg}"

if __name__=="__main__":
    app.run(debug=True)
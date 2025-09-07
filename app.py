from email.policy import default
from flask import Flask , render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///flask2.db"
db=SQLAlchemy(app)



class flask2(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=flask2(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
       
    alltodo=flask2.query.all()
    return render_template('index.html',alltodo=alltodo)


@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=flask2.query.get(sno)
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    
    
    todo=flask2.query.get(sno)
    return render_template('update.html',todo=todo)
    
    
    
@app.route('/delete/<int:sno>')    
def delete(sno):
    todo=flask2.query.get(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
  



if  __name__ =='__main__':
    app.run(debug=True,port=8000)
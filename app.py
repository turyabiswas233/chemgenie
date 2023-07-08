from flask import Flask, render_template, request, redirect, g, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']= False
db=SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=True)
    date=db.Column(db.String(500), nullable=True)
    schedule=db.Column(db.String(500), nullable=True)
    
    def __repr__(self) -> str:
        return

@app.route("/abs-login",methods=['POST','GET'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        
        if request.form['password']=='12345678' and request.form['username']=='abs-admin' :
            session['user'] = request.form['username'] 
            return redirect("/abs-admin")
        
    return render_template('login.html') 
            


@app.route("/abs-admin",methods=['POST','GET'])
def admin():
    if g.user:
        if request.method=='POST':
            todo = Todo(title=request.form['title'],date=request.form['date'],schedule=request.form['schedule'])                                                                                                                            
            db.session.add(todo)
            db.session.commit()
            
        allTodo = Todo.query.all()                                                                                           
        return render_template('admin.html',allTodo=allTodo)


@app.route("/delete/<int:sno>")
def delete(sno):
    if g.user:
        todo = Todo.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect("/abs-admin")



@app.route("/update/<int:sno>", methods=['POST','GET'])
def update(sno):
    if g.user:
        if request.method=='POST':
            title=request.form['title']
            date= request.form['date']
            schedule= request.form['schedule']
            todo = Todo.query.filter_by(sno=sno).first()     
            todo.title=title
            todo.date=date 
            todo.schedule=schedule                                                                                                                      
            db.session.add(todo)
            db.session.commit()
            return redirect('/abs-admin')
        
        todo = Todo.query.filter_by(sno=sno).first()
        return render_template('update.html',todo=todo)


@app.route("/")
def hello_world():
    allTodo = Todo.query.all() 
    return render_template('index.html',allTodo=allTodo)


@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/about")
def about():
    return render_template('about.html')


@app.before_request
def before_request():
    g.user = None
    
    if 'user' in session:
        g.user = session['user']

@app.route("/dropsession")
def dropsession():
    session.pop('user',None)
    return render_template('login.html')



if __name__=="__main__":
    app.run(debug=True)
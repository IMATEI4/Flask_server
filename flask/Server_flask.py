from flask import Flask, request, render_template
import mysql.connector
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,template_folder='Templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Newuser:Mateisky5!@localhost/testDB'
db = SQLAlchemy(app)

class books(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year_of_aparition = db.Column(db.Integer())
    rating = db.Column(db.Integer())

    def __init__(self, id, name, author, year_of_aparition, rating):
        self.id = id
        self.name = name
        self.author = author
        self.year_of_aparition = year_of_aparition
        self.rating = rating

@app.route("/", methods = ["GET"])
def index():
    a = books.query.all()
    return render_template('index.html', acc = a)

@app.route("/insert", methods = ["GET","POST"])
def insert():
    if(request.method == "POST"):
        newbook = books(id = request.form['ID'], name = request.form['nume'], author = request.form['author'], year_of_aparition = request.form['year_of_aparition'], rating= request.form['rating'])
        db.session.add(newbook)
        db.session.commit()
        books.query.all()
        return render_template('return.html')
    else:
        return render_template('Add.html')

@app.route("/<id>/delete", methods = ["GET"])
def delete(id):
    if (request.method == "GET"):
        book = books.query.filter_by(id = id).first()
        db.session.delete(book)
        db.session.commit()
        books.query.all()
        return render_template('return.html')
    
@app.route("/<id>/update", methods = ["GET","POST"])
def update(id):
    if(request.method == "POST"):
        new_book = books.query.filter_by(id = id).first()
        new_book.name = request.form['nume']
        new_book.author = request.form['author']
        new_book.year_of_aparition = request.form['year_of_aparition']
        new_book.rating = request.form['rating']
        db.session.commit()
        books.query.all()
        return render_template('return.html')
    else:
        a = books.query.filter_by(id = id)
        return render_template('Update.html', acc = a)

if __name__ == "__main__":
    app.run(debug = True,host = "localhost", port = 8300)

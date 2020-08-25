import flask
from flask import request, jsonify, render_template, flash, url_for, redirect
import sqlite3, json
import bookclass
from forms import BookForm
from config import Config

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/index', methods=['GET'])
def index():
    conn = sqlite3.connect('bookdata')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM BooksTable;').fetchall()
    conn.close()

    return render_template('booksweb.html', all_books = all_books) 

@app.route('/newbook', methods=['GET', 'POST'])
def bookform():
    form = BookForm()
    if form.validate_on_submit():
        # flash('Book Saved (author - {}, title{}'.format(
        #     form.author.data, form.title.data))
        conn = sqlite3.connect('bookdata')
        cur = conn.cursor()
        all_books = cur.execute('SELECT * FROM BooksTable;').fetchall()
        book_dict = {
            'Author' : form.author.data,
            'Title'  : form.title.data,
            'Rating' : int(form.rating.data), 
            'ID' : len(all_books)
        }
        #result = jsonify(book_dict)
        cur.execute("INSERT INTO BooksTable VALUES (?,?,?,?)", [book_dict["ID"], book_dict["Title"], book_dict["Author"], book_dict["Rating"]])
        conn.commit()
        conn.close()
        return redirect('/index')
    return render_template('bookform.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == '__main__':
    app.config.from_object(Config)
    app.run()
    
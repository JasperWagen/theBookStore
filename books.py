from flask import request, jsonify, render_template, flash, url_for, redirect, abort
import sqlite3, json, flask, uuid
import bookclass
from forms import BookForm
from config import Config
from PIL import Image

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

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

@app.route('/index/<id>', methods=['GET'])
def bookPage(id):
    try:
        conn = sqlite3.connect('bookdata')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        db_fetch = cur.execute('SELECT * FROM BooksTable WHERE ID=?', (id,)).fetchall()
        book = db_fetch[0]
        conn.close()

        return render_template('bookpage.html', book = book, fileName = 'userImages/' + book.get('FileName') + '.png')
    
    except IndexError:
        abort(404)

@app.route('/index/delete/<ID>', methods=['GET'])
def delete_entry(ID):
    try:
        conn = sqlite3.connect('bookdata')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute('delete from BooksTable WHERE id = ?', [ID])
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    except IndexError:
        abort(404)

@app.route('/newbook', methods=['GET', 'POST'])
def bookform():
    form = BookForm()
    if form.validate_on_submit():

        conn = sqlite3.connect('bookdata')
        cur = conn.cursor()
        all_books = cur.execute('SELECT * FROM BooksTable;').fetchall()
        id = str(uuid.uuid4())
        fileName = 'bookPhoto_'+ str(id)
        book_dict = {
            'Author' : form.author.data,
            'Title'  : form.title.data,
            'Rating' : int(form.rating.data), 
            'Description' : form.description.data,
            'FileName': fileName,
            'ID' : id
        }

        form.photo.data.save("static/userImages/" + fileName + ".png")
        
        cur.execute("INSERT INTO BooksTable VALUES (?,?,?,?,?,?)", [book_dict["ID"], book_dict["Title"], book_dict["Author"], book_dict["Rating"], book_dict["FileName"], book_dict["Description"]])
        conn.commit()
        conn.close()
        return redirect('/index')
    return render_template('bookform.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.config.from_object(Config)
    app.run(host="0.0.0.0", debug=True)
    
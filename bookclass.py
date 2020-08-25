# import sqlite3
# from flask import jsonify

# class Book:
  
#       def __init__(self, title, author, rating, id):
#         self.title = title
#         self.author = author
#         self.rating = rating
#         self.id = id

    # def as_json(): {

    # }

# def dict_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return d
        
# def get_all_books():
#     conn = sqlite3.connect('bookdata')
#     conn.row_factory = dict_factory
#     cur = conn.cursor()
#     all_books = cur.execute('SELECT * FROM BooksTable;').fetchall()
#     return jsonify(all_books)

#if __name__ == '__main__':
    #print(get_all_books())
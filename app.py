import datetime
from flask import Flask, render_template, request, jsonify
from database import Database

app = Flask(__name__)
db = Database()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/create', methods=['post'])
def create():
    title = request.form['title']
    message = request.form['message']
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    modified_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pin = False
    sql = "INSERT INTO board(title, message, created_at, modified_at, pin) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, (title, message, created_at, modified_at, pin))
    db.commit()
    return "ok"

@app.route('/delete', methods=['post'])
def delete():
    id = request.form['id']
    sql = "DELETE FROM board WHERE id=?"
    db.execute(sql, (id, ))
    db.commit()
    return "ok"

@app.route('/update', methods=['post'])
def update():
    id = request.form['id']
    title = request.form['title']
    message = request.form['message']
    modified_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "UPDATE board SET title=?, message=?, modified_at=? WHERE id=?"
    db.execute(sql, (title, message, modified_at, id))
    db.commit()
    return "ok"

@app.route('/pin', methods=['post'])
def pin():
    id = request.form['id']
    sql = "SELECT pin FROM board WHERE id=?"
    pin = db.execute_fetch_one(sql, (id, ))[0]

    sql = "UPDATE board SET pin=?, pinned_at=? WHERE id=?"
    if pin :
        db.execute(sql, (False, None, id))
    else:
        db.execute(sql, (True, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id))
    db.commit()
    return "ok"

@app.route('/list', methods=['get'])
def list():
    sql = "SELECT * FROM board ORDER BY pin DESC, pinned_at DESC, modified_at DESC"
    result = db.execute_fetch(sql)
    tuple_keys = ('id', 'title', 'message', 'created_at', 'modified_at', 'pin')
    dict_list = []
    for r in result:
        dict_value = dict(zip(tuple_keys, r))
        dict_list.append(dict_value)
    return jsonify(dict_list)

if __name__ == "__main__" :
    app.run(debug=True)
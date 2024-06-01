from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(host='127.0.0.1', user='root', password='root', db='notice', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def main():
    query = request.args.get('query')
    conn = get_db_connection()
    cursor = conn.cursor()

    if query:
        sql = "SELECT * FROM test WHERE title LIKE %s OR text LIKE %s"
        like_query = f"%{query}%"
        cursor.execute(sql, (like_query, like_query))
    else:
        sql = "SELECT * FROM test"
        cursor.execute(sql)

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('메인페이지.html', data=data)

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO test (title, text) VALUES (%s, %s)"
        cursor.execute(sql, (title, text))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('main'))
    return render_template('작성페이지.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        sql = "UPDATE test SET title = %s, text = %s WHERE id = %s"
        cursor.execute(sql, (title, text, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('main'))
    else:
        sql = "SELECT * FROM test WHERE id = %s"
        cursor.execute(sql, (id,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('수정페이지.html', data=data)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM test WHERE id = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)

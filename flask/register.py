from flask import Flask,redirect, url_for, request,render_template
import psycopg2 

app = Flask(__name__)

def db_connection():
    
    connection = psycopg2.connect(
                    host='localhost',
                    database='flask_db',
                    user='postgres',
                    password='root')
                
    return connection                            

@app.route('/')
def index():

    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM object_master;')
    data = cursor.fetchall()
    connection = db_connection()
    
    return render_template('home_page.html', result = data)


@app.route('/add_employee', methods = ['POST', 'GET'])
def add_employee():
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
    
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO object_master (first_name,last_name,email,password)VALUES (%s,%s,%s,%s)", (first_name,last_name,email,password))
        connection.commit()
        connection = db_connection()
        
        return redirect(url_for('index'))

@app.route('/register')
def register():
    
    return render_template('register_form.html')



@app.route('/delete_employee/<id>')
def delete_employee(id):

    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM object_master WHERE emp_id='+id)
    connection.commit()
    connection = db_connection()
    
    return redirect(url_for('index'))

@app.route('/edit_data', methods=['POST'])
def edit_data():

    if request.method == 'POST':
        user_data = request.get_json()
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE object_master SET first_name = '"+user_data[1]+"', last_name = '"+user_data[2]+"', email = '"+user_data[3]+"' WHERE emp_id="+user_data[0])
        connection.commit()
        connection = db_connection()
        
        return redirect(url_for('index'))
    
if __name__ == '__main__':
   app.run(debug = True)
   
     
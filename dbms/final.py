from functools import wraps

from flask import Flask, render_template, request, session, flash, url_for,redirect
import pymysql

__cnx = None
app = Flask(__name__)

app.secret_key = 'many random bytes'
def get_sql_connection():
    print("Opening mysql connection")
    global __cnx

    if __cnx is None:
        __cnx = pymysql.connect(host='localhost', database='cafeteria2', user='root', passwd='Sanju@123')

    return __cnx

@app.route('/')
def start():
    return render_template("front page.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    connection = get_sql_connection()
    status = True
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["upass"]
        cur = connection.cursor(pymysql.cursors.DictCursor)
        cur.execute("select * from customer where c_email=%s and c_pswd=%s", (email, pwd))
        data = cur.fetchone()
        if data:
            session['logged_in'] = True
            session['username'] = data["c_user_name"]
            flash('Login Successfully', 'success')
            return redirect('home')
        else:
            flash('Invalid Login. Try Again', 'danger')
    return render_template("login.html")

# check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))

    return wrap

# Registration
@app.route('/reg', methods=['POST', 'GET'])
def reg():
    connection = get_sql_connection()
    status = False
    if request.method == 'POST':
        name = request.form["uname"]
        email = request.form["email"]
        pwd = request.form["upass"]
        cur = connection.cursor(pymysql.cursors.DictCursor)
        cur.execute("insert into customer(c_user_name,c_pswd,c_email) values(%s,%s,%s)", (name, pwd, email))
        cur.execute("drop trigger if exists login")
        connection.commit()

        cur.close()
        flash('Registration Successfully. Login Here...', 'success')
        return redirect('login')
    return render_template("reg.html", status=status)


# Home page
@app.route("/home")
@is_logged_in
def home():
    return render_template('main.html')


# logout
@app.route("/logout")
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/menu', methods=['GET', 'POST'])
def menu():

    connection = get_sql_connection()

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['tot']
        name2 = request.form['qty']
        cur = connection.cursor()
        cur.execute("INSERT INTO f_order (total_amnt,quantity) VALUES (%s,%s)",
                    (name,name2))
        connection.commit()

    return render_template("store.html")


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def loginad():
    connection = get_sql_connection()
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM manager WHERE m_user_name = %s AND m_pswd = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True

            session['username'] = account['m_user_name']
            # Redirect to home page
            return redirect(url_for("Index"))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'''
    # Show the login form with message (if any)
    return render_template('adlogin.html', msg=msg)



@app.route('/admin')
def Index():
    connection = get_sql_connection()
    cur = connection.cursor()
    cur.execute("SELECT  * FROM food")
    data = cur.fetchall()
    cur.close()




    return render_template('index2.html', students=data )



@app.route('/insert', methods = ['POST'])
def insert():
    connection = get_sql_connection()

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        price=request.form['price']
        type = request.form['type']
        description = request.form['description']
        catID = request.form['catID']
        cur = connection.cursor()
        cur.execute("INSERT INTO food (f_name, price, f_type,f_description,cat_id) VALUES (%s,%s,%s,%s,%s)",
                    (name, price, type, description, catID))
        connection.commit()
        return redirect(url_for('Index'))




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    connection = get_sql_connection()
    flash("Record Has Been Deleted Successfully")
    cur = connection.cursor()
    cur.execute("DELETE FROM food WHERE f_id=%s", (id_data,))
    connection.commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update():
    connection = get_sql_connection()
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        price = request.form['price']
        type = request.form['type']
        description = request.form['description']
        catID = request.form['catID']
        cur = connection.cursor()
        cur.execute("""
                      UPDATE food
                      SET f_name=%s, price=%s, f_type=%s,f_description=%s,cat_id=%s
                      WHERE f_id=%s
                   """, (name, price, type, description, catID, id_data))
        flash("Data Updated Successfully")
        connection.commit()
        return redirect(url_for('Index'))
@app.route('/menuu', methods=['GET', 'POST'])

def menuu():
    connection = get_sql_connection()
     # creating variable for connection
    cursor = connection.cursor(pymysql.cursors.DictCursor)
        # executing query
    cursor.execute("select * from food")

        # fetching all records from database
    data = cursor.fetchall()
        # returning back to projectlist.html with all records from MySQL which are stored in variable data
    return render_template("menu2.html", data =data)




@app.route('/user')
def Order():
    connection = get_sql_connection()
    cur = connection.cursor()
    cur.execute("SELECT  * FROM f_order")
    data = cur.fetchall()
    cur.close()

    return render_template('user.html', students=data )


@app.route('/userr')
def Order2():
    connection = get_sql_connection()
    cur = connection.cursor()
    #cur.execute("SELECT  * FROM f_order")
    #data = cur.fetchall()
    cur.close()

    return render_template('result.html')



@app.route('/insertUser', methods = ['POST'])
def insertUser():
    connection = get_sql_connection()

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        price=request.form['price']
        type = request.form['type']
        description = request.form['description']
        catID = request.form['catID']
        cur = connection.cursor()
        cur.execute("INSERT INTO f_order (o_id, total_amnt, quantity,f_id,c_id) VALUES (%s,%s,%s,%s,%s)",
                    (name, price, type, description, catID))
        connection.commit()
        return redirect(url_for('Order'))




@app.route('/deleteUser/<string:id_data>', methods = ['GET'])
def deleteUser(id_data):
    connection = get_sql_connection()
    flash("Record Has Been Deleted Successfully")
    cur = connection.cursor()
    cur.execute("DELETE FROM f_order WHERE o_id=%s", (id_data,))
    connection.commit()
    return redirect(url_for('Order'))





@app.route('/updateUser',methods=['POST','GET'])
def updateUser():
    connection = get_sql_connection()
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        price = request.form['price']
        type = request.form['type']
        description = request.form['description']
        catID = request.form['catID']
        cur = connection.cursor()
        cur.execute("""
                      UPDATE f_order
                      SET total_amnt=%s, quantity=%s, f_id=%s,c_id=%s
                      WHERE f_id=%s
                   """, (name, price, type, description, id_data))
        flash("Data Updated Successfully")
        connection.commit()
        return redirect(url_for('Order'))




if __name__ == "__main__":

    app.run(debug=True)
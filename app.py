from flask import *
import sqlite3
  
app = Flask(__name__)  
app.secret_key = 'mySecretKey#123'
 
@app.route('/')  
def index():
    return render_template("index.html"); 

@app.route('/home')  
def home():
	name = session['name']
	return render_template("home.html", name = name) 

''' Long and Redundant Way
@app.route('/accessVerify')  
def accessVerify():
		return render_template("accessVerify.html")

@app.route('/keyVerify', methods = ["POST","GET"])  
def keyVerify():
	accessKey = request.form["key"]
	if accessKey == 'aaa':
		return render_template("admin.html");
	else: return "Invalid Access Key!"
	
@app.route('/admin')  
def admin():
	if request.referrer == (request.url_root + 'view'):
		return render_template("admin.html");
	else: return "Not Permitted" 
    	
'''
@app.route('/accessVerify')  
def accessVerify():
		return render_template("accessVerify.html")

@app.route('/admin', methods = ["POST","GET"])  
def admin():
	if request.referrer == (request.url_root + 'accessVerify'):
		accessKey = request.form["key"]
		if accessKey == 'aq123':
			return render_template("admin.html")  
		else: return abort(401)	#invalid access key
	elif request.referrer == (request.url_root + 'view') or request.referrer == (request.url_root + 'deleteEmployee'):
		return render_template("admin.html");
	else: return abort(403)	#direct access 

@app.route('/registerEmployee')  
def registerEmployee():  
    return render_template("registerEmployee.html"); 

@app.route("/result", methods = ["POST","GET"])
def result():  
    msg = "Looks like the database is not connected :("  
    if request.method == "POST":  
        try:  
            eid = request.form["eid"] 
            name = request.form["name"]  
            address = request.form["address"]
            dob = request.form["dob"]  
            mobile = request.form["mobile"]  
            with sqlite3.connect("employee.db") as con: 
                cur = con.cursor()  
                cur.execute("INSERT into Employees (empID, empName, empAddress, empDOB, empMobileNumber) values (?,?,?,?,?)", (eid, name, address, dob, mobile))  
                con.commit()  
                msg = "Employee record successfully added."
        except:  
            con.rollback()  
            msg = "Unable to add employee record."
        finally:  
            return render_template("success.html", msg = msg)
            con.close()      

@app.route("/view")
def view():
	if request.referrer != (request.url_root + 'admin'): return "Not Permitted"
	con = sqlite3.connect("employee.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute("SELECT * FROM Employees")
	rows = cur.fetchall()
	return render_template("view.html", rows = rows)

@app.route('/searchEmployee')  
def searchEmployee():  
    return render_template("searchEmployee.html");

@app.route("/search_result", methods=['GET', 'POST'])
def search_result():
	search_term = request.form["search_term"]
	searchType = request.form["searchType"]
	con = sqlite3.connect("employee.db")  
	con.row_factory = sqlite3.Row  
	cur = con.cursor()
	if searchType == 'name':
		cur.execute("select * from employees WHERE empName LIKE '' || (?) || '%' COLLATE NOCASE", (search_term,))
	elif searchType == 'eid': cur.execute("SELECT * FROM employees WHERE empID == (?)", (search_term,)) 
	elif searchType == 'age': 
		search_term = int(search_term)
		cur.execute("SELECT * FROM employees WHERE ((strftime('%Y', 'now') - strftime('%Y', empDOB)) - (strftime('%m-%d', 'now') < strftime('%m-%d', empDOB))) = (?);", (search_term,))
	rows = cur.fetchall()
	if len(rows) == 0: msg = "No matching records found."
	else: msg = "All records matching the search criteria are: "
	return render_template("search_result.html", msg = msg, rows = rows)

@app.route("/searchByFirstLetter", methods=['GET', 'POST'])
def searchByFirstLetter():
	nameStart = request.form["nameStart"]
	con = sqlite3.connect("employee.db")  
	con.row_factory = sqlite3.Row  
	cur = con.cursor()
	cur.execute("select * from Employees where empName LIKE '' || (?) || '%' COLLATE NOCASE", (nameStart,)) 
	rows = cur.fetchall()
	if len(rows) == 0: msg = "No matching records found."
	else: msg = "All records matching the search criteria are: "
	return render_template("search_result.html", msg = msg, rows = rows)

@app.route("/deleteEmployee")
def deleteEmployee():
	if request.referrer != (request.url_root + 'admin'): return "Not Permitted"
	return render_template("deleteEmployee.html")
	
@app.route("/delete", methods = ["POST","GET"])
def delete():
	msg = "Looks like the database is not connected :("  
	if request.method == "POST":
		try:  
			eid = request.form["eid"]
			name = request.form["name"]
			with sqlite3.connect("employee.db") as con:			
				cur = con.cursor()  
				cur.execute("SELECT empID FROM employees WHERE empID = (?)", (eid,))
				rows=cur.fetchall()
				if len(rows) == 0:	msg="No such record exists."
				else:
					cur = con.cursor()  
					cur.execute("DELETE FROM employees WHERE empID = (?) AND empName = (?)", (eid, name))  
					con.commit()
					msg = "Employee record successfully deleted."
		except:  
			con.rollback()  
			msg = "Unable to delete employee record."
		finally:  
			return render_template("success.html", msg = msg)
			con.close() 	

@app.route('/login', methods = ['POST'])
def login():
	name = request.form['name']
	session['name'] = name
	return redirect(url_for('home'))

@app.route('/logout', methods = ['POST'])
def logout():
	if session.pop('name') is not None:
		return '''<p>Logged out successfully.<p><br><br><a href="/">Login again</a>'''
	else: return "There was an error in processing your request."	
#main
if __name__ =='__main__':  
    app.run(debug = True)  


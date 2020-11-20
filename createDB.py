import sqlite3  
  
con = sqlite3.connect("employee.db")  
print("Database created successfully.")  
  
con.execute("create table Employees (empId INTEGER PRIMARY KEY NOT NULL, empName VARCHAR(50) NOT NULL, empAddress TEXT NOT NULL, empDOB DATE NOT NULL, empMobileNumber UNIQUE NOT NULL)")  
  
print("Table created successfully.")  
  
con.close() 
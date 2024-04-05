from sqlalchemy import create_engine, text

# Engine is connection string ( mysql:// [username] : [password] @ localhost / [DB Name] )  (NOT TABLE NAME)
eng = create_engine('mysql://root:@localhost/demo_flask')
con = eng.connect()

# To perform SQL You NEED to text() it or it will break
t = text("SELECT * FROM users;")
result = con.execute(t)

# print(result)
#Loop through all users in users table and print it out
for data in result:
    print(data) 

# STEPS FOR CONNECTING SQLALCHEMY TO XAMPP
# 1 - pip install sqlalchemy
# 2 - pip install mysqlclient   (FIXES THE ERROR: 'no module named "MySQLdb"')
# 3 - import create_engine & text from sqlalchemy
# 4 - create an engine connection string
# 5 - create a connector and call connect() on that engine
# 6 - text() ALL SQL code and save as a variable
# 7 - save connector.execute(SQL CODE VAR) as a variable
# (CALL $ python filename ) {db.test.py} to see results!
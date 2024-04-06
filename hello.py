from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from webforms import UserForm, NamerForm

# Create a Flask Instance
app = Flask(__name__)

# Secret Key - Used For Data Validation
app.config['SECRET_KEY'] = "dev"

# Add Database (MySQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/demo_flask'

# Initialize Database
db = SQLAlchemy(app)


# Debug Automatically Saves Changes - Don't Need to Restart App in Terminal
if __name__ == "__main__":
    app.run(debug=True)


# ----- Routes/Decorators  -----

# Create Add User Page (localhost:5000/name)
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    # -- Local Variables --
    name = None             # Save User's Name
    form = UserForm()       # Save User-Template Form

    # IF Valid Submission - Add User To DataBase
    if form.validate_on_submit():
        # Variable Checks if User's Email is Unique or User Doesn't Exist
        user = Users.query.filter_by(email=form.email.data).first()

        # Email Doesn't Exist yet (New User)
        if user is None:
            # Create New User Object and Add it to the Database
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        form.name.data = ''     # Empty Out Form For Next Use
        form.email.data = ''    # Empty Out Form For Next Use
        flash("User Added Successfully!")

    our_users = Users.query.order_by(Users.date_added)
    
    return render_template(
        'add_user.html',
        form = form, 
        name = name, 
        our_users = our_users
    )

# Delete Users Database Record
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    # -- Local Variables --
    name = None             # Save User's Name
    form = UserForm()       # Save User-Template Form
    user_to_delete = Users.query.get_or_404(id)  # Save Record at 'id' / If Doesn't Exist: Display Error 404 Page

    try:
        # Delete the Record and Commit the Change
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
    except:
        print("Whoops! There was a problem deleteing user, try again!")

    our_users = Users.query.order_by(Users.date_added)

    return render_template(
        'add_user.html',
        form = form, 
        name = name, 
        our_users = our_users
    )

# Create Default Route / Home Page (localhost:5000)
@app.route('/') 
def index():
    list_of_items = ["abc", "defg", 15, 4.3, "qwert"]
    return render_template('index.jinja', list_of_items = list_of_items)

# Create Name Page (localhost:5000/name)
@app.route('/name', methods=['GET', 'POST'])
def name():
    # -- Local Variables --
    name = None             # Save User's Name
    form = NamerForm()      # Save User-Template Form
    
    # IF Valid Submission - Save User
    if form.validate_on_submit():
        flash("Form Submitted Successfully!")
        name = form.name.data
        form.name.data = ''     # Empty Out Form For Next Use

    return render_template(
        'name.html',
        name = name,
        form = form
    )

# Update Users Database Record (localhost:5000/update/id)
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # -- Local Variables --
    form = UserForm()   # Save User-Template Form 
    user_to_update = Users.query.get_or_404(id) # Save Record at 'id' / If Doesn't Exist: Display Error 404 Page
    user_to_update.id = id  # Save ID into 'user_to_update' ID field

    if request.method == "POST":
        # Save Name/Email From User Form into Record Object 'user_to_update' 
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']

        try:
            # Attempt to Save Change To DataBase
            db.session.commit()        
            flash("User Updated Successfully!")
        except: 
            flash("ERROR!! Looks Like Something Went Wrong... Try Again!")     

    return render_template(
        'update.html',
        form = form, 
        user_to_update = user_to_update
    )

# Create User Profile Page (localhost:5000/user/name)
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name = name)


# ----- Custom Error Pages -----

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# ----- Models -----

# Create Model for User{id, name, email, date_added}
class Users(db.Model):
    with app.app_context():
        db.create_all()

    # Database Data 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # Create A String Repersentaion of the Object
    def __repr__(self):
        return '<Name %>' % self.name
    
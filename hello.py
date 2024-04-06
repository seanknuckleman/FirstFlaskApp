from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# Create a Flask Instance
app = Flask(__name__)

# Secret Key - Used For Data Validation
app.config['SECRET_KEY'] = "dev"
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# if not app.config['SECRET_KEY']:
#   raise  EnvironmentError("Missing SECRET_KEY environment variable")

# Add Database (sqlite) (Save as a txt file)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Add Database (MySQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/demo_flask'

# Initialize Database
db = SQLAlchemy(app)

# STEPS FOR CREATING A DB
# 1 - Open Bash Terminal
# 2 - $ winpty python
# 3 - >> from [project_name] import app, db
# 4 - >> app.app_context().push()
# 5 - >> db.create_all()
# 6 - >> exit()

# --- Models ---

# Create a Model
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


# --- Classes ---

# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# --- Routes/Decorators ---

# Create Default Route / Home Page (localhost:5000)
@app.route('/') 
def index():
    list_of_items = ["abc", "defg", 15, 4.3]
    return render_template(
        'index.jinja',
        list_of_items = list_of_items
    )


# Create User Profile Page (localhost:5000/user/...)
@app.route('/user/<name>')
def user(name):
    # render_template Variables DONT HAVE TO BE THE SAME
    return render_template(
        'user.html',
        user_name = name    # CONVENTION IS TO NAME SAME (name = name)
    )


# Create Name Page (localhost:5000/name)
@app.route('/name', methods=['GET', 'POST'])
def name():
    # -- Local Variables --
    name = None         # Save User's Name
    form = UserForm()   # Save User-Template Form
    
    # IF Valid Submission - Save User
    if form.validate_on_submit():
        # Save Name For Website Display Purposes
        name = form.name.data

        # Empty Out Form For Next Use
        form.name.data = ''

        # Display Success Alert 
        flash("Form Submitted Successfully!")
    
    return render_template(
        'name.html',
        name = name,
        form = form
    )


# Create Add User Page (localhost:5000/name)
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    # -- Local Variables --
    name = None         # Save User's Name
    form = UserForm()   # Save User-Template Form

    # IF Valid Submission - Add User To DataBase
    if form.validate_on_submit():
        # Variable Checks if User's Email is Unique or User Doesn't Exist
        user = Users.query.filter_by(email=form.email.data).first()

        # Email Doesn't Exist yet (New User)
        if user is None:
            # Create New User Object
            user = Users(name=form.name.data, email=form.email.data)

            # Add User to DataBase
            db.session.add(user)
            db.session.commit()
        
        # Save Name From DataBase For Website Display Purposes
        name = form.name.data

        # Empty Out Form For Next Use
        form.name.data = ''
        form.email.data = ''
        
        # Display Success Alert 
        flash("User Added Successfully!")
    
    # Retrive DataBase Data
    our_users = Users.query.order_by(Users.date_added)

    return render_template(
        'add_user.html',
        form = form,
        name = name,
        our_users = our_users
    )


# Update Users Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # Retrieve Record With ID - If Doesn't Exist: Display Error 404 Page
    user_to_update = Users.query.get_or_404(id)

    # Save ID to the 'user_to_update' Object - (Used For Deletion)
    user_to_update.id = id

    # -- Local Variables --
    form = UserForm()   # Save User-Template Form 

    # IF Method == ["POST"]  
    if request.method == "POST":
        
        # Save Records to 'user_to_update' Object from Respective Form Fields 
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        
        # Try Saving Updated Record
        try:
            # Save Change To DataBase
            db.session.commit()
            
            # Display Success Alert 
            flash("User Updated Successfully!")
            
            return render_template(
                'update.html',
                form = form,
                user_to_update = user_to_update
            )
        
        except: 
            # Display Error Alert 
            flash("ERROR!! Looks Like Something Went Wrong... Try Again!")
           
            return render_template(
                'update.html',
                form = form,
                user_to_update = user_to_update
            )
        
    # Method == ["GET"]
    else:
        return render_template(
            'update.html',
            form = form,
            user_to_update = user_to_update
        )


# Delete Users Database Record
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    # Retrieve Record With ID - If Doesn't Exist: Display Error 404 Page
    user_to_delete = Users.query.get_or_404(id)
    
    # -- Local Variables --
    name = None         # Save User's Name
    form = UserForm()   # Save User-Template Form

    # Try Deleting Chosen Record
    try:
        # Delete the Record and Commit the Change
        db.session.delete(user_to_delete)
        db.session.commit()

        # Display Success Alert 
        flash("User Deleted Successfully!")

        # Retrive and Save Updated DataBase In 'our_users'
        our_users = Users.query.order_by(Users.date_added)

        return render_template(
            'add_user.html',
            form = form, 
            name = name, 
            our_users = our_users
        )
    
    except:
        # Print Out Error Message
        print("Whoops! There was a problem deleteing user, try again!")

        # Retrive DataBase Data
        our_users = Users.query.order_by(Users.date_added)

        return render_template(
            'add_user.html',
            form = form, 
            name = name, 
            our_users = our_users
        )



# --- Custom Error Pages ---

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# --- Run App ---

# Run App In Debug Mode If Loaded Succssfully
if __name__ == "__main__":
    app.run(debug=True)

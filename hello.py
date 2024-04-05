from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
# from datetime import datetime

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

# Create a Model
class Users(db.Model):
    with app.app_context():
        db.create_all()

    # Database Data 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # date_added = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    # Create A String Repersentaion of the Object
    def __repr__(self):
        return '<Name %>' % self.name

# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Routes/Decorators

# Create Default Route / Home Page (localhost:5000)
@app.route('/') 
def index():
    list_of_items = ["abc", "defg", 15, 4.3]
    return render_template('index.jinja',
        list_of_items = list_of_items)

# Create User Profile Page (localhost:5000/user/...)
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)

# Create Name Page (localhost:5000/name)
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")
    return render_template(
        'name.html',
        name = name,
        form = form
    )

# Create Add User Page (localhost:5000/name)
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',
        form=form,
        name=name,
        our_users=our_users
    )


# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# Run App In Debug Mode If Loaded Succssfully
if __name__ == "__main__":
    app.run(debug=True)

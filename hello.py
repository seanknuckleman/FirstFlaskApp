from flask import Flask, render_template


# Create a Flask Instance
app = Flask(__name__)


# Create a route decorator
@app.route('/')
def index():
    list_of_items = ["abc", "defg", 15, 4.3]
    return render_template('index.jinja',
        list_of_items = list_of_items)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)


# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# If Main Run App
if __name__ == "__main__":
    app.run(debug=True)

# {{ X|(FILTER) }}
# capitalize    Abc
# lower         abc
# upper         ABC
# title         Ab Cd Efg Hi    Capitalize first letter of every word
# safe          Allows HTML to be passed - tells Framework NOT TO CRASH (Not a Hacker)
# trim          Eliminate all trailing white space

# localhost:5000/user/Sean
# @app.route("/user/<name>")
# def user(name):
#     return "<h1>Hello {}!!!</h1>".format(name)

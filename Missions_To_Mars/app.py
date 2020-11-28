# Import necessary libraries
from flask import Flask, render_template

# Create instance of Flask app
app = Flask(__name__)

# Create route
@app.route("/")
def index():


if __name__ == "__main__":
    app.run(debug=True)

# Import necessary libraries
from flask import Flask, render_template, jsonify, redirect
from scrape_mars import scrape
from flask_pymongo import PyMongo

# Create instance of Flask app
app = Flask(__name__)

# Set up MongoDB
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Create route
@app.route("/")
def index():
    # Query the Mongo Database
    mars = mongo.db.mars.find_one()
    return render_template("index.html")
    

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_data,
        upsert = True
    )
    return redirect("http://localhost:5000/", code = 302)

if __name__ == "__main__":
    #thread.start_new_thread(go, ())
    app.run(debug=True)

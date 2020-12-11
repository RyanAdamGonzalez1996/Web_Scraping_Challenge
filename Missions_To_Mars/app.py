# Import necessary libraries
from flask import Flask, render_template, jsonify, redirect
import scrape_mars
from flask_pymongo import PyMongo
import pymongo
import os

# Create instance of Flask app
app = Flask(__name__)

# Set up MongoDB
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Declare the database
db = client.mars_db

# Declare the Collection
mars = db.mars

# Create route
@app.route("/")
def index():
    # Query the Mongo Database
    marsFinal = mars.find_one()
    return render_template("index.html", marsFinal = marsFinal)
    

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_data,
        upsert = True
    )
    return redirect("http://localhost:5000/", code = 302)

if __name__ == "__main__":
    app.run(debug=True)

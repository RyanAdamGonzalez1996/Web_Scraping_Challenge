# Import necessary libraries
from flask import *
import random
from scrape_mars import scrape
import pymongo

# Create instance of Flask app
app = Flask(__name__)

# Set up MongoDB
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Declare the Database

# Declare the collection
x=2

def go():
    while True:
        global x
        x=random.uniform(20.20, 30.00)
        x=Decimal(x)
        x=round(x,2)
        time.sleep(2)
       

# Create route
@app.route("/")
def index():
    thread.start_new_thread(background, ())
    return(
        f"Available Routes: <br/>"
        f"/scrape"
    )

@app.route("/scrape")
def scrape():

    return jsonify(scrape())

if __name__ == "__main__":
    thread.start_new_thread(go, ())
    app.run(debug=True, threaded = True)

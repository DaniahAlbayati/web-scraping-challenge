from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/dic_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    dic = mongo.db.dic.find_one()

    # Return template and data
    return render_template("index.html", dic=dic)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    dic=mongo.db.dic
    dic_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    dic.update(
        {},
        dic_data,
        upsert=True
    )

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
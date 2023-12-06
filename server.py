from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db

app = Flask(__name__)
app.secret_key = "placeholder"

@app.route('/')
def show_homepage():
    pass



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
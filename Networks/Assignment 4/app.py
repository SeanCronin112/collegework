from flask import Flask, render_template, request, jsonify
import csv
import json
import flask_wtf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'moonshine'

@app.route('/')
def home():
    return render_template("welcome.html")

@app.route('/formtest', methods=["POST", "GET"])
def formtest():
    user="Default"
    if request.method == "POST":
        return render_template('formdata.html', value=request.form["name"])
    else:    
        return render_template('formtest.html')

@app.route('/formdata')
def formdata(user=""):
    username = user
    return render_template("formdata.html", value=username)


@app.route('/allegiances')
def allegiances():
    with open("allegiance.csv", "r") as b:
        csv_reader = csv.reader(b)
        exampleData = list(csv_reader)
    return jsonify(exampleData)

@app.route('/allegiancedashboard')
def allegiancedashboard():
    return render_template("allegiance_templates.html")

if __name__ == "__main__":
    app.run(debug=True)
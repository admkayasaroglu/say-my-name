import os
from flask import Flask, render_template, url_for, request, redirect
from match_names import Matcher

app = Flask(__name__)
app.debug=True

@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        name = request.form['yourname']
        return redirect(url_for('matches', name=name))
    else:
        return render_template('home.html')

@app.route('/matches/<name>', methods=['GET'])
def matches(name):
    name_matcher = Matcher()
    name_list = name_matcher.match(name, 5) 
    return render_template('matches.html', name_list=name_list)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')




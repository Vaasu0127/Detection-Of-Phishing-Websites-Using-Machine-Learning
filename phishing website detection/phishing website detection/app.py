import flask
from flask import Flask, render_template, request
import joblib
import inputScript
import regex

import sys
import logging


app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


# @app.route('/')
@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/faq')
def faq():
    return flask.render_template('faq.html')

@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/contactus')
def contactus():
    return flask.render_template('contactus.html')

@app.route('/predict', methods = ['POST'])
def predict():
    classifier = joblib.load('rf_final.pkl')
    if request.method=='POST':
        url = request.form['url']
        if not url:
            return render_template('index.html', label = 'Please input url')
        elif(not(regex.search(r'^(http|ftp)s?://', url))):
            return render_template('index.html', label = 'Please input full url, for exp- https://facebook.com')
        
        
        checkprediction = inputScript.main(url)
        prediction = classifier.predict(checkprediction)

        if prediction[0]==1 :
            label = 'website is not legitimate'
        elif prediction[0]==-1:
            label ='website is legitimate'
        
        return render_template('index.html', label=label)
        
        
if __name__ == '__main__':
    app.run()
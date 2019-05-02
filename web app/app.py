from flask import Flask, render_template, flash, redirect, url_for, session, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

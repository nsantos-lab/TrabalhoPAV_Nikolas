from app import app
from flask import render_template

#rota para a página inicial
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/blog')
def blog():
    return 'Esse é o blog' 
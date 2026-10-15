from app import app

#rota para a página inicial
@app.route('/')
def homepage():
    return 'Essa é a página inicial' 

@app.route('/blog')
def blog():
    return 'Esse é o blog' 
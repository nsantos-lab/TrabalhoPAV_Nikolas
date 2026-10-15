from app import app

#rota para a página inicial
@app.route('/')

def homepage():
    return 'Agora tem sua propria rota!!' 
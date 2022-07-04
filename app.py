from flask import Flask, render_template, request, session
from game_of_life import GameOfLife


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = True
client_width = 10
client_height = 10


@app.route('/', methods=['get', 'post'])
def index():
    global client_width
    global client_height
    message_width = ''
    message_height = ''
    if request.method == 'POST':
        try:
            client_width = int(request.form.get('width'))
            client_height = int(request.form.get('height'))
        except:
            client_width = 20
            client_height = 20
            message_height = 'Некорректные данные'
            message_width = 'Некорректные данные'
        if client_width < 3:
            message_width = 'Число должно быть больше 3'
        if client_height < 3:
            message_height = 'Число должно быть больше 3'
    GameOfLife(client_width, client_height)
    return render_template('index.html', message_height=message_height, message_width=message_width)


@app.route('/live')
def live(game=GameOfLife(client_width, client_height)):
    if game.count > 0:
        game.form_new_generation()
    game.count += 1
    return render_template('live.html', live=game)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

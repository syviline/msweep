from flask import Flask, request, render_template
from random import randrange
import json
from gameclass import Game

app = Flask(__name__)

game = Game()


def get_data(request):
    return json.loads(request.data.decode("UTF-8"))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    
    game.currently_working_with(ip)
    
    print(game.games)

    if request.method == "POST":
        a = get_data(request)
        if a['type'] == 'server_status':
            return "ok"
        
        elif a['type'] == 'start_game':  # Start of the game
            if ip in game.games:
                return game.get_field(ip)
                pass  # TODO
            game.game_start(ip, int(a['field_size']), int(a['mines_amount']))
            return game.get_field(ip)
        
        elif a['type'] == 'get_field':
            return game.get_field()

        elif a['type'] == 'move':
            a = game.make_move(int(a['x']), int(a['y']))
            return game.get_field(with_state=True)
        
        elif a['type'] == 'stop_game':
            game.stop()
            return "ok"
        
        elif a['type'] == 'flag':
            game.flag(int(a['x']), int(a['y']))
            return game.get_field()


    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
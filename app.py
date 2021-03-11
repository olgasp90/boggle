from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Some_Secret_Password'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route('/')
def home():
    """ Display the boggle board"""
    boggle_board = boggle_game.make_board()
    session['boggle_board'] = boggle_board

    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)
    return render_template('home.html', boggle_board=boggle_board, highscore=highscore, nplays=nplays)


@app.route('/check-word')
def check_word():
    """ check if the user word is a valid word in words.txt file"""
    word = request.args['word']
    boggle_board = session['boggle_board']
    result = boggle_game.check_valid_word(boggle_board, word)

    return jsonify({"result": result})


@app.route('/user-score', methods=["POST"])
def user_score():
    """ updates the nplays and highscore"""
    score = request.json["$score"]
    nplays = session.get('nplays', 0)
    highscore = session.get('highscore', 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify({'highscore': session['highscore']})
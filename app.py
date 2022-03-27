from flask import Flask, render_template
import database
import callbacks
app = Flask(__name__)

import database
from flask import request
import random
import json
from elosports.elo import Elo


def timer_thread():
    # Thread running in the backend that
    # a) Keeps time
    # b) When timer runs out, Adds highest value post to the ledger, Deletes all posts, then resets timer.
    # c) save timer to a global variable which is accessible by javascript and displays on the frontend
    ...

def _timer():
    # Returns timer to frontend
    ...

def calculate_new_scores(winner_score = 0, loser_score = 0):
    # Return results of elo calculation
    eloLeague = Elo(k=20)
    eloLeague.addPlayer("winner", rating=winner_score)
    eloLeague.addPlayer("loser", rating=loser_score)
    eloLeague.gameOver(winner='winner', loser='loser', winnerHome='winner') # I don't think winnerhome matters too much
    return eloLeague.ratingDict


@app.route('/_ledger_endpoint')
def _ledger_endpoint():
    # TODO: Need to limit how many are shown at once.

    return json.dumps({'html': render_template('_ledger.html', obj_list = database.get_ledger())})

@app.route('/_post_endpoint')
def _post_endpoint():
    post = request.args.get('post', 0, type=str)
    # Append the post to database with default elo score
    # Also would be worthwhile to search for signs of trouble
    # HTTP, HTML, SQL injections, etc.
    # Nasty stuff.
    print(post)
    if 129 > len(post) > 10:
        database.add_prompt(post)

    return '{}'


@app.route('/_submit_endpoint')
def _submit_vote_endpoint():
    win =  request.args.get('win', 0, type=int)
    lose = request.args.get('lose', 0, type=int)
    print("WIN: ")
    print(win)
    print("LOSE: ")
    print(lose)
    # TODO: Calculate elo scores between these two and update database
    data = database.get_thoughts()
    # find our elo scores

    w = None
    l = None

    s = [z for z in data if z['id'] in [win, lose]]

    for z in s:
        if win == z['id']:
            w = z
        else:
            l = z
    print(w, l)
    new_scores = calculate_new_scores(w['elo'], l['elo'])
    print(new_scores)
    database.update_elo(id=w['id'], score=new_scores['winner'])
    database.update_elo(id=l['id'], score=new_scores['loser'])

    return _options_endpoint()

@app.route('/_options_endpoint')
def _options_endpoint():
    # Returns option for user to vote on
    # Two random samples from database
    # Could change in future? More liekly to show good ones, etc?
    # Would need careful deliberation

    d = database.get_thoughts()
    options = random.sample(d, 2)
    # Get two random ones from this

    json_return_struc = {'option_1_text': options[0]['text'],
                         'option_1_id': options[0]['id'],
                         'option_2_text': options[1]['text'],
                         'option_2_id': options[1]['id']}
    return json.dumps(json_return_struc)
    # option_1_text, option_1_id, option_2_text, option_2_id


@app.route('/')
def index():
    return render_template('base.html')


if __name__ == '__main__':
    app.run()

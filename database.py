import sqlite3
import random
def update_elo(id, score):
    con = sqlite3.connect('database')
    score = int(score)
    cur = con.cursor()
    cur.execute(f'''
        UPDATE thoughts
        SET elo = {score}
        WHERE
            id = {id};
    ''')
    con.commit()
    con.close()



def get_thoughts():
    # Return all posts
    con = sqlite3.connect('database')

    cur = con.cursor()
    cur.execute('''
        SELECT * FROM thoughts ORDER BY elo    
    ''')
    g = cur.fetchall()
    rtn_list = []
    for i in g:
        rtn_list.append({'id': i[0],
                         'text': i[1],
                         'timestamp': i[2],
                         'upvotes': i[3],
                         'downvotes': i[4],
                         'elo': i[5]})

    con.close()
    return rtn_list

def get_ledger():

    con = sqlite3.connect('database')

    cur = con.cursor()
    cur.execute('''
        SELECT * FROM ledger ORDER BY elo    
    ''')
    g = cur.fetchall()
    rtn_list = []
    for i in g:
        rtn_list.append({'id': i[0],
                         'text': i[1],
                         'timestamp': i[2],
                         'upvotes': i[3],
                         'downvotes': i[4],
                         'elo': i[5]})

    con.close()
    return rtn_list


def add_prompt(prompt):
    from datetime import datetime
    # Write to database
    # Add a prompt

    randid = random.randint(0, 9999999999)

    con = sqlite3.connect('database')
    cur = con.cursor()
    cur.execute(f'''INSERT INTO thoughts
    (id, text, timestamp, upvotes, downvotes, elo)
    VALUES
    ({randid}, '{prompt}', '{str(datetime.now())}', 0, 0, 1000)
    
    ''')
    con.commit()
    con.close()


from flask import Flask, render_template, request, redirect
import sqlite3
import os
import yaml

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config_list/')
def config():
    return render_template('listconfig.html')

@app.route('/create_config/', methods=['GET', 'POST'])
def create_config():
    conn = sqlite3.connect("configs.db")
    c = conn.cursor()
    if request.method == 'POST':
        try:
            c.execute(
                "INSERT INTO configs (subreddit_name, keywords, num_limit, filter, client_id, client_secret, user_agent, webhook) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (request.form['subreddit_name'],
                request.form['keywords'],
                request.form['num_limit'],
                request.form['filter'],
                request.form['client_id'],
                request.form['client_secret'],
                request.form['user_agent'],
                request.form['webhook']
                ))
            conn.commit()
            conn.close()
            return redirect('/')
        except:
            return "There was an error adding your config."
    else:
        return render_template('createconfig.html')


def init_configs_list_db():
    conn = sqlite3.connect("configs.db")
    c = conn.cursor()
    try:
        c.execute(
            """CREATE TABLE configs (
            subreddit_name TEXT,
            keywords TEXT,
            num_limit INTEGER,
            filter TEXT,
            client_id TEXT,
            client_secret TEXT,
            user_agent TEXT,
            webhook TEXT
            )"""
        )
        conn.commit()
        conn.close()
        print("Successfully created table")
    except:
        print("This is the problem")

if __name__ == "__main__":
    if not os.path.exists("configs.db"):
        init_configs_list_db()
        print("Successfully created configs database")
    app.run(debug = True)
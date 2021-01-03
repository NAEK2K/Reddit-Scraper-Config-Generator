from flask import Flask, render_template, request, redirect
import yaml
import os
import time
import sqlite3
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/config_list/")
def config():
    path = "./config/"
    count = 0
    directories = os.listdir(path)
    for file in directories:
        count += 1
    
    if count > 0:
        return render_template("listconfig.html", message = "There are {number} config(s) available.".format(number = count), directories = directories)
    else:
        return render_template("listconfig.html", message = "There are no available configs.")

@app.route("/create_config/", methods=["GET", "POST"])
def create_config():
    reddit_bot = {}
    reddit_data = {}

    discord = {}
    discord_data = {}

    data = {}
    if request.method == "POST":
        try:
            reddit_data = {
                "subreddit_name": request.form["subreddit_name"],
                "keywords": request.form["keywords"],
                "num_limit": request.form["num_limit"],
                "filter": request.form["filter"],
                "client_id": request.form["client_id"],
                "client_secret": request.form["client_secret"],
                "user_agent": request.form["user_agent"],
                "username": request.form["reddit_username"],
                "password": request.form["reddit_password"],
                "tracked_users": request.form["tracked_users"]
            }

            discord_data = {
                "username": request.form["discord_bot_name"],
                "avatar_url": request.form["discord_bot_picture"],
                "webhook_url": request.form["discord_bot_webhook"]
            }

            data = {'reddit_bot': reddit_data, 'discord': discord_data}
            if not os.path.exists("./config/{filename}.yaml".format(filename=request.form["file_name"])):
                conn = sqlite3.connect("config.db")
                c = conn.cursor()
                with open(
                    "./config/{filename}.yaml".format(filename=request.form["file_name"]), "w+"
                ) as yaml_file:
                    yaml.dump(data, yaml_file)
                c.execute(
                    "INSERT INTO config (filename, filename_directory) VALUES (?, ?)",
                    (
                        request.form["file_name"],
                        "./config/{filename}.yaml".format(filename=request.form["file_name"])
                    )
                )
                conn.commit()
                conn.close()
                return redirect('/')
            else:
                return render_template("createconfig.html", message = "Error: filename already exists.")
        except:
            return render_template("createconfig.html", message = "Error: There was an error adding your config.")
    else:
        return render_template("createconfig.html")

@app.route("/config/<config_name>", methods=["GET", "POST"])
def configs():
    if request.method == "GET":
        with open("./config/{filename}.yaml".format(filename=request.form["file_name"])):
            pass

def init_db():
    conn = sqlite3.connect("config.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE config (
            filename TEXT,
            filename_directory TEXT
        )"""
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if not os.path.exists("config.db"):
        init_db()
    app.run(debug=True)

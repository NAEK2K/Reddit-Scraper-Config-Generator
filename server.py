from flask import Flask, render_template, request, redirect
from flask_restful import Api
import yaml
import os

app = Flask(__name__)
api = Api(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_config/", methods=["GET", "POST"])
def create_config():
    reddit_data = {}
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
                "tracked_users": request.form["tracked_users"],
            }

            discord_data = {
                "username": request.form["discord_bot_name"],
                "avatar_url": request.form["discord_bot_picture"],
                "webhook_url": request.form["discord_bot_webhook"],
            }

            data = {"name": request.form["file_name"], "reddit_bot": reddit_data, "discord": discord_data}
            if not os.path.exists(
                "./config/{filename}.yaml".format(filename=request.form["file_name"])
            ):
                with open(
                    "./config/{filename}.yaml".format(
                        filename=request.form["file_name"]
                    ),
                    "w+",
                ) as yaml_file:
                    yaml.dump(data, yaml_file)
                return redirect("/")
            else:
                return render_template(
                    "createconfig.html", message="Error: filename already exists."
                )
        except:
            return render_template(
                "createconfig.html",
                message="Error: There was an error adding your config.",
            )
    else:
        return render_template("createconfig.html")

@app.route("/config/", methods=["GET"])
def listconfigs():
    if request.method == "GET":
        path = "./config/"

        directories = os.listdir(path)
        configs_contents = {}
        count = 0
        for file in directories:
            with open("./config/{}".format(file), "r") as f:
                config = yaml.safe_load(f)
                configs_contents[count] = config
                count += 1
        
        return render_template("configs.html", configs = configs_contents, count = count)
    else:
        return "Cannot make POST request."

@app.route("/config/<config_name>", methods=["GET", "POST"])
def configfile(config_name):
    if request.method == "GET":
        with open("./config/{}.yaml".format(config_name), "r") as f:
            config = yaml.safe_load(f)

            return render_template("createconfig.html",
            discord_bot_picture = config.get("discord").get("avatar_url"),
            discord_bot_name = config.get("discord").get("username"),
            discord_bot_webhook = config.get("discord").get("webhook_url"),
            subreddit_name = config.get("reddit_bot").get("subreddit_name"),
            client_id = config.get("reddit_bot").get("client_id"),
            client_secret = config.get("reddit_bot").get("client_secret"),
            filter = config.get("reddit_bot").get("filter"),
            keywords = config.get("reddit_bot").get("keywords"),
            num_limit = config.get("reddit_bot").get("num_limit"),
            password = config.get("reddit_bot").get("password"),
            tracked_users = config.get("reddit_bot").get("tracked_users"),
            user_agent = config.get("reddit_bot").get("user_agent"),
            reddit_username = config.get("reddit_bot").get("username"),
            reddit_password = config.get("reddit_bot").get("subreddit_name"),
            file_name = config.get("name")
            )
    else:
        pass

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template
import twitter import get_tweets

finalBots = Flask(__name__)

@finalBots.route("/")
def home():
  return render_template("home.html")

@finalBots.route("/ryan")
def ryan():
  return "Hello Ryan"

if __name__ == "__main__":
  finalBots.run(debug=True)

  
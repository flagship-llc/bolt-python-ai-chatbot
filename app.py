import os
import logging
from flask import Flask
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from listeners import register_listeners

# Initialize Flask and Slack Bolt apps
flask_app = Flask(__name__)
slack_app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
handler = SlackRequestHandler(slack_app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Register Slack Listeners
register_listeners(slack_app)

# Create Flask route for Slack events
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(flask_app.request)

# Start Flask app
if __name__ == "__main__":
    flask_app.run(port=3000)
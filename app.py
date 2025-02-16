from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App
app = App(
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    token=os.environ.get("SLACK_BOT_TOKEN")
)

# Register Slack Listeners
from listeners import register_listeners
register_listeners(app)

# Initialize Flask app
from flask import Flask, request
flask_app = Flask(__name__)

# SlackRequestHandler translates WSGI requests to Bolt's interface
# and builds WSGI response from Bolt's response.
from slack_bolt.adapter.flask import SlackRequestHandler
handler = SlackRequestHandler(app)

# Create Flask route for Slack events
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    # handler runs App's dispatch method
    return handler.handle(request)

# Start Flask app
if __name__ == "__main__":
    flask_app.run(port=3000)
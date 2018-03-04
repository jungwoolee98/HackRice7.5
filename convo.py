from slackclient import SlackClient
import os

"""#slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient("xoxb-325094916343-7MqoXn0dTluyEY0JLgbPATfe")

sc.api_call(
  "conversations.open",
  users=["U9HTFSU59", "U9J0Z5YN6"]
)"""


#slack_token = os.environ["SLACK_API_TOKEN"]
#sc = SlackClient("xoxp-324004296788-323933912179-324157171010-78485801d0faec19843d7f466ce3e1ce")
sc = SlackClient(os.environ.get("SLACK_API_TOKEN"))
"""sc.api_call(
  "conversations.create",
  name="myprivatechannel3",
  is_private=True
)"""

def create_convo(name1):
	sc.api_call(
		"conversations.create",
		name=name1,
		is_private=True)

def invite_convo(user_id, channel_id):
	sc.api_call(
        "conversations.invite",
        channel=channel_id,
        users=user_id)
sc.api_call(
    "conversations.invite",
    channel='G9K1BTBK8',
    users=['U9J0Z5YN6'])


"""sc.api_call(
  "conversations.open",
  users=["U9HTFSU59", "U9J0Z5YN6"]
)"""
import os
import time
import re
from slackclient import SlackClient
import psycopg2 as p
from datetime import datetime
import convo

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_client_user = SlackClient(os.environ.get("SLACK_API_TOKEN"))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

con = p.connect("dbname = 'hackdb' user = 'hackrice' host = 'localhost' password = '123456' port = '5432'")
cur = con.cursor()

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

bush = {}
hobby = {}
#jungwoo = "U9HTFSU59"
#andy = "U9J0Z5YN6"

def constructDateTime(input):
    """
    JUST GIVE THE HOUR, 7:00 IS FINE THO
    """
    #Possible Ways the Date Can be represented:
    #March 1
    #mar 1
    #3/22
    #3-22
    #

    #Possible ways time can be represented:
    #7
    #7 pm
    #7 p.m.
    #7:00 p.m
    elements = input.split(" ")
    digits = ['0','1','2','3','4','5','6','7','8','9']
    months = ['JANUARY','JAN','FEBRUARY','FEB','MARCH','MAR','APRIL','APR','MAY','IGNORE','JUNE','JUN',
              'JULY','JUL','AUGUST','AUG','SEPTEMBER','SEPT','OCTOBER','OCT','NOVEMBER','NOV','DECEMBER','DEC']
    elements.reverse()
    hour = 0
    month = None
    day = None
    am = False
    if elements[0].upper()[0] not in digits:
        time_type = elements.pop(0)
        if time_type.upper()[0] == "P":
            hour = 12
        elif time_type.upper()[0] == "A":
            am = True
    if ":" in elements[0]:
        hour += int(elements.pop(0).split(":")[0])
    else:
        hour += int(elements.pop(0))
    if elements[1].upper() in months:
        month = months.index(elements[1].upper()) / 2 + 1
        day = int(elements[0])
    else:
        for item in ["/","-"]:
            if item in elements[0]:
                month = int(elements[0].split(item)[0])
                day = int(elements[0].split(item)[1])
    if hour == 24:
        hour -= 12
    elif hour == 12 and am == True:
        hour -= 12
    try:
        datentime = datetime(2018, month, day, hour)
        date,time = str(datentime.month) + "-" + str(datentime.day), str(datentime.hour)
    except ValueError as e:
        #Jungwoo tell them to learn how to fucking tell time
        print "learn how to tell time"
        date, time = "no","work"
    return date, time

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                real_user = event["user"]
                return message, event["channel"], real_user
    return None, None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def get_private_channels():
    private_channels = {}
    jsonlist = slack_client_user.api_call(
        "conversations.list",
        types="private_channel")['channels']
    for channel in jsonlist:
        print channel['id']
        print channel['name']
        private_channels[channel['name']] = channel['id']
    return private_channels

def uber_to(place, real_user, command, channel):
    default_message = "Invalid command. Example format: 'uber to hobby 2/23 7 pm'"
    try:
        date1, time1 = constructDateTime(command)
        print date1
        print time1
        #cur.execute("INSERT INTO UserData VALUES (%s, %s, %s, %s)", (real_user, 'hobby', date, time))
        #con.commit() 
        #cur.execute("INSERT INTO DateCount VALUES ('invalid, 'invalid', 'invalid')")
        #con.commit()
        cur.execute("SELECT * FROM DateCount")
        data = cur.fetchall()
        flag = 0
        for row in data:
            print 1
            if date1 not in row and time1 not in row:
        		#make a new row in DateCount with count = 1
                flag = 1
        		#cur.execute("INSERT INTO DateCount VALUES (%s, %s, %s)", (date, time, '1'))
        		#con.commit()
        	#elif date in row and time in row:
        		#go to that row and do count += 1
        		#print 'ERROR'
        		#freq_count = row[2]
        		#print freq_count
        		#cur.execute("UPDATE DateCount SET freq = %s WHERE date = %s AND time = %s", (freq_count, date, time))
        name2 = place+'_'+date1+'_'+time1
        name2 = str(name2)
        print str(name2)
        if name2 not in bush and name2 not in hobby:
            #cur.execute("INSERT INTO DateCount VALUES (%s, %s, %s)", (date, time, '1'))
            #con.commit()
            #cur.execute()
            #CREATE A CHANNEL
            
            """slack_client_user.api_call(
                "conversations.create",
                name=name1,
                is_private=True)"""
            convo.create_convo(name2)

            """ jsonlist = slack_client_user.api_call(
                "conversations.list",
                types="private_channel")['channels']
            for channel in jsonlist:
                print channel['id']
                print channel['name']"""

            private_channels = get_private_channels()
            print private_channels
            if place == 'bush':
                bush[name2] = private_channels[name2]
            if place == 'hobby':
                hobby[name2] = private_channels[name2]

        else:
            #freq_count = row[2]
            #print "meeeeeeeeeep"
            #cur.execute("UPDATE DateCount SET freq = %s WHERE date = %s AND time = %s", (freq_count, date, time))
            #con.commit()
            if place == 'bush':
                channel_id = bush[name2]
            if place == 'hobby':
                channel_id = hobby[name2]
            print channel_id
            print 'CHANNEL_IDDDDDDDDDDDDDDD'
            print real_user
            print 'REAL_USERRRRRRRRRRRRRRRRRR'
            convo.invite_convo([real_user], channel_id)
        

            

    except:
        slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=default_message)

    #cur.execute("INSERT INTO UserData VALUES (%s, %s, %s, %s)" % (real_user, 'hobby', date, time))
    #Add info to UserData
    #if date and time not in DateCount, then make a new row with count = 1
    #if date and time in DateCount, then go to that row and do count += 1
    #version = count / 4
    #if count % 4 = 1 in DateCount for that date and time, make a new channel; get that channel's id - within Channel make a row of data
    #if count % 4 != 1, then get the channel_id for that date, time, version
    #now add real_user to that channel_id 


    """elif place == 'bush':
        ree1 = 2
        #bush shit
    else:
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=default_message)"""



def handle_command(command, channel, real_user):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)
    help_response = "To use Uber Bot use the command 'uber to [location] [date] [time]'"

    command = command.lower()

    # Finds and executes the given command, filling in response
    response = None
    """slack_client.api_call(
        "conversations.list",
        types="public_channel, private_channel")['channels']"""
    # This is where you start to implement more commands!
    help_message = "type commands in this format: \n" \
              "uber to [destination] [date] [time]\n" \
              "Acceptible date formats (using April 28 as our example):\n" \
              "April 22\n" \
              "apr 22\n" \
              "4/22\n" \
              "4-22\n" \
              "Acceptible time formats (using 1:00 pm as our example)\n" \
              "13\n" \
              "13:00\n" \
              "1 pm\n" \
              "1 P.M.\n" \
              "1:00 pm\n" \
              "Nothing is case sensitive, only the hour is needed \n" \
              "Please put a space between the hour and am/pm(7pm is not acceptible)"

    if command.startswith("help"):
        

        # Sends the response back to the channel
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=help_message
        )
    elif command.startswith("uber to hobby"):
        response = "Testing uber to hobby"
        uber_to('hobby', real_user, command, channel)
        #dates = command.split(' ')[3:]
        #dates = command.lstrip("uber to hobby ")

        """slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response
        )"""
        """slack_client_user.api_call(
            "conversations.invite",
            channel="G9K059A14",
            users=[andy])"""
        """slack_client_user.api_call(
            "conversations.create",
            name="testingpublic",)"""
        #print slack_client_user.api_call(
            #"groups.list")
        #get_private_channels()


    else:
    	slack_client.api_call(
    		"chat.postMessage",
    		channel = channel,
    		text=help_message)



if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            #print slack_client.rtm_read()
            command, channel, real_user = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel, real_user)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

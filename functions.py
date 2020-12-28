import requests
import json
import random
import threading
from colorama import Fore, Back, Style
from replit import db
from datetime import date, datetime, timezone


# Function to format the time
# Used in get_daily_quote() function but can
# Be used in future functions if necessary
def format_time():
    # Get the current date
    today = date.today()

    # Format the date to fit mm/dd/yy
    # Used as reference: https://strftime.org/
    today_formatted = today.strftime("%B %d, %Y")

    # Return the formatted date
    return (today_formatted)


# Function to get the quote of the day
def get_daily_quote():
    # Use the request module to request data from the API
    # It will return a random quote
    response = requests.get("https://zenquotes.io/api/today")

    # Call the format_time() function
    quote_today = format_time()

    # Convert this response to JSON
    json_data = json.loads(response.text)

    # Get the quote from the JSON data
    # Displays the quote, then the author of the quote
    # q = quote
    # a = author
    daily_quote = ("Quote for " +
                   str(quote_today) +
                   ": " +
                   json_data[0]['q'] +
                   " - " +
                   json_data[0]['a'])

    # Return the daily quote
    return(daily_quote)


# Function to get the link for the rick roll
def get_rick():
    link = "https://www.youtube.com/watch?v=dGeEuyG_DIc"

    return (link)


# Function to get the current date and time
# Gets the time in UTC, but not in intended time zone (AST)
# Used as reference: https://stackoverflow.com/questions/25837452/python-get-current-time-in-right-timezone
def get_time():

    utc_time = datetime.now(timezone.utc)

    current_time = utc_time.astimezone()

    time_formatted = current_time.strftime("The current time is: %H %M:%S")

    return (time_formatted)


# Function to get a random color
# Used as reference: https://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
def get_random_color():
    rand_color = "%06x" % random.randint(0, 0xFFFFFF)

    link_color = "https://color-hex.org/color/" + rand_color

    text_color = get_text_color()

    print(text_color)

    return (link_color)


# Function to style the text
# This function gets called when user types in $color
# This will ONLY get printed to the console.
def get_text_color():

    text_color = Fore.RED + "some red text\n"
    background_color = Back.BLUE + "a blue background\n"
    style_color = Style.NORMAL + "with a normal style\n"

    full_color = text_color + " " + background_color + " " + style_color

    print(full_color)


# Function to determine how much money you made
# Get a random number, and if your number is the lucky one
# You will make $100,000
# Note: this is meant to be for fun
def get_money():
    amount = "$100,000"
    amount_made = ""

    rand_num = random.randint(0, 9999)

    if rand_num <= 10 and rand_num >= 900:
        amount_made = "Congratulations, you just made " + amount
    else:
        amount_made = "Sorry, you made no money. Better luck next time."

    return (amount_made)


# Function to make sure that the bot is saying something
# Every 10 minutes. Note that this will only print to
# The console, and not to the Discord server.
# Used as reference: https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds
def time_test():
    threading.Timer(600.0, time_test).start()
    print("This is a test to make sure "
          "I am always saying something every 10 minutes.")


# Function to update the encouragements from the database
# If encouragements is in our database,
# Then retrieve that encouragement,
# And use it in our program
def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements

    else:
        db["encouragements"] = [encouraging_message]


# Function to delete an encouragement
# Index = index of msg to delete
# If the length of our encouragement
# Is longer than the index,
# Then delete the encouragement at its index,
# Then update the database
def delete_encouragement(index):
    encouragements = db["encouragements"]

    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements

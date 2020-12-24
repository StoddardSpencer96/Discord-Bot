import requests
import json
import time
import random
from replit import db
from datetime import date


# Function to get the quote of the day
def get_quote():
    # Use the request module to request data from the API
    # It will return a random quote
    response = requests.get("https://zenquotes.io/api/today")

    # Get the current date
    today = date.today()

    # Format the date to fit mm/dd/yy
    # Used as reference: https://strftime.org/
    today_formatted = today.strftime("%B %d, %Y")

    # Convert this response to JSON
    json_data = json.loads(response.text)

    # Get the quote from the JSON data
    # Displays the quote, then the author of the quote
    # q = quote
    # a = author
    quote = ("Quote for " 
    + str(today_formatted) 
    + ": " 
    + json_data[0]['q'] 
    + " - "
    + json_data[0]['a'])

    # Return the quote
    return(quote)

# Function to get the link for the rick rol
def get_rick():
  link = "https://www.youtube.com/watch?v=dGeEuyG_DIc"

  return (link)

# Function to get the current date and time
# Work in Progress
def get_time():
  current_time = time.strftime("%I:%S %p")

  time_formatted = ("The current time is: " 
  + str(current_time))
  
  return (time_formatted)

# Function to get a random color
# Used as reference: https://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
def get_color():
  rand_color = "#" + "%06x" % random.randint(0 , 0xFFFFFF)

  return (rand_color)


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

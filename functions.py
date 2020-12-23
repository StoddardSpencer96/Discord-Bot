import requests
import json
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
    quote = "Quote for " + str(today_formatted) + ": " + json_data[0]['q'] + " - " + json_data[0]['a']

    # Return the quote
    return(quote)


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

# ALL FUNCTIONS GO HERE
import requests
import json
from replit import db # used for our replit database
from datetime import date # used to get the current date

# FUNCTION TO GET THE QUOTE OF THE DAY
def get_quote():
  # use the request module to request data from the API
  # it will return a random quote
  response = requests.get("https://zenquotes.io/api/today")

  # get the current date
  today = date.today()

  # format the date to fit mm/dd/yy
  # used as reference: https://strftime.org/
  today_formatted = today.strftime("%B %d, %Y")

  #convert this response to JSON
  json_data = json.loads(response.text)

  # get the quote from the JSON data
  # displays the quote, then the author of the quote
  # q = quote, a = author
  quote = "Quote for " + str(today_formatted) + ": " + json_data[0]['q'] + " - " + json_data[0]['a']

  # return the quote
  return(quote)

# function to update the encouragements from the database
# if encouragements is in our database,
# then retrieve that encouragement,
# and use it in our program
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements

  else:
    db["encouragements"] = [encouraging_message]

# function to delete an encouragement
# index = index of msg to delete
# if the length of our encouragement 
# is longer than the index, 
# then delete the encouragement at its index,
# then update the database
def delete_encouragement(index):
  encouragements = db["encouragements"]

  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements
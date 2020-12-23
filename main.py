# USER GUIDE
#--------------------------------------------------------#
# LIST OF COMMANDS:
# $inspire = for a new inspirational quote
# $new  = to add a new inspirational quote
# $del = to delete an inspirational quote
# $list  = to see the list of inspirational quotes
# $responding = if it's True, the bot will respond; if it's false, the bot will not respond
# $rickroll = Bot will send a YouTube link to Never Gonna Give You Up by Rick Astley

# OTHER:
# Bot will send a random encouraging message whenever a user types in a sad word (ex: sad, lonely, depressed, angry)
# Bot will notify the chat when the GitHub repo has been updated (ex: star/unstar the repo sends a notification)
#Bot will send a random greeting whenever the user types in "hi", "hey", or "hello" in lower or uppercase.

#TO-DO LIST:
#1) Get the greeting to work with mixed case (ex: HeY, HeLLo)
#2) Fix up commenting (some are all caps, some are all lowercase)
#3) Clean up code to make the main.py file neater.
#--------------------------------------------------------#

# LIBRARIES
#--------------------------------------------------------#
#Import libraries to use
import discord
import os
import random # used for the bot to choose messages randomly
from replit import db # used for our replit database
from keep_alive import keep_alive # used for our server
from functions import get_quote, update_encouragements, delete_encouragement # used for our functions

# VARIABLE DECLARATIONS
#--------------------------------------------------------#
#Create variable for our bot
client = discord.Client()

#List of sad words
sad_words = ["sad", "depressed", "lonely", "crying", "alone", "unhappy", "miserable", "depressing", "anger", "angry"]

#List of encouraging messages
#reason for variable name: user can add more encouragements to the database
starter_encouragements = ["Cheer up", "Hang in there", "You are a wonderful soul", "I am here for you"]

#List of greetings
bot_greetings = ["Hello!", "Hey!", "Greetings and salutations.", "What's up?", "Hi!", "Good to see you again.", "Hey dude!"]
#--------------------------------------------------------#

# EVENTS
#--------------------------------------------------------#
# Event for logging in
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

# Event for getting the message
@client.event
async def on_message(message):
  if message.author == client.user:
    return
#--------------------------------------------------------#

# LOGIC FOR THE BOT
#--------------------------------------------------------#
  #Create new variables for easier access
  msg = message.content
  greeting = bot_greetings
  options = starter_encouragements
  
  #If user types $inspire, call the get_quote() function,
  #then show the quote to the user
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  #If our message starts with any variation of hi, hey or hello,
  #then choose a random greeting for the bot to use
  if msg.lower() == "hi" or msg.lower() == "hey" or msg.lower() == "hello":
    await message.channel.send(random.choice(greeting))

  #If our message is $rickroll, then rick roll the user
  if msg.startswith('$rickroll'):
    link = "https://www.youtube.com/watch?v=dGeEuyG_DIc"
    await message.channel.send(link)
    
  #If "responding" isn't in our database,
  #then add True
  if db["responding"]:
    if "responding" not in db.keys():
      db["responding"] = True

  #If encouragements is in our database,
  #add the encouragements to the database
  if "encouragements" in db.keys():
    options = options + db["encouragements"]

  #Go through all of the words in the list of 
  #sad words, and if any of the words are 
  #in the message, randomly choose an encouraging 
  #phrase for the user to see
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  # if the user types in $new, then our message 
  # will be split, and we'll get the message 
  # as an array
  if msg.startswith('$new'):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message has been added.")
  
  #If the user types in $del, then create a new list,
  #of encouragements, and if it's in our database,
  #delete the encouragement from our database,
  #then update the database, and show the new list
  #of encouragements
  if msg.startswith('$del'):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split('$del',1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  #If the user types in $list, thehn create a new list,
  #and if the encouragements are in our database,
  #show the user the list of encouragements
  if msg.startswith('$list'):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  #If the user types in $responding, then take the
  #user input, and if they type true, notify the user
  #that responding is on. If they type false, notify
  #the user that responding is off.
  if msg.startswith('$responding'):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
      
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
#--------------------------------------------------------#

# MISCELLANEOUS
#--------------------------------------------------------#
#Runs our web server
keep_alive()

#Runs our bot
client.run(os.getenv('TOKEN'))
#--------------------------------------------------------#
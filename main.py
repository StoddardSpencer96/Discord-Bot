# USER GUIDE
#--------------------------------------------------------#
# LIST OF COMMANDS:
# $inspire = for a new inspirational quote
# $new  = to add a new inspirational quote
# $del = to delete an inspirational quote
# $list  = to see the list of inspirational quotes
# $responding = if it's True, the bot will respond; if it's false, the bot will not respond

# OTHER:
# Bot will send a random encouraging message whenever a user types in a sad word (ex: sad, lonely, depressed, angry)
# Bot will notify the chat when the GitHub repo has been updated (ex: star/unstar the repo sends a notification)
#--------------------------------------------------------#

# LIBRARIES
#--------------------------------------------------------#
# IMPORT LIBRARIES TO USE
import discord
import os
import random # used for the bot to choose messages randomly
from replit import db # used for our replit database
from keep_alive import keep_alive # used for our server
from functions import get_quote, update_encouragements, delete_encouragement # used for our functions

# VARIABLE DECLARATIONS
#--------------------------------------------------------#
# CREATE VARIABLE FOR THE BOT
client = discord.Client()

# LIST FOR SAD WORDS
sad_words = ["sad", "depressed", "lonely", "crying", "alone", "unhappy", "miserable", "depressing", "anger", "angry"]

# LIST OF ENCOURAGING MESSAGES
# reason for variable name: user can add more encouragements to the database
starter_encouragements = ["Cheer up", "Hang in there", "You are a wonderful soul", "I am here for you"]

#LIST FOR GREETINGS
bot_greetings = ["Hello!", "Hey!", "Greetings and salutations.", "What's up?", "Hi!"]
#--------------------------------------------------------#

# EVENTS
#--------------------------------------------------------#
# EVENT FOR LOGGING IN
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

# EVENT FOR GETTING THE MESSAGE
@client.event
async def on_message(message):
  if message.author == client.user:
    return
#--------------------------------------------------------#

# LOGIC FOR THE BOT
#--------------------------------------------------------#
# creates a new variable from message.content, 
  # that way we save some time instead of typing it all out
  msg = message.content
  greeting = bot_greetings
  options = starter_encouragements
  
  # IF OUR MESSAGE STARTS WITH $INSPIRE,
  # CALL THE GET_QUOTE() FUNCTION,
  # THEN SHOWCASE THE QUOTE
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  #If our message starts with any variation of hi, hey or hello,
  #then choose a random greeting for the bot to use
  if msg.lower() == "hi" or msg.lower() == "hey" or msg.lower() == "hello":
    await message.channel.send(random.choice(greeting))
    
  if db["responding"]:
    if "responding" not in db.keys():
      db["responding"] = True

    if "encouragements" in db.keys():
      options = options + db["encouragements"]

  # go through any words in the sad words, 
  # and if any of the words are in the message
  # randomly choose an encouraging phrase for 
  # the user to see
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  # if the user types in $new, then our message 
  # will be split, and we'll get the message 
  # as an array
  if msg.startswith('$new'):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message has been added.")

  if msg.startswith('$del'):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split('$del',1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith('$list'):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

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
# runs our web server
keep_alive()

# RUN THE BOT
client.run(os.getenv('TOKEN'))
#--------------------------------------------------------#
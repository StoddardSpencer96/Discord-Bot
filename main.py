import discord
import os
import random
import events
from replit import db
from keep_alive import keep_alive
from functions import (time_test, update_encouragements, delete_encouragement)

client = discord.Client()


# List of sad words
sad_words = ["sad", "depressed",
             "lonely", "crying", "alone",
             "unhappy", "miserable", "depressing",
             "anger", "angry"]

# List of encouraging messages
# Reason for variable name: user can add more encouragements to the database
starter_encouragements = ["Cheer up",
                          "Hang in there", "You are a wonderful soul",
                          "I am here for you"]

# List of greetings
bot_greetings = ["Hello!", "Hey!",
                 "Greetings and salutations.", "What's up?",
                 "Hi!", "Good to see you again.",
                 "Hey dude!"]

# Calls the function
time_test()


# Event for logging in
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# Event for getting the message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Call the on_message() function in the events.py file
    await events.on_message(message)

    # Define variables to make it easier to access
    msg = message.content
    options = starter_encouragements

    # If "responding" isn't in our database,
    # Then add True
    if db["responding"]:
        if "responding" not in db.keys():
            db["responding"] = True

    # If encouragements is in our database,
    # Add the encouragements to the database
    if "encouragements" in db.keys():
        options = options + db["encouragements"]

    # Go through all of the words in the list of
    # Sad words, and if any of the words are
    # In the message, randomly choose an encouraging
    # Phrase for the user to see
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    # If the user types in $new, then our message
    # Will be split, and we'll get the message
    # As an array
    if msg.startswith('$new'):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message has been added.")

    # If the user types in $del, then create a new list,
    # Of encouragements, and if it's in our database,
    # Delete the encouragement from our database,
    # Then update the database, and show the new list
    # Of encouragements
    if msg.startswith('$del'):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split('$del', 1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    # If the user types in $list, thehn create a new list,
    # And if the encouragements are in our database,
    # Show the user the list of encouragements
    if msg.startswith('$list'):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

# Runs our web server
keep_alive()

# Runs our bot
client.run(os.getenv('TOKEN'))

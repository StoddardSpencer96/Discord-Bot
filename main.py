import discord
import os
import random
from replit import db
from keep_alive import keep_alive
from functions import (get_daily_quote, get_rick,
                       get_time, get_random_color,
                       time_test, update_encouragements, delete_encouragement)

# Create variable for our bot
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

# Call the time_test() function before the events start.
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

    # Create new variables for easier access
    msg = message.content
    greeting = bot_greetings
    options = starter_encouragements

    # If user types $daily, call the get_daily_quote() function,
    # Then show the quote to the user
    if msg.startswith('$daily'):
        quote = get_daily_quote()
        await message.channel.send(quote)

    # If our message starts with any variation of hi, hey or hello,
    # Then choose a random greeting for the bot to use
    if (msg.lower().startswith("hi") or
            msg.lower().startswith("hey") or
            msg.lower().startswith("hello")):
        await message.channel.send(random.choice(greeting))

    # If our message is $rickroll, then rick roll the user
    if msg.startswith('$rickroll'):
        link = get_rick()
        await message.channel.send(link)

    # If our message is $time, then display the current time (in EST)
    if msg.startswith('$time'):
        now = get_time()
        await message.channel.send(now)

    if msg.startswith('$color'):
        rand_color = get_random_color()
        await message.channel.send(rand_color)

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

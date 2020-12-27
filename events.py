import discord
import random
from functions import get_daily_quote, get_rick, get_time, get_random_color
                      
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


# Event for getting the message
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Create new variables for easier access
    msg = message.content
    greeting = bot_greetings

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
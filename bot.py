import discord
from discord.ext import commands
import Players
import os
from dotenv import load_dotenv
import json

#getting token and stuff, copied from online
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#setting up bot in discord client
client = discord.Client()
bot = commands.Bot(command_prefix='$')

#list of commands (even index) and their corresponding explanations (next index)
commands = [
"wins","says how many wins a player has. write player's name after", 
"whoKing","says who the current king/queen is",
"newKing","sets a new king/queen of the hill",
"add","adds a new player.",
"getStreak", "Gives the monarch's curren win streak. resets after a loss",
"getValues", "Gives your win/loss and win percentage (% of games won)",
"gamePlayed", "updates win/loss counters for the players involved. example: Sevag win Altug lose",
"getPlayers", "Gives the names of all the players"]

#following done when bot loads
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

#gives number of wins of given player (input: player name)
@bot.command(name="wins")
async def getWins(ctx, name):
    data = loaddata()
    people = data["people"]
    for p in people:
        if p["name"]==name:
            await ctx.send(p["name"]+" has "+str(p["gamesWon"])+" win(s)")

#checks who is the king/queen (no input)
@bot.command(name="whoKing")
async def WhoIsKing(ctx):
    kingFound = False
    data = loaddata()
    for p in data["people"]:
        if p["isKingOfHill"]:
            await ctx.send(p["name"]+" is the King/Queen, All hail "+p["name"]+"!")
            kingFound = True
    if kingFound == False:
        await ctx.send("Y'all forgot to make someone the monarch.....")

#sets a new king and dethrones old one (input: name of new king)
#can add more roles in the future!
@bot.command(name="newKing")
async def setNewKing(ctx, name):
    oldKing=""
    data = loaddata()
    for p in data["people"]:
        if p["isKingOfHill"] and p["name"] != name: #who to dethrone
            p["isKingOfHill"] = False
            p["currentStreak"] = 0
            oldKing=p["name"]
            writedata(data)
        elif p["name"] == name and p["isKingOfHill"]==False:
            p["isKingOfHill"] = True
            writedata(data)
            await ctx.send(oldKing+" Has been dethrown! All hail "+p["name"]+", the new monarch!")
        elif p["name"] == name and p["isKingOfHill"]:
            await ctx.send("This person is already King/Queen! Why are you doing this?")


#creates a new player ands saves them into the json.txt file 
#(input: name of player)
@bot.command(name="add")
async def CreatePlayer(ctx, name):
    doneOnce = False
    checking = False #false means name exists in json file
    data = loaddata()
    if(len(data["people"])==0) and doneOnce == False: #base condition: when json is empty
        Players.Player(name)
        await ctx.send("Welcome, "+name+" :)")
        doneOnce = True
    else: #when at least 1 person is in json file
        for p in data["people"]:
            if p["name"] == name:
                checking = False
                break
            checking=True
        if checking == True:
            Players.Player(name) #creates new player and adds to json
            await ctx.send("Welcome, "+name+" :)")
            checking = False #reset flag/checking
        else:
            await ctx.send("Person named "+name+" already exists!")


#gives the current streak of a given player (input: name of player)
@bot.command(name="getStreak")
async def giveStreak(ctx):
    data = loaddata()
    for p in data["people"]:
        if p["isKingOfHill"]:
            await ctx.send("King/Queen "+p["name"]+"'s current streak is "+str(p["currentStreak"])+" wins.")

#gives number of wins, losses and win % (W/L/WP) (input: name of player)
#MUST REFACTOR TO USE JSON
@bot.command(name="getValues")
async def getWP(ctx, name):
    data = loaddata()
    for p in data["people"]:
        if p["name"] == name:
            gamesWon = p["gamesWon"]
            gamesLost = p["gamesLost"]
            WP = p["WP"]
            await ctx.send("Your Numbers are "+str(gamesWon)+"/"+str(gamesLost)+" (W/L). Your win percentage is "+str(WP)+".")

#saves score of a recently played game 
#(input: player 1, win/loss, player 2, win/lose)
#user must write "win" for win and "loss" for loss 
#MUST REFACTOR TO USE JSON
@bot.command(name="gamePlayed")
async def gameResult(ctx, name1, state1, name2, state2):
    data = loaddata()
    for p in data["people"]:
        if state1 == "win" or state2 == "lose":
            if p["name"] == name1:
                p["gamesWon"] += 1
                calcWP(data, p)
            elif p["name"] == name2:
                p["gamesLost"] += 1
                calcWP(data, p)
        elif state1 == "lose" or state2 == "win":
            if p["name"] == name1:
                p["gamesLost"] += 1
                calcWP(data, p)
            elif p["name"] == name2:
                p["gamesWon"] += 1
                calcWP(data, p) 
    if state1 == "win":
        await ctx.send("congratulations on your win, "+name1+" and better luck next time "+name2)
    elif state2 == "win":
        await ctx.send("congratulations on your win, "+name2+" and better luck next time "+name1)
    elif state1 == "loss" and state2 == "loss":
        await ctx.send("Both players can't lose. Please fix the command and try again")
    elif state1 == "win" and state2 == "win":
        await ctx.send("Both players can't win. Please fix the command and try again")
    else:
        await ctx.send("Please educate yourself on how to use me by typing $giveCommands :)")


#gives the names of all the players registered
@bot.command(name="getPlayers")
async def getPlayers(ctx):
    names = ""
    index = 0
    data = loaddata()
    for p in data["people"]:
        index+=1
        if(index < len(data["people"])):
            names += p["name"]+", "
        else:
            names += p["name"]
    await ctx.send(names)


@bot.command(name="giveCommands")
async def getHelp(ctx):
    message = ""
    for i in range(int(len(commands))):
        if(i%2==0):
            message += commands[i]+": "+commands[i+1]+"\n"
    message += "-----------------------------------------------\n"
    message += "write $ before every command and your between the command and your input should be a space.\n"
    message += "Every time this bot starts up, players have to be set up.\n"
    await ctx.send(message)

#helper function that loads the json file
def loaddata():
    with open('data.json') as json_file:
        data = json.load(json_file)
        return data

#helper function that writes to the json file (input: json file)
def writedata(data):
    writing = open("data.json", "w")
    json.dump(data, writing)
    writing.close()

#helper function that calculates win % (input: json file to write to, person in question from json file)
def calcWP(data, person):
    person["WP"] = (person["gamesWon"] / (person["gamesWon"] + person["gamesLost"])) * 100
    writedata(data)

bot.run(TOKEN)

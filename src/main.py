from random import randint
from discord.ext import commands
import discord

from discord import Permissions

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 1022192700105179206  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    await ctx.send(ctx.author)    

@bot.command()
async def d6(ctx):
    await ctx.send(randint(1,6))

@bot.event
async def on_message(message):
    if message.content == "Salut tout le monde":
        ping = "Salut tout seul <@" + str(message.author.id) + ">"
        await message.channel.send(ping)
    await bot.process_commands(message)


async def getMemberFromUsername(ctx, username):
    for member in ctx.guild.members:
            if (member.name == username):
                return member

@bot.command()
async def admin(ctx, usernameToPromote=None):
    if not usernameToPromote:
        await ctx.send("Give me the name of the new (potential) admin !")
    else:
        adminRole = None
        for role in ctx.guild.roles: 
            if (str(role) == "Admin"):
                adminRole = role  

        if not adminRole: 
            adminRole = await ctx.guild.create_role(name="Admin",permissions=Permissions.all(), mentionable=True)

        userToPromote = await getMemberFromUsername(ctx, usernameToPromote)
        
        if not userToPromote:
            await ctx.send("This user is not on this server !")
        
        else: 
            await userToPromote.add_roles(adminRole) 
            await ctx.send(str(userToPromote.mention) + " is now" + str(adminRole.mention))
        

@bot.command()
async def ban(ctx, usernameToBan=None):
    if not usernameToBan:
        await ctx.send("Give me the name of the user to ban !")
    else:
        userToBan = await getMemberFromUsername(ctx, usernameToBan)
        
        if not userToBan:
            await ctx.send("This user is not on this server !")
        else: 
            await userToBan.ban(reason = "bye bye looser")
            await ctx.send(str(userToBan.mention) + " is now banned !")


@bot.command()
async def count(ctx):

    dictionnary = {'online': 0, 'offline' : 0, 'idle' : 0, 'dnd' : 0}
    for user in ctx.guild.members:
            dictionnary[str(user.status)]+=1 

   
    await ctx.send("There is " + str(dictionnary['online']) + " online members")


token = ""
bot.run(token)  # Starts the bot
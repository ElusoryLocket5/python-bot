# WARNING!
# You must modify this file to make your bot work properly!
# WARNING!
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="<YOUR_PREFIX_HERE>") # Put your command prefix here
client.remove_command('help')

@client.event
async def on_ready():
    print(f"Bot {client.user} online!") # This is the statement you'll see printed in console when the bot is ready
@client.command()
async def help(ctx):
	embed=discord.Embed(title="List", description="Here the command list", color=0xffb908)
	embed.set_thumbnail(url="<THUMBNAIL>") # Put here the link (ex. imgur) of the tumbnail of the help embed
	embed.add_field(name="!<COMMAND>", value="<DESCRIPTION>", inline=False) # You have to set <COMMAND> and <DESCRIPTION> values manually for each command. You can copy-paste "embed.add_field" to add more commands
	embed.set_footer(text="<MADE_BY>") # You can write what you want here      
	await ctx.send(embed=embed)
  
@client.command(aliases=['purge']) # This command has the "purge" alias. It means that !purge and !clear will be the same command
async def clear(ctx, amount=3): # The default amount of messagges the bot will clear is 3. It means that if you run "!clear" without any argument, it'll purge 3 messagges
    await ctx.channel.purge(limit=(amount + 1))
    await ctx.send(f':white_check_mark: **Cleared {amount} messagges!**', delete_after=15) # The message that says how much messagges were cleared is changeable, and it will delete after 15 seconds by default
# This command was made by RescueTeam#4804	

  
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms!') # Sends your ping in milliseconds
    
@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)


@client.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    await client.process_commands(message)


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has reached level {lvl_end}') # This message is sent in chat when a user reaches a certain level. You can change that
        users[f'{user.id}']['level'] = lvl_end

@client.command()
async def level(ctx, member: discord.Member = None): # This command says by default (whithout any arg(s)) what's your level. If you specify a member mentioning it (ex. "!level @ElusoryLocket5") it'll send pinged member's level
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        embed=discord.Embed(title="LEVEL", description=f'Your level is: {lvl}', color=0xffb908)
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_footer(text=f"Made by...")
        await ctx.send(embed=embed)
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        embed=discord.Embed(title="LEVEL", description=f'{member} level is {lvl}', color=0xffb908)
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_footer(text="Made by...")
        await ctx.send(embed=embed)
       
client.run('TOKEN') 
       
# Comments made by RescueTeam#4804

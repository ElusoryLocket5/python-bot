import discord
from discord.ext import commands

client = commands.Bot(command_prefix="<YOUR_PREFIX_HERE>")
client.remove_command('help')

@client.event
async def on_ready():
    print(f"Bot {client.user} online!")

@client.command()
async def help(ctx):
	embed=discord.Embed(title="List", description="Here the command list", color=0xffb908)
	embed.set_thumbnail(url="<THUMBNAIL>")
	embed.add_field(name="!<COMMAND>", value="<DESCRIPTION>", inline=False)
	embed.set_footer(text="<MADE_BY>")        
	await ctx.send(embed=embed)
  
@client.command(aliases=['purge'])
async def clear(ctx, amount=3):
    await ctx.channel.purge(limit=(amount + 1))
    await ctx.send(f':white_check_mark: **Cleared {amount} messagges!**', delete_after=15)
# Made by RescueTeam#4804	

  
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms!')
    
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
        await message.channel.send(f'{user.mention} has reached level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end

@client.command()
async def level(ctx, member: discord.Member = None):
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
       

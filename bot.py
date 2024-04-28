import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import MY_TOKEN

# Set up bot prefix
bot_prefix = "!"
driver = webdriver.Chrome()

# Define Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# Create a bot instance with a command prefix and Intents
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

# Command: Hello
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')

@bot.command(name='score')
async def score(ctx, team_name: str, week: str):
    team = team_name.upper()
    game_list = []
    playoff = False
    found = False

    if week == "wc":
        url = "https://www.foxsports.com/scores/nfl?seasonType=post&week=1"
        playoff = True
    elif week == "div":
        url = "https://www.foxsports.com/scores/nfl?seasonType=post&week=2"
        playoff = True
    elif week == "cnf":
        url = "https://www.foxsports.com/scores/nfl?seasonType=post&week=3"
        playoff = True
    elif week == "sb":
        url = "https://www.foxsports.com/scores/nfl?seasonType=post&week=4"
        playoff = True
    else:
        url = "https://www.foxsports.com/scores/nfl?seasonType=reg&week=" + week

    try:
        driver.get(url)
        games = driver.find_elements(By.XPATH, '//div[@class="teams"]')
        if playoff:
            games = driver.find_elements(By.XPATH, '//div[@class="score-chip-playoff-content"]')

        for game in games:
            game_info = game.text.splitlines()
            game_list.append(game_info)

    finally:
        driver.quit()

    for game in game_list:
        if team in game:
            found = True
            if int(game[2]) > int(game[5]):
                await ctx.send(f"{game[0]} won {game[2]} to {game[5]} against the {game[3]}")
            elif int(game[2]) < int(game[5]):
                await ctx.send(f"{game[3]} won {game[5]} to {game[2]} against the {game[0]}")
            else:
                await ctx.send(f"{game[0]} tied {game[2]} to {game[5]} with the {game[3]}")

# Run the bot with the token
bot.run(MY_TOKEN)

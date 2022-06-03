import discord
import random
import os
import constants
import googletrans
from gnews import GNews
from discord.ext import commands
from discord.commands import OptionChoice
from discord.commands import Option

bot = commands.Bot(intents=discord.Intents.all(), help_command=None)


@bot.slash_command(name='hi', description="Greets the user.", guild_ids=[os.environ.get('GUILD_ID')])
async def _sayhi(ctx: discord.ApplicationContext):
    await ctx.respond(random.choice(constants.GREETINGS))


@bot.slash_command(name='fcbnews', description="Shows actual news of FC Bayern.", guild_ids=[os.environ.get('GUILD_ID')])
async def _bayernmuenchenfacts(ctx: discord.ApplicationContext):
    google_news = GNews(max_results=10)
    bayernmuenchen_news = google_news.get_news('Bayern Munich match, transfer')
    randomised_url = bayernmuenchen_news[random.randint(0, 9)]['url']
    description = google_news.get_full_article(randomised_url).title
    embed = discord.Embed(title="Bayern Nachrichten!!!",
                          url=randomised_url,
                          description=description,
                          color=discord.Color.blue())
    embed.set_thumbnail(
        url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg/1200px-FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg.png")
    await ctx.respond(embed=embed)


@bot.slash_command(name='translate', description="Translates the message into the selected language.", guild_ids=[os.environ.get('GUILD_ID')])
async def _translate(ctx: discord.ApplicationContext,language: OptionChoice(value=["en", "de"]), text: Option(str, "Enter text to translate.")):
    if language != "en" and language != "de":
        await ctx.respond("Sehe ich aus, als könnte ich Französisch sprechen?")
    else:
        # the actual text, removing the language from the text
        translator = googletrans.Translator()
        translated_text = translator.translate(
            text, dest=language).text
        await ctx.respond(translated_text)


@bot.slash_command(name='bavarian',description="Tells about bavarian life.",guild_ids=[os.environ.get('GUILD_ID')])
async def _livelikeabavarian(ctx: discord.ApplicationContext):
    actual_list = list(constants.BAVARIAN_TO_DO_LIST)
    random_key = random.choice(actual_list)
    randomised_url = constants.BAVARIAN_TO_DO_LIST[random_key]
    embed = discord.Embed(
        title=random_key, url=randomised_url, color=discord.Color.blue())
    await ctx.respond(embed=embed)


@bot.slash_command(name="commands", description="Sends all available commands.", guild_ids=[os.environ.get('GUILD_ID')])
async def _help(ctx: discord.ApplicationContext):
    embed = discord.Embed(title=f'Available Commands:', description='\uFEFF',
                          colour=ctx.author.colour)
    for command in bot.application_commands:
        embed.add_field(name=f"{command}", value=command.description)
    await ctx.respond(embed=embed)


bot.run(os.environ.get('DISCORD_TOKEN'))

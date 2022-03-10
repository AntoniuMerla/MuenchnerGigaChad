import discord
import random
import time
import asyncio
# import requests
import json
import os
from urllib.request import urlopen
# import redis
import googletrans
from gnews import GNews
#import youtube_dl
from discord.ext import commands

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    for s in commands:
        if (message.content.startswith(s)):
            await commands[s](message)
            break


# greetings
async def sayhi(message):
    await message.reply(random.choice(greetings))


greetings = [
    "Servus!",
    "Hallo!",
    "Wie geht's?",
    "Guten Tag!",
    "Gruß Gott!"
]


# Bayern München facts
async def bayernmuenchenfacts(message):
    google_news = GNews(max_results=10)
    bayernmuenchen_news = google_news.get_news('Bayern Munich match, transfer')
    randomised_url = bayernmuenchen_news[random.randint(0, 9)]['url']
    description = google_news.get_full_article(randomised_url).title
    embed = discord.Embed(title="Bayern Nachrichten!!!",
                          url=randomised_url,
                          # url="https://fcbayern.com/en/news",
                          description=description,
                          color=discord.Color.blue())
    embed.set_thumbnail(
        url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg/1200px-FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg.png")
    await message.channel.send(embed=embed)


# translation - reverso XD, update: actually, not
async def translate(message):
    length = len(".translate")
    # removing the command from the text
    text_to_be_translated = message.content[length:]
    language_to = text_to_be_translated[1:3].lower()
    if language_to != "en" and language_to != "de":
        await message.reply("Sehe ich aus, als könnte ich Französisch sprechen?")
    else:
        # the actual text, removing the language from the text
        text_to_be_translated = text_to_be_translated[4:]
        translator = googletrans.Translator()
        translated_text = translator.translate(text_to_be_translated, dest=language_to).text
        await message.reply(translated_text)


# Bavarian life-style
async def livelikeabavarian(message):
    actual_list = list(bavarian_to_do_list)
    random_key = random.choice(actual_list)
    randomised_url = bavarian_to_do_list[random_key]
    embed = discord.Embed(title=random_key, url=randomised_url, color=discord.Color.blue())
    await message.reply(embed=embed)


bavarian_to_do_list = {
    "A Pretzel a day keeps the hunger away!": "https://en.wikipedia.org/wiki/Pretzel",
    "Berliner, was ist das? Slap some bayerische Leberkäse onto your plate": "https://www.kitchenstories.com/en/recipes/bavarian-meatloaf-with-potato-salad",
    "Regensburger, Presskopf, Gelbwurstbrot, Weißwürste oder Bratwurst? Can't decide...": "https://www.tasteatlas.com/most-popular-sausages-in-bavaria",
    "Drink beer like it's Oktoberfest!": "https://www.tasteatlas.com/most-popular-beers-in-bavaria",
    "Lederhosen is love, Lederhosen is life": "https://www.ebay.de/itm/264775398504?_trkparms=amclksrc%3DITM%26aid%3D1110002%26algo%3DSPLICE.SOI%26ao%3D1%26asc%3D237167%26meid%3D5de15833fa214b279a5c71562fa0e9cb%26pid%3D101196%26rk%3D1%26rkt%3D12%26sd%3D254569794654%26itm%3D264775398504%26pmt%3D1%26noa%3D0%26pg%3D2047675%26algv%3DPromotedSellersOtherItemsV2WithMLRv3&_trksid=p2047675.c101196.m2219&amdata=cksum%3A2647753985045de15833fa214b279a5c71562fa0e9cb%7Cenc%3AAQAGAAACAAL%252FCBQK5lCQXlXa8u2ZLegtf806g2LWS5qggo4inSE3YBp8fpUtGkvenjVYcvRhLBkq4ilskxNU0IfM503JrL07gJDYcZmknygnREReDoUKbJV04qyaGTOqb7ul%252Fa9KRK%252BQQ7YxmKGZ%252B7O2wEzRo%252FO6Dqpmmj3fULvk7D5OWi19aT2vnGsr7tQBamkgn5MzHYz2%252FO8zHeDmuINa%252F%252FAyFSnruBqvVjCs1R5VTyNH103q70w4SKZvWQH%252Fl%252FU3BeufwNGsOcn2%252B99yRXcUUvD89erKuTirXJE%252BTSuuf9MK1OTvVvDouKaYtnPWc6q40uoNrF%252B8A923My0K57ambcDF%252FaNTl1IeD5JqZBuHyz4VJxGFt3JWVarp94giGPJHglfQVtGfzodt8kRuRnJqEWEhIfmG9X3Gq5fhiCGbnYC4KtJRzPLWQn5JaqETiQFOQWm0ocXq3qu%252B8lz6ZCeA%252FqMrAapaIrDQ7K0WxZuIajMX5Oh%252Fblhxw8T9QMsWkO6wdY6yT2WuZMelRIDhVxD%252BSwkGMY7BRiUcXAZ2v6ZIs2sxSSH0VWKng7cYJ1hb7CBT48VFOP7gDOj2ak9eXJljTzNh8g4ys6thYVzp%252BgrabdB8dBgu%252BMdBFlgbTM0Ny75jfmHf0EXRpMAk%252BhuuRCS4%252Bs%252F4%252B4YKOLvLVMwmqB7bKqZ2a%252FFJ%7Campid%3APL_CLK%7Cclp%3A2047675",
    "Dubste-what? Kid, culturalise yourself! Go to the Bayeruth Festival!": "https://www.bayreuther-festspiele.de/en/",
    "Kind: Papa, can we go to Disneyland? \n Papa: Nein, we have Disneyland at home \n Disneyland at home: (insert image of Neuschwanstein Castle)": "https://www.neuschwanstein.de/englisch/tourist/admiss.htm"
}


# for yodelling


# List of commands
async def listofcommands(message):
    result = "List of commands: \n"
    for s in commands:
        result = result + s + "\n"
        if s == ".translate":
            result = result + "(i.e.: .translate en Arbeiterunfallverischerungsgesetz OR .translate de the backer is not here)" + "\n"
    await message.channel.send(result)


commands = {
    '.sayhi': sayhi,
    '.bayernmuenchenfacts': bayernmuenchenfacts,
    '.translate': translate,
    '.livelikeabavarian': livelikeabavarian,
    '.listofcommands': listofcommands,
    # '.yodel': yodel
}

# client.run(token)
client.run(os.environ.get('DISCORD_TOKEN'))

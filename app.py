import asyncio
import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

choices = ['Rock', 'Paper', 'Scissors']


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$RPS' or '$RockPaperScissors'):
        await message.reply('Pick: Rock, Paper, or Scissors', mention_author=True)

        # not entirely sure the purpose of m here, I believe It's if multiple users, id have to do more testing
        def check(m):
            return m.author == message.author and m.content

        bot_choice = random.choice(choices)

        try:
            game = await client.wait_for('message', check=check, timeout=5.0)
        except asyncio.TimeoutError:
            return await message.channel.send(f'Sorry, you took too long. I chose {bot_choice}')

        if check:
            await message.channel.send(f'DEBUG: TRUE {bot_choice}, {game.content}')
        elif not check:
            await message.channel.send(f'DEBUG: FALSE {bot_choice}, {game.content}')
        else:
            await message.channel.send(f'DEBUG: How did u get here? {bot_choice}, {game.content}')

        # Tie
        if game.content == bot_choice:
            await message.channel.send(f'TIE! We both picked {bot_choice}')
        # Player picks rock
        elif game.content == choices[0]:
            if bot_choice == choices[1]:
                await message.channel.send(f'YOU LOSE! {bot_choice} beats {game.content}')
            elif bot_choice == choices[2]:
                await message.channel.send(f'YOU WIN! {game.content} beats {bot_choice}')
        # Player picks paper
        elif game.content == choices[1]:
            if bot_choice == choices[0]:
                await message.channel.send(f'YOU WIN! {game.content} beats {bot_choice}')
            elif bot_choice == choices[2]:
                await message.channel.send(f'YOU LOSE! {bot_choice} beats {game.content}')
        # Player picks scissors
        elif game.content == choices[2]:
            if bot_choice == choices[0]:
                await message.channel.send(f'YOU LOSE! {bot_choice} beats {game.content}')
            elif bot_choice == choices[1]:
                await message.channel.send(f'YOU WIN! {game.content} beats {bot_choice}')


client.run(os.getenv('TOKEN'))
# error getting ssl cert (_ssl.c:1122)

# ideas:
# chat logging
# chat cleanup
# game? tictactoe? bingo game based on words in chat - dans idea?
# reaction roles

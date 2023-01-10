import asyncio
import os
import random

import discord
from dotenv import load_dotenv

choices = ['Rock', 'Paper', 'Scissors']


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print("----------")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('$hello'):
            await message.reply('Hello!', mention_author=True)

        if message.content.startswith('$RPS'):
            await message.reply('Pick: Rock, Paper, or Scissors', mention_author=True)
            print(f'{message.author} started a game of RPS')

            bot_choice = random.choice(choices)

            def check_game_user(m):
                return m.author == message.author and m.content

            try:
                game = await client.wait_for('message', check=check_game_user, timeout=10.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long. I chose {bot_choice}')

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
            else:
                await message.channel.send(f'{game.content} is not a valid option, check your spelling! Ending Game...')


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(os.getenv('TOKEN'))

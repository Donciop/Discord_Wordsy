import discord  # main packages
from discord.ext import commands
import random
import os
import json  # utility packages

intents = discord.Intents().all()
intents.members = True
client = commands.Bot(command_prefix='*', intents=intents, help_command=None)


@client.command()
async def wordle(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me
    letters = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p",
               "a", "s", "d", "f", "g", "h", "j", "k", "l",
               "z", "x", "c", "v", "b", "n", "m"]
    used_words = []
    final_string = [':black_large_square:', ':black_large_square:', ':black_large_square:', ':black_large_square:', ':black_large_square:']
    list_of_strings = [final_string, final_string, final_string, final_string, final_string, final_string]
    with open('JsonData/words_dictionary.json') as wordle_file:
        wordle_file_dict = wordle_file.read()
        wordle = json.loads(wordle_file_dict)
        wordle_file.close()
    wordle_word = random.choice(list(wordle.keys()))
    iterator = 1
    while True:
        if iterator == 7:
            await ctx.send(f"You didn't make it :( The word was: {wordle_word}")
            return
        await ctx.send(f"Guess the word! (5 letters) {iterator} / 6 tries")
        msg = await client.wait_for('message', check=check)
        if any(char.isdigit() for char in msg.content):
            await ctx.send("Word cannot contain numbers!")
            continue
        if len(msg.content) < 5:
            await ctx.send(f"Word's too short ({len(msg.content)} / 5 letters)")
            continue
        if len(msg.content) > 5:
            await ctx.send(f"Word's too long ({len(msg.content)} / 5 letters)")
            continue
        if msg.content in used_words:
            await ctx.send("You've already used that word!")
            continue
        typed_word = str(msg.content)
        if typed_word not in wordle:
            await ctx.send("Word's not in dictionary")
            continue
        used_words.append(str(msg.content))
        for index, typed_letter in enumerate(typed_word):
            if typed_letter == wordle_word[index]:
                final_string[index] = ':green_square:'
                try:
                    letters[letters.index(typed_letter)] = f'**{typed_letter}**'
                except:
                    continue
            elif typed_letter in wordle_word:
                final_string[index] = ':yellow_square:'
                try:
                    letters[letters.index(typed_letter)] = f'**{typed_letter}**'
                except:
                    continue
            else:
                final_string[index] = ':black_large_square:'
                try:
                    letters[letters.index(typed_letter)] = f' '
                except:
                    continue
        final_letters = letters.copy()
        for lower_letter in final_letters:
            final_letters[final_letters.index(lower_letter)] = lower_letter.upper()
        await ctx.send(f"""
        {final_string[0]} {final_string[1]} {final_string[2]} {final_string[3]} {final_string[4]}\n\n{final_letters[0]} {final_letters[1]} {final_letters[2]} {final_letters[3]} {final_letters[4]} {final_letters[5]} {final_letters[6]} {final_letters[7]} {final_letters[8]} {final_letters[9]}\n    {final_letters[10]} {final_letters[11]} {final_letters[12]} {final_letters[13]} {final_letters[14]} {final_letters[15]} {final_letters[16]} {final_letters[17]} {final_letters[18]}\n       {final_letters[19]} {final_letters[20]} {final_letters[21]} {final_letters[22]} {final_letters[23]} {final_letters[24]} {final_letters[25]}
        """)
        if final_string == [':green_square:', ':green_square:', ':green_square:', ':green_square:', ':green_square:']:
            await ctx.send(f"You won! The word is: {wordle_word}")
            return
        iterator += 1

client.run(os.getenv('TOKEN'))

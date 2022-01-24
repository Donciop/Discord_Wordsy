import discord  # main packages
from discord.ext import commands
import random  # utility packages
import os
import json

intents = discord.Intents().all()  # Making sure the bot has all the permissions
intents.members = True
client = commands.Bot(command_prefix='*', intents=intents, help_command=None)  # Initialize bot


@client.event
async def on_ready():
    """ Event handler that is called when bot is turned on. """
    print("Bot's ready")
    await client.change_presence(  # change the bot's description on Discord member list
        activity=discord.Activity(
            type=discord.ActivityType.watching,  # get the "is watching ..." format
            name="*wordsy to start!"
        )
    )


@client.command()
@commands.max_concurrency(1, commands.BucketType.user)  # allow only one instance of that command running at the time
async def wordsy(ctx):
    # making sure the bot only accepts responses from author of command in current channel
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me
    # initialize lists that will be used later to store information
    letters = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p",
               "a", "s", "d", "f", "g", "h", "j", "k", "l",
               "z", "x", "c", "v", "b", "n", "m"]
    used_words = ['', '', '', '', '', '']
    final_string = [
            [':black_square_button:', ':black_square_button:', ':black_square_button:', ':black_square_button:', ':black_square_button:'],
            [':black_square_button:', ':black_square_button:', ':black_square_button:', ':black_square_button:', ':black_square_button:'],
            [':black_square_button:', ':black_square_button:', ':black_square_button:', ':black_square_button:', ':black_square_button:'],
            [':black_square_button:', ':black_square_button:', ':black_square_button:', ':black_square_button:', ':black_square_button:'],
            [':black_square_button:', ':black_square_button:', ':black_square_button:', ':black_square_button:', ':black_square_button:'],
            [':black_square_button:', ':black_square_button:', ':black_square_button:', ':black_square_button:', ':black_square_button:']
        ]
    winning_string = [':green_square:', ':green_square:', ':green_square:', ':green_square:', ':green_square:']
    with open('JsonData/words_dictionary.json') as wordle_file:  # getting our dictionary from .json file
        wordle_file_dict = wordle_file.read()
        wordle = json.loads(wordle_file_dict)
        wordle_file.close()
    wordle_word = random.choice(list(wordle.keys()))  # choosing random word from the dictionary
    iterator = 1
    while True:
        if iterator == 7:  # check if we still have tries
            await ctx.send(f"You didn't make it :( The word was: {wordle_word}")
            return
        await ctx.send(f"Guess the word! (5 letters) {iterator} / 6 tries")
        # wait for user's response and check channel and author of the command
        msg = await client.wait_for('message', check=check)
        if any(char.isdigit() for char in msg.content):  # check if passed string doesn't have any digits in it
            await ctx.send("Word cannot contain numbers!")
            continue
        if len(msg.content) < 5:  # check if passed string have correct length
            await ctx.send(f"Word's too short ({len(msg.content)} / 5 letters)")
            continue
        if len(msg.content) > 5:
            await ctx.send(f"Word's too long ({len(msg.content)} / 5 letters)")
            continue
        if msg.content in used_words:  # check if the word has been used before
            await ctx.send("You've already used that word!")
            continue
        typed_word = str(msg.content).lower()  # make sure we're working on lowercase letters
        if typed_word not in wordle:  # check if word from user's response is in dictionary
            await ctx.send("Word's not in dictionary")
            continue
        used_words[iterator-1] = str(msg.content)  # store passed word in list to print it later
        for index, typed_letter in enumerate(typed_word):  # iterate over every letter in passed word
            # if the letter's and it's position is correct, we assign green square to this position
            if typed_letter == wordle_word[index]:
                final_string[iterator-1][index] = ':green_square:'
                try:
                    letters[letters.index(typed_letter)] = f'**{typed_letter}**'  # here we bold the correct letter
                except:
                    continue
            # if the letter's correct but in wrong position, we assign yellow square to this position
            elif typed_letter in wordle_word:
                final_string[iterator-1][index] = ':yellow_square:'
                try:
                    letters[letters.index(typed_letter)] = f'**{typed_letter}**'
                except:
                    continue
            # if the letter's wrong, we assign black square to this position
            else:
                final_string[iterator-1][index] = ':black_large_square:'
                try:
                    letters[letters.index(typed_letter)] = f' '  # here we remove the letter from the keyboard
                except:
                    continue
        # here we uppercase the letters to make them more readable
        final_letters = letters.copy()
        for lower_letter in final_letters:
            final_letters[final_letters.index(lower_letter)] = lower_letter.upper()
        # the final message that is sent every iteration of the while loop contains every squares and whole keyboard
        await ctx.send(f"{final_string[0][0]} {final_string[0][1]} {final_string[0][2]} {final_string[0][3]} {final_string[0][4]}   {used_words[0].upper()}\n\n"
                       f"{final_string[1][0]} {final_string[1][1]} {final_string[1][2]} {final_string[1][3]} {final_string[1][4]}   {used_words[1].upper()}\n\n"
                       f"{final_string[2][0]} {final_string[2][1]} {final_string[2][2]} {final_string[2][3]} {final_string[2][4]}   {used_words[2].upper()}\n\n"
                       f"{final_string[3][0]} {final_string[3][1]} {final_string[3][2]} {final_string[3][3]} {final_string[3][4]}   {used_words[3].upper()}\n\n"
                       f"{final_string[4][0]} {final_string[4][1]} {final_string[4][2]} {final_string[4][3]} {final_string[4][4]}   {used_words[4].upper()}\n\n"
                       f"{final_string[5][0]} {final_string[5][1]} {final_string[5][2]} {final_string[5][3]} {final_string[5][4]}   {used_words[5].upper()}\n\n"
                       f"{final_letters[0]} {final_letters[1]} {final_letters[2]} {final_letters[3]} {final_letters[4]} {final_letters[5]} {final_letters[6]} {final_letters[7]} {final_letters[8]} {final_letters[9]}\n"
                       f"    {final_letters[10]} {final_letters[11]} {final_letters[12]} {final_letters[13]} {final_letters[14]} {final_letters[15]} {final_letters[16]} {final_letters[17]} {final_letters[18]}\n"
                       f"       {final_letters[19]} {final_letters[20]} {final_letters[21]} {final_letters[22]} {final_letters[23]} {final_letters[24]} {final_letters[25]}"
                       )
        if winning_string in final_string:  # winning condition
            await ctx.send(f"You won! The word is: {wordle_word}")
            return
        iterator += 1


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MaxConcurrencyReached):  # called when you don't have permission to use that command.
        await ctx.send(f"{ctx.author.mention}, finish the game before starting new one!")
        return

client.run(os.getenv('TOKEN'))

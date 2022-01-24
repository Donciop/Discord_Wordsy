# Discord Wordsy
Discord Bot that imitates a popular web game "Wordle".

## Playing the game
The rules are simple, you have 6 chances to guess the 5 letters word.

![image](https://user-images.githubusercontent.com/39534836/150879029-0a0d0d14-d9a6-4177-99ac-28cf96131c82.png)

Each time you will know if the letter is in right place (green square) or if the letter is correct, but in wrong place (yellow square).
The word is chosen from all the 5 letters words in British dictionary.

Under the squares, there is keyboard that shows which characters are used or which characters aren't in the final word.
![image](https://user-images.githubusercontent.com/39534836/150879438-6f49664c-830b-4481-aca9-c3ccfb4a45d4.png)

## Tech used
This simple Discord Bot uses:
- [Discord.py](https://github.com/Rapptz/discord.py) - A modern, easy to use, feature-rich, and async ready API wrapper for Discord written in Python.
- [Heroku](https://dashboard.heroku.com/apps) - A platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

## Code example
Simple user's response check to prevent digits or already used words to be passed to the game.
```sh
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
typed_word = str(msg.content).lower()
if typed_word not in wordle:
    await ctx.send("Word's not in dictionary")
    continue
```

## Adding bot to your server

You can add this bot directly to your Discord server here: [Add me!](https://discord.com/api/oauth2/authorize?client_id=934989894995021866&permissions=101376&scope=bot) or you can join our [Discord server](https://discord.gg/e5daMkFVJP) directly to maybe ask some questions!

However, this bot is not fully configured for being on multiple servers. It's still in early development. If you really want this bot on your Discord server, feel free to contact me on our Discord server.

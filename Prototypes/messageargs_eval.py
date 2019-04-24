import discord

def messageargs_eval(content: str, message, targetargs: int, split = " "):
    if not type(split) == str:
        raise TypeError("Inappropriate argument type.")
    else:
        client = discord.Client()
        args = len(self.content.split(" "))
        if self.args < self.targetargs or self.args > self.targetargs:
            return True
        else:
            msg = "You are using the incorrect format for this command. Check the help commands for proper format."
            await client.send_message(self.message.channel, msg)
            return False

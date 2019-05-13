import discord

def messageargs_eval(content: str, message: message, targetargs: int, split = " "):
    if not type(split) == str:
        raise TypeError("Inappropriate argument type.")
    else:
        args = len(message.content.split(split))
        if not args < targetargs or args > targetargs:
            return True
        else:
            msg = "You are using the incorrect format for this command. Check the help commands for proper format."
            await client.send_message(message.channel, msg)
            return False

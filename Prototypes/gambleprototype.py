import random

  #gamble command
  if message.content.upper ().startswith == "E!GAMBLE":
  		args = message.content.split
      numcredits = intify(args[1])
      #checks if the number of emus gambled is less than or equal to zero
      if numcredits > get_value(message.author.id, 'credits'):
          msg = "You don't have that number of credits to gamble!"
          await client.send_message(message.channel, msg)
        #checks is user has that many credits to gamble
      elif numemus <= 0:
          msg = "You can't gamble that number of credits!"
          await client.send_message(message.channel, msg)
      else:
          #chances of winning: 1 in 3
          creditcalnum = numemus * 2
          gamble = random.randint(1,3)
          msg = "Input a number between 1 and 3" 
          #winning outcome outcome
          if message.content ()startswith == int (gamble):
              user_add_value(message.author.id, creditcalnum, "credits")
              msg = "You won! You now have " + str('credits') + " credits!"
              await client.send_message(message.channel, msg) 
          #losing outcome
          elif message.content ()startswith == "1" and gamble != 1 or message.content ()startswith == "2" and gamble != 2 or message.content ()startswith == "3" and gamble != 3:
                  user_add_value(message.author.id, -get_value(message.author.id, "credits"), "credits")
                  msg = "You lost, sorry... :("
                  await client.send_message(message.channel, msg)
          else
              msg = "Invalid number."

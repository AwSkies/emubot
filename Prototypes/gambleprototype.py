import random

  #gamble command
  if message.content.upper ().startswith == "E!GAMBLE":
  		args = message.content.split
      numemus = intify(args[1])
      #checks if the number of emus gambled is less than or equal to zero
      if numemus > get_value(message.author.id, 'emustorage'):
          msg = "You don't have that number of emus to gamble!"
          await client.send_message(message.channel, msg)
        #checks is user has that many emus to gamble
      elif numemus <= 0:
          msg = "You can't gamble that number of emus!"
          await client.send_message(message.channel, msg)
      else:
          gamble = random.randint(0,9)
          #losing outcome
          if gamble <= 4:
              user_add_value(message.author.id, -numemus, "emustorage")
              msg = "You lost, sorry... :("
              await client.send_message(message.channel, msg) 
          else:
              #big winning outcome
              if gamble >=8:    
                  emucalnum = numemus * 2
              elif gamble > 4 and <= 7:
                  emucalnum = numemus * 1.5
                  emucalnum = int(emucalnum)
              fullemus = maxemus - get_value(message.author.id, "emudefense")
              #if the number of emus goes over the limit
              if emucalnum > fullemus:
                  user_add_value(message.author.id, -get_value(message.author.id, "emustorage"), "emustorage")
                  user_add_value(message.author.id, fullemus, "emustorage")
                  msg = "You won! You now have " + str(fullemus) + " emus in storage!"
                  await client.send_message(message.channel, msg)
              else:
                  user_add_value(message.author.id, numemus, "emustorage")
                  msg = "You won! You gained " + str(numemus) + " emus!"
                  await client.send_message(message.channel, msg)

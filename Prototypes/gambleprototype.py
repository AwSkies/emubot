
  #gamble command------------------------------------------------------------------
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
          def dicepicker():
            dicenum = random.randint(1,6)
            if dicenum == 1:
                diceface = 'dice1'
            elif dicenum == 2:
                diceface = 'dice2'
            elif dicenum == 3:
                diceface = 'dice3'
            elif dicenum == 4:
                diceface = 'dice4'
            elif dicenum == 5:
                diceface = 'dice5'
            elif dicenum == 6:
                diceface = 'dice6'
            return(diceface)
          gamble = random.randint(0,9)
          #losing outcome
          if gamble <= 4:
              outcome = 'lost'
              user_add_value(message.author.id, -numemus, "emustorage")
          else:
              #big winning outcome
              if gamble >= 8:
                  emucalnum = numemus * 2
              #medium winning outcome
              elif gamble > 4 and <= 7:
                  emucalnum = numemus * 1.5
                  emucalnum = int(emucalnum)
              fullemus = maxemus - get_value(message.author.id, "emudefense")
              #if the number of emus goes over the limit
              if emucalnum > fullemus:
                  user_add_value(message.author.id, -get_value(message.author.id, "emustorage"), "emustorage")
                  user_add_value(message.author.id, fullemus, "emustorage")
              else:
                  user_add_value(message.author.id, numemus, "emustorage")
              outcome = 'won'
          msg = 'Rolling the dice...' + dicepicker() + dicepicker()
          edit = await client.send_message(message.channel, msg)
          await asyncio.sleep(1)
          edited = 'Rolling the dice...' + dicepicker() + dicepicker()
          await client.edit_message(edit, edited)
          await asyncio.sleep(1)
          edited = 'Rolling the dice...' + dicepicker() + dicepicker()
          await client.edit_message(edit, edited)
          await asyncio.sleep(1)
          #makes outcome
          if outcome == 'lost': 
              edited = 'You lost, sorry... :('
              await client.edit_message(edit, edited) 
          elif outcome == 'won':
              edited = 'You won! you now have `{}` emus in storage!'.format(get_value(message.author.id, 'emustorage'))
              await client.edit_message(edit, edited)

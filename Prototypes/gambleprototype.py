
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
          msg = 'Rolling the dice...' + dicepicker1 + dicepicker2
          edit = await client.send_message(message.channel, msg)
          await asyncio.sleep(1)
          edited = 'Rolling the dice...' + dicepicker1 + dicepicker2
          await client.edit_message(edit, edited)
          await asyncio.sleep(1)
          edited = 'Rolling the dice...' + dicepicker1 + dicepicker2
          await client.edit_message(edit, edited)
          await asyncio.sleep(1)
          #makes outcome
          if outcome == 'lost': 
              edited = 'You lost, sorry... :('
              await client.edit_message(edit, edited) 
          elif outcome == 'won':
              edited = 'You won! you now have `{}` emus in storage!'.format(get_value(message.author.id, emustorage))
              await client.edit_message(edit, edited)

    def dicepicker1():
        dicenum = random.randint(1,6)
        if dicenum == 1:
            diceface = <insert dice emoji here>
        elif dicenum == 2:
            diceface = <insert dice emoji here>
        elif dicenum == 3:
            diceface = <insert dice emoji here>
        elif dicenum == 4:
            diceface = <insert dice emoji here>
        elif dicenum == 5:
            diceface = <insert dice emoji here>
        elif dicenum == 6:
            diceface = <insert dice emoji here>
        return(diceface)

    def dicepicker2():
        dicenum2 = random.randint(1,6)
        if dicenum2 == 1:
            diceface2 = <insert dice emoji here>
        elif dicenum2 == 2:
            diceface2 = <insert dice emoji here>
        elif dicenum2 == 3:
            diceface2 = <insert dice emoji here>
        elif dicenum2 == 4:
            diceface2 = <insert dice emoji here>
        elif dicenum2 == 5:
            diceface2 = <insert dice emoji here>
        elif dicenum2 == 6:
            diceface2 = <insert dice emoji here>
        return(diceface2)


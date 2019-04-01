import datetime

loanstarttime = dict()

    #loan command------------------------------------------
    if message.content.upper () == "E!LOAN":
        loanstarttime[message.author] = int(datetime.datetime.today().strftime('%j')
        

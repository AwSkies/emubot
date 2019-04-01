import datetime

loanstartday = dict()

    #loan command------------------------------------------
    if message.content.upper () == "E!LOAN":
        loanstartday[message.author] = int(datetime.datetime.today().strftime('%j')
        

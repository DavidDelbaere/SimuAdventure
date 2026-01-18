import time
from dine import fetch

def geminiPrompt(geminiNeededResponse):

    match geminiNeededResponse:
        case 1:
            #button button
            while(fetch[0] != 1):
                time.sleep(0.5)
                return(geminiNeededResponse)
            return "I have pressed the button."
        
        case 2:
            #lights button
            while(fetch[1] != 1):
                time.sleep(0.5)
                return(geminiNeededResponse)
            return "I have turned the lights on."
        
        case 3:
            #heat button
            while(fetch[2] != 1):
                time.sleep(0.5)
                return(geminiNeededResponse)
            return "I have heated the object up."
        
        #default case
        case _:
            return 'invalid request type'
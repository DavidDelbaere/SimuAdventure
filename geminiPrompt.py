'''import time
from dine import fetch

def geminiPrompt(geminiNeededResponse):
    grine = fetch()
    match geminiNeededResponse:
        case 1:
            #button button
            while((int)(grine[1]) != 1):
                time.sleep(0.5)
                return geminiPrompt(geminiNeededResponse)
            return "I have pressed the button."
        
        case 2:
            #lights button
            while((int)(grine[4]) != 1):
                time.sleep(0.5)
                return geminiPrompt(geminiNeededResponse)
            return "I have turned the lights on."
        
        case 3:
            #heat button
            while((int)(grine[7]) != 1):
                time.sleep(0.5)
                return geminiPrompt(geminiNeededResponse)
            return "I have heated the object up."
        
        #default case
        case _:
            return 'invalid request type'
            '''

import time
from dine import fetch

def geminiPrompt(geminiNeededResponse):
    while True:
        grine = fetch()

        match geminiNeededResponse:
            case 1:
                if int(grine[1]) == 1:
                    return "I have pressed the button."

            case 2:
                if int(grine[4]) == 1:
                    return "I have turned the lights on."

            case 3:
                if int(grine[7]) == 1:
                    return "I have heated the object up."

            case _:
                return "invalid request type"

        time.sleep(0.1)
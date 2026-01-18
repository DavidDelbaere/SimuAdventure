def geminiPrompt(geminiNeededResponse):
    
    match geminiNeededResponse:
        case 1:
            return "I have moved."
        
        case 2:
            return "I have heated up the requested thing."
        
        case 3:
            return "I have cooled down the requested thing."
        
        case 4:
            return "I have pushed the requested button."
        
        #default case
        case _:
            return 'invalid request type'
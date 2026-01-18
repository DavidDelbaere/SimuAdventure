def keyRequest(i):
    #determine which key should be used (goes to next after 20 uses)
    i = (int)((i-i%20)/20)

    keys = open('keys.txt', 'r').readlines()

    return keys[i]
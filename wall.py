#!/usr/bin/python
import os, sys, string, random, hashlib, time, http.client

#  **************************
#  **************************
#  ***                    ***
#  ***  BBSlink.net Wall  ***
#  ***                    ***
#  **************************
#  **************************
#  
#  PLEASE DO NOT DISTRIBUTE THIS FILE
#  ==================================
#  
#  Version 0.1.beta  13th December 2015
#  Version 0.2.beta  1st August 2023 - Updated to Python3
#
#  (C)2015 Christopher Taylor. All Rights Reserved.
#  of Dogtown BBS :: BBS.KIWI.NET
#
#  Insert your system's BBSlink.net log in credentials between the "" below:

#  Mystic BBS Configuration:
#  Command: (D-) Exec door (no dropfile)
#     Data: /mystic/scripts/wall.py %# %U
#

host = "games.bbslink.net" # Server address, usually 'games.bbslink.net'
syscode = "" # Your system code
authcode = "" # Your system's authorisation code
schemecode = "" # Scheme code

if len(sys.argv) < 3:
    sys.exit(1)

userno = sys.argv[1]
username = sys.argv[2]

dg = "[0;40;30m"
red = "[0;40;31m"
gray = "[0;40;0m"
white = "[0;40;37m"

os.system("stty echo")
clear = lambda: os.system('clear')

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def getMD5Hash(s):
    #m = md5.new()
    #m.update(s)
    #rv = m.hexdigest()

#   m = hashlib.md5(s)
#   rv = m.hexdigest()
    m = hashlib.md5()
    m.update(s.encode())
    rv = m.hexdigest()

    return rv

def ShowWall():
    # Show splash
    clear()
    print(red + "Reading the wall...")

    wall = os.system('/usr/bin/curl -s "http://games.bbslink.net/wall.php?action=show"')
    return wall


    ### DONT USE THIS CODE ANYMORE

    # Get ANSI text from BBSlink server
    h1 = http.client.HTTPConnection(host)
    h1.request("GET", "/wall.php?action=show")
    response = h1.getresponse()
    wall = response.read()
    h1.close

    # Display the wall
    clear()
    wall = str(wall)
    print(wall)

    return

def SendToServer(action, data):
    xkey = randomString(6)
    scripttype = "PY"
    scriptver = "0.1.beta"

    h1 = http.client.HTTPConnection(host)
    h1.request("GET", "/token.php?key=" + xkey)
    response = h1.getresponse()
    token = response.read()
    h1.close

    token = str(token).strip().replace("'","").replace("b","")

    xauth = str(authcode)+str(token)
    xcode = str(schemecode)+str(token)

    auth = getMD5Hash(xauth)
    code = getMD5Hash(xcode)


    headers = {"X-User": userno,
               "X-System": syscode,
               "X-Auth": auth,
               "X-Code": code,
               "X-Key": xkey,
               "X-Token": token,
               "X-Type": scripttype,
               "X-Version": scriptver,
               "X-Data": data
    }
    h1 = http.client.HTTPConnection(host)
    h1.request("GET", "/wall.php?action=" + action + "&key=" + xkey, "", headers)
    response = h1.getresponse()
    out = response.read()
    h1.close

    return out

# Show the wall!
ShowWall()

# Ask user if they want to write to the wall themselves
yes = set(['yes','y', 'ye'])
no = set(['no','n'])
choice = input(white + "Write on the wall [Y/n]? ").lower()

if choice in no:
    sys.exit(0)
elif choice in yes:
    clear()
else:
    sys.exit(0)

print(red + "What's on your mind, " + username + "? (max 64 characters)")
wallmsg = input()

if len(wallmsg) > 5:
    f = SendToServer("newuser", username);
    postresult = SendToServer("post", wallmsg)
    
    # Check result of post attempt
    if postresult == "*post":
        # Successful
        print("Post successful!")
    elif postresult == "*int":
        # Last post < 10 minutes ago
        print("Sorry, you have to wait 10 minutes between posts.")
        time.sleep(3)
        sys.exit()
    elif postresult == "*inval":
        # Post contained > 64 characters
        print("Your post contained too many characters (max length 64 chars).")
        time.sleep(3)
        sys.exit()
    else:
        # Post failed, unknown reason
        print("\nPost failed :-(")
        time.sleep(3)
        sys.exit()
else:
    print("Your post was too short!")
    time.sleep(3)
    sys.exit()

time.sleep(0.70)
clear()
ShowWall()

input("[0;40;37mPress [1;30m[[37mEnter[30m][0m to continue.")

# Restart's Discord Timeline
# v1.1
# Made with ❤️ in 2024 - https://github.com/restartb/discordtimeline

# --- Imports ---
from operator import itemgetter
import json
import glob
import os
from collections import Counter
from tqdm import tqdm
from sys import exit

# Starting messages
print("Discord Message History")
print("Depending on the amount of messages and your CPU power, this can take a while.\n")

# Take user paths
print("Please enter the path to your Discord Data Package's messages folder. (e.g. package/messages/)")
userPath = input("> ")

# Take user order selection
print("\nSelect a sorting option:\n\n1. Ascending Order (old to new) (default)\n2. Descending Order (new to old)\n")
userSort = str(input("(1/2) "))

if userSort == "1":
    print("Ascending Order selected.")
    userSort = False
elif userSort == "2":
    print("Descending Order selected.")
    userSort = True
else:
    print("Unknown input, selecting default.")
    userSort = False

print("\nLoading....")

# Clean up user input
try:
    userPath = os.path.normpath(userPath)
except ValueError as error:
    print("\nERROR: An error has occured while converting your path! Please check it's valid!\nIf you are sure the path is valid, open a GitHub issue and share the following info:")
    print(error)
    print("\nGitHub Issues Link: https://github.com/restartb/discordtimeline/issues")
    input("\nPress enter to exit.")
    exit()

# --- Finding Files ---
# Use Glob to find all message and channel files
try:
    messageFiles = glob.glob(os.path.join(userPath, "*", "messages.json"))
    channelFiles = glob.glob(os.path.join(userPath, "*", "channel.json"))
except Exception as error:
    print("\nERROR: An error has occured while finding files! Please check the path provided is valid!\nIf you are sure the path is valid, open a GitHub issue and share the following info:")
    print(error)
    print("\nGitHub Issues Link: https://github.com/restartb/discordtimeline/issues")
    input("\nPress enter to exit.")
    exit()

# Return error if we can't find any channel / message files
if len(messageFiles) == 0 or len(channelFiles) == 0:
    print(f"\nERROR: couldn't find any channel or message files in {userPath}.\nAre you sure this is the messages folder in the Discord Data Package?")
    exit()

print(f"Found {len(channelFiles)} message channels.")
input("\nPress enter to start!")

allMessages = []

# --- Main ---
# Iterate through all channels in package
try:
    print("\nReading files.")
    for currentChannelFile in tqdm(channelFiles):
        with open(currentChannelFile, "r", errors="ignore") as channelFile:
            try:
                # Load JSON
                channelData = json.load(channelFile)

                # Set values
                try:
                    # Show Direct Message when type is 1
                    if channelData["type"] == 0:
                        id = channelData["id"]
                        server = channelData["guild"]["name"]
                        channel = channelData["name"]
                        rich = f"{id} - #{channel} in {server}"
                    else:
                        id = channelData["id"]
                        rich = f"{id} - Direct Message (IDs: {channelData['recipients']})"
                except KeyError:
                    id = channelData["id"]
                    rich = f"{id} - Unknown Server (server deleted or user left)"
        
                # Get channel file path
                head, tail = os.path.split(currentChannelFile)
                messagePath = os.path.join(head, "messages.json")
                
                # Open channel's message file
                with open(messagePath, "r", encoding='utf-8', errors="ignore") as messageFile:
                    try:
                        messageData = json.load(messageFile)
    
                        # Add message to global message list
                        for message in messageData:
                            data = [id, rich, message['Timestamp'], message['Contents']]
                            allMessages.append(data)
                    except json.decoder.JSONDecodeError:
                        print(f"Note: {messagePath} has no messages / is corrupt. Skipping...")
            except json.decoder.JSONDecodeError:
                print(f"Note: {currentChannelFile} is corrupt. Skipping...")
except Exception as error:
    print("\nERROR: Error has occured while reading messages! Try again, or open a GitHub issue and share the following info:")
    print(error)
    print("\nGitHub Issues Link: https://github.com/restartb/discordtimeline/issues")
    input("\nPress enter to exit.")
    exit()

lastMessage = [None]
richList = []
yearList = []

# Sort lists
try:
    print("\nSorting lists...")
    allMessages.sort(key=itemgetter(2), reverse=userSort)
except Exception as error:
    print("\nERROR: Error has occured while sorting message list! Try again, or open a GitHub issue and share the following info:")
    print(error)
    print("\nGitHub Issues Link: https://github.com/restartb/discordtimeline/issues")
    input("\nPress enter to exit.")
    exit()

# Generate rich strings for final .txt file
try:
    print("\nGenerating strings...")
    for message in tqdm(allMessages):
        # Show server ID / name when server changes
        if message[0] != lastMessage[0]:
            richList.append(f"\n---------------\n{message[1]}\n---------------\n\n")
        
        richList.append(f"{message[2]} - {message[3]}\n")  
        yearList.append(message[2].split("-")[0])

        lastMessage = message
except Exception as error:
    print("\nERROR: Error has occured while creating final list! Try again, or open a GitHub issue and share the following info:")
    print(error)
    print("\nGitHub Issues Link: https://github.com/restartb/discordtimeline/issues")
    input("\nPress enter to exit.")
    exit()

# Messages per year counting
try:
    print("\nCounting messages...")
    messagesYearString = "Messages Per Year:\n"
    messagesYearCount = Counter(yearList)

    for year in messagesYearCount:
        messagesYearString = f"{messagesYearString}{year}: {messagesYearCount[year]}\n"

    richList.insert(0, ("Discord Message Timeline\n"
                    "Made by @restartb in 2024 - https://github.com/restartb/discordtimeline\n\n"
                    "DISCLAIMER\nDue to Discord restrictions, deleted messages will not be shown or counted in the timeline.\n\n"
                    f"You have {len(allMessages)} messages in this data package\n\n"))

    richList.insert(1, messagesYearString)
except Exception as error:
    print("\nERROR: Error has occured while counting messages! Try again, or open a GitHub issue and share the following info:")
    print(error)
    print("\nGitHub Issues Link: https://github.com/restartb/discordtimeline/issues")
    input("\nPress enter to exit.")
    exit()

# Write rich strings to final .txt file
try:
    print("\nWriting to file...")
    with open("timeline.txt", "w", encoding='utf-8', errors="ignore") as file:
        path = os.path.realpath(file.name)
        
        for item in tqdm(richList):
            file.write(item)
except Exception as error:
    print("\nERROR: Error has occured while writing to timeline file! Try again, or open a GitHub issue and share the following info:")
    print(error)
    print("\nGitHub Issues Link: https://github.com/restartb/discordtimeline/issues")
    input("\nPress enter to exit.")
    exit()

# All done!
print(f"\nAll done! Processed {len(allMessages)} messages. Find your timeline at the following path:")
print(path)

input("\nPress enter to exit.")
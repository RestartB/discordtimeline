# Restart's Discord Timeline
# Made with ❤️ in 2024 - https://github.com/restartb/discordtimeline

# --- Imports ---
from operator import itemgetter
import json
import glob
import os

# Starting messages
print("Discord Message History")
print("Depending on the amount of messages and your CPU power, this can take a while.")

# Take user paths
print("Please enter the path to your Discord Data Package's messages folder. (e.g. package/messages/)")
userPath = input("> ")

# Clean up user input
try:
    userPath = os.path.normpath(userPath)
except ValueError as error:
    print("An error has occured while converting your path! Please check it's valid!\nIf you are sure the path is valid, open a GitHub issue and share the following info:")
    print(error)
    exit()

# --- Finding Files ---
# Use Glob to find all message and channel files
try:
    print("Loading....")
    messageFiles = glob.glob(os.path.join(userPath, "*", "messages.json"))
    channelFiles = glob.glob(os.path.join(userPath, "*", "channel.json"))
except Exception as error:
    print("An error has occured while finding files! Please check the path provided is valid!\nIf you are sure the path is valid, open a GitHub issue and share the following info:")
    print(error)
    exit()

# Return error if we can't find any channel / message files
if len(messageFiles) == 0 or len(channelFiles) == 0:
    print(f"ERROR: couldn't find any channel or message files in {userPath}.\nAre you sure this is the messages folder in the Discord Data Package?")
    exit()

print(f"Found {len(channelFiles)} message channels.")
input("\nPress enter to start!")

allMessages = []

# --- Main ---
# Iterate through all channels in package
print("Reading files.")
for currentChannelFile in channelFiles:
    with open(currentChannelFile, "r", errors="ignore") as channelFile:
        # Load JSON
        channelData = json.load(channelFile)

        # Set values
        try:
            id = channelData["id"]
            server = channelData["guild"]["name"]
            channel = channelData["name"]

            rich = f"{id} - #{channel} in {server}"
        except KeyError:
            id = channelData["id"]
            rich = id

        # Get channel file path
        head, tail = os.path.split(currentChannelFile)
        channelPath = os.path.join(head, "messages.json")
        
        # Open channel's message file
        with open(channelPath, "r", errors="ignore") as messageFile:
            messageData = json.load(messageFile)

            # Add message to global message list
            for message in messageData:
                data = [id, rich, message['Timestamp'], message['Contents']]
                allMessages.append(data)

lastMessage = [None]
richList = []

# Sort lists
print("Sorting lists...")
allMessages.sort(key=itemgetter(2))

richList.append(f"Restart's Discord Timeline\nYou have {len(allMessages)} messages on Discord\n\n---------------\n")

# Generate rich strings for final .txt file
print("Generating strings...")
for message in allMessages:
    # Show server ID / name when server changes
    if message[0] != lastMessage[0]:
        richList.append(f"\n---------------\n{message[1]}\n---------------\n\n")
    
    richList.append(f"{message[2]} - {message[3]}\n")

    lastMessage = message

# Write rich strings to final .txt file
print("Writing to file...")
with open("messages.txt", "w", errors="ignore") as file:
    for item in richList:
        file.write(item)

# All done!
print(f"All done! Processed {len(allMessages)} messages. Find your timeline in the messages.txt file.")
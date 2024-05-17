# Restart's Discord Timeline
# v1
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
    print("\nGitHub Issues Link: https://github.com/restartb/discordtimeline/issues")
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
try:
    print("Reading files.")
    for currentChannelFile in channelFiles:
        with open(currentChannelFile, "r", errors="ignore") as channelFile:
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
                rich = f"{id} - No Data"

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
except Exception as error:
    print("ERROR: Error has occured while reading messages! Try again, or open a GitHub issue and share the following info:")
    print(error)
    print("\nGitHub Issues Link: https://github.com/restartb/discordtimeline/issues")
    exit()

lastMessage = [None]
richList = []

# Sort lists
print("Sorting lists...")
allMessages.sort(key=itemgetter(2))

richList.append("Discord Message Timeline\n"
                "Made by @restartb in 2024 - https://github.com/restartb/discordtimeline\n\n"
                f"You have {len(allMessages)} messages in this data package\n")

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
with open("timeline.txt", "w", errors="ignore") as file:
    for item in richList:
        file.write(item)

# All done!
print(f"All done! Processed {len(allMessages)} messages. Find your timeline in the timeline.txt file.")

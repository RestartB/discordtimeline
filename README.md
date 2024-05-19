# Discord Message Timeline
The Discord Message Timeline allows you to save the timeline of all of your Discord Messages to a txt file.

> [!IMPORTANT]
> You must obtain a [Discord Data Package](https://support.discord.com/hc/en-us/articles/360004957991-Your-Discord-Data-Package) before you are able to use the Timeline generator.

> [!NOTE]
> Messages deleted from Discord will NOT appear on the timeline. There is no way to show deleted messages.

## Instructions
You have one of two options on how to use the Timeline Generator:

### GitHub Releases (recommended)
The GitHub release does not require you to download Python; simply run the file. Click below for the latest release, then download the file for your operating system.\
\
[![Latest Release](https://img.shields.io/github/v/release/restartb/discordtimeline?display_name=release&style=for-the-badge&logo=github&label=Latest)](https://github.com/RestartB/discordtimeline/releases/latest)
### Python
You can also use Python to run the Timeline Generator.
#### Requirements
- [Python 3](https://www.python.org/)
- [TQDM](https://pypi.org/project/tqdm/)

#### Instructions
1. Run `python main.py`.
2. Enter the path to the `messages` folder in your Discord Data Package.
3. Press enter, and wait for the program to generate your timeline.
4. The timeline will be saved to the current running directory, under the filename `timeline.txt`.

## Performance
While the performance of the Timeline creator is very fast, there may be some factors that affect it. Some of the factors are, but not limited to, the following:
- Amount of Messages
- CPU Performance
- RAM Capacity
- Storage Speed
- Python Version
###
During my testing with a dataset of around 60,000 messages, it took no longer than a few seconds to run. Therefore, I don't expect performance to be an issue.

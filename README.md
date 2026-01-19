# Framesbot
A discord bot to show random frames from videos like [Azuframes](https://top.gg/bot/1219806220416843806)

## Features
- deep searches a directory to finds all videos and images
- extract frames from videos on demand
- equally distributed possibilities to all frames (shorter videos are less likely to appear)
- changes pfp and banner to a random frame every 24 hours(can be configured)
- uses rich presence to show a custom text and the frames command
- with each response shows a custom text, the name of the video and the frame number
- ignores files and directories starting with "_"

# Usage
Download source and install needed libs <br><br>
**Configure the bot** <br>
change the following section
```python
#CONFIGURATION
TOKEN = "YOUR-DISCORD-BOT-TOKEN"
VIDEOS_DIR = "videos"
COMMAND_NAME = "frame"
COMMNAD_DESC = "Get a random frame from videos"
CUSTOM_TEXT = "VIDEO\n"
EMBED_COLOR=0x2ecc71
DO_CHANGE_PFP = True
CHANGE_PFP_EVERY = 24 #HOURS
VIDEO_FORMATS = (".mp4", ".mkv", ".avi")
IMAGE_FORMATS = (".png", ".jpg")
```
set TOKEN to the token of your discord bot <br>
set VIDEOS_DIR to the root path of your videos <br>
set COMMAND_NAME to the command you want to use, by default is `/frame` <br>
set COMMAND_DESC to the description of the command you want discord to show <br>
set CUSTOM_TEXT to what you want to show in the first line of your embed, for example a series name <br>
set EMBED_COLOR to the color you want for the left bar on the responses <br>
set DO_CHANGE_PFP to True if you want the bot to change its own pfp and banner every some time <br>
set CHANGE_PFP_EVERY to how many hour it should pass between every change <br>
set VIDEO_FORMAT to a tuple of the types of video files you have <br>
set IMAGE_FORMAT to a tuple of the types of images you want to include <br><br>

modify the `format_path` function to your convenience, by default it removes the extension, name of the root and changes slashes and underscores to spaces <br><br>

Now run the program <br><br>

In discord invite the bot to your server or add it to your aplication and run your command <br>
you'll see something like this <br>
![embed](videos/example.png) <br><br>

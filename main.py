import os
import random
import cv2
import discord
from discord.ext import commands, tasks
import bisect

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

videos = [""]
length = [0]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def format_path(path: str):
    dot = path.rindex(".")
    path = path[len(VIDEOS_DIR):dot]
    return path.translate(str.maketrans("/\\_","   ")).strip()

def make_video_list():
    global videos, length

    print("making video list")

    videos = [""]
    length = [0]
    make_video_list_step(VIDEOS_DIR)
    
    print(videos)
    print(length)
    print("video list ready")
def make_video_list_step(root):
    global videos, length
    
    for ff in os.listdir(root):
        f = os.path.join(root, ff)
        print(f)
        if os.path.isdir(f):
            make_video_list_step(f)
        elif f.endswith(VIDEO_FORMATS):
            videos.append(f)
            cap = cv2.VideoCapture(f)
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
            length.append(length[-1]+total)
        elif f.endswith(IMAGE_FORMATS):
            videos.append(f)
            length.append(length[-1]+1)

def extract_frame(filepath, frame_number, output="frame.jpg"):
    if filepath.endswith(IMAGE_FORMATS):
        #is image not video
        with open(output,"wb") as w:
            with open(filepath,"rb") as r:
                w.write(r.read())
        return output, 1

    cap = cv2.VideoCapture(filepath)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    
    if not ret:
        cap.release()
        raise Exception("error reading frame")
    
    cv2.imwrite(output, frame)
    cap.release()
    return output, total

def random_frame():
    global videos, length
    frame=random.randint(0,length[-1])
    index = bisect.bisect_right(length, frame)

    if length[index]==frame:
        index+=1

    return videos[index], frame-length[index-1]

make_video_list()
@bot.event
async def on_ready():
    print(f"Bot launched as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)}")
    except Exception as e:
        print(e)

    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=CUSTOM_TEXT, state=f"/{COMMAND_NAME}"))

    if DO_CHANGE_PFP:
        change_pfp.start()


@bot.tree.command(name=COMMAND_NAME, description=COMMNAD_DESC)
async def frames(interaction: discord.Interaction):
    await interaction.response.defer()

    #get frame number
    filepath, frame_number = random_frame()

    #extract frame
    image_path, total = extract_frame(filepath, frame_number)
    print("- frame extracted")

    #send response
    embed = discord.Embed(color=EMBED_COLOR)
    embed.description = (
        f"{CUSTOM_TEXT}"
        f"**{format_path(filepath)}**\n"
        f"Frame: {frame_number+1}/{total}"
    )

    file = discord.File(image_path)
    embed.set_image(url=f"attachment://{image_path}")

    await interaction.followup.send(file=file, embed=embed)
    print("- response send")


#task
@tasks.loop(name="change pfp every some time", hours=CHANGE_PFP_EVERY)
async def change_pfp():
    print("UPDATING PROFILE")

    make_video_list()

    filepath1, frame_number1 = random_frame()
    img1, total1 = extract_frame(filepath1, frame_number1, "pfp.jpg")
    filepath2, frame_number2 = random_frame()
    img2, total2 = extract_frame(filepath2, frame_number2, "banner.jpg")
    
    image=open(img1,"rb")
    image2=open(img2,"rb")
    try:
        await bot.user.edit(avatar=image.read(), banner=image2.read())
    except:
        print("can't change profile")

@change_pfp.before_loop
async def before_change_pfp():
    await bot.wait_until_ready()
    print("scheduled task waiting for bot to be ready...")


bot.run(TOKEN)
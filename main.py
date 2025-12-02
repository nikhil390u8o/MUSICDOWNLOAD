#MUSIC DOWN OLDER BY: JERRYRANDIHEHE
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import yt_dlp
import requests
import os
from config import Config

bot = Client(
    "SongPlayRoBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

@bot.on_message(filters.command(["start"]))
def start(client, message):
    text = f"👋 Hello @{message.from_user.username}\n\nSend /s song name"
    message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("SUPPORT", url="https://yourlink.com"),
                    InlineKeyboardButton("ADD ME", url="")
                ]
            ]
        )
    )

@bot.on_message(filters.command(["s"]))
def search_song(client, message):
    query = " ".join(message.command[1:])
    m = message.reply("🔎 Searching...")

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)

        result = info['entries'][0]

        title = result['title']
        link = result['webpage_url']
        duration = result['duration']
        thumbnail = result['thumbnail']

        thumb_name = f"thumb{message.id}.jpg"
        open(thumb_name, "wb").write(requests.get(thumbnail).content)

    except Exception as e:
        m.edit("❌ Nothing Found!")
        print(e)
        return

    m.edit("🎧 Downloading...")

    try:
        with yt_dlp.YoutubeDL({"format": "bestaudio"}) as ydl:
            audio_path = ydl.prepare_filename(result)
            ydl.process_info(result)

        message.reply_audio(
            audio_path,
            caption=f"🎧 {title}\n🔗 {link}",
            title=title,
            duration=duration,
            thumb=thumb_name
        )

        m.delete()

    except Exception as e:
        m.edit("❌ Download Error!")
        print(e)

    try:
        os.remove(audio_path)
        os.remove(thumb_name)
    except:
        pass

bot.run()

import json, os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

API_ID = 35616241
API_HASH = "1789f7461c9dd990e821f6ffb01ca8f3"
BOT_TOKEN = "8791952245:AAGe1oZ_yImK2SG_sTdknV7LDBImvdLH0HQ"

OWNER_ID = 6451644278

app = Client("joinbot_data_v2", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ================= DATABASE =================
DB_FILE = os.path.join(os.getcwd(), "data.json")

default_db = {
    "admins": [OWNER_ID],
    "users": [],
    "welcome": "Hello {name} 👋\nWelcome to our channel 🚀",
    "photos": [],
    "photo_caption": "",
    "apk": None,
    "apk_caption": "",
    "video": None,
    "video_caption": "",
    "voice": None,
    "voice_caption": ""
}

# Load DB safely
if os.path.exists(DB_FILE):
    try:
        with open(DB_FILE, "r") as f:
            db = json.load(f)
    except:
        db = default_db.copy()
else:
    db = default_db.copy()

# Ensure all keys exist
for key in default_db:
    if key not in db:
        db[key] = default_db[key]

# Save function (safe)
def save():
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

# ================= LOAD =================
def load_all():
    global admins, users, welcome, photos
    global photo_caption, apk, apk_caption
    global video, video_caption, voice, voice_caption

    admins = db.get("admins", [OWNER_ID])
    users = set(db.get("users", []))
    welcome = db.get("welcome", "")
    photos = db.get("photos", [])
    photo_caption = db.get("photo_caption", "")
    apk = db.get("apk", None)
    apk_caption = db.get("apk_caption", "")
    video = db.get("video", None)
    video_caption = db.get("video_caption", "")
    voice = db.get("voice", None)
    voice_caption = db.get("voice_caption", "")

load_all()
mode = None

# ================= PANEL =================
def panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Admin",callback_data="addadmin"),
         InlineKeyboardButton("➖ Remove Admin",callback_data="deladmin")],

        [InlineKeyboardButton("📝 Set Welcome",callback_data="setwelcome")],

        [InlineKeyboardButton("📸 Set Photo",callback_data="setphoto"),
         InlineKeyboardButton("🗑 Delete Photo",callback_data="delphoto")],

        [InlineKeyboardButton("✏ Set Photo Caption",callback_data="setphotocap"),
         InlineKeyboardButton("❌ Delete Photo Caption",callback_data="delphotocap")],

        [InlineKeyboardButton("📦 Set APK",callback_data="setapk"),
         InlineKeyboardButton("🗑 Delete APK",callback_data="delapk")],

        [InlineKeyboardButton("✏ Set APK Caption",callback_data="setapkcap"),
         InlineKeyboardButton("❌ Delete APK Caption",callback_data="delapkcap")],

        [InlineKeyboardButton("🎬 Set Video",callback_data="setvideo"),
         InlineKeyboardButton("🗑 Delete Video",callback_data="delvideo")],

        [InlineKeyboardButton("✏ Set Video Caption",callback_data="setvideocap"),
         InlineKeyboardButton("❌ Delete Video Caption",callback_data="delvideocap")],

        [InlineKeyboardButton("🎤 Set Voice",callback_data="setvoice"),
         InlineKeyboardButton("🗑 Delete Voice",callback_data="delvoice")],

        [InlineKeyboardButton("✏ Set Voice Caption",callback_data="setvoicecap"),
         InlineKeyboardButton("❌ Delete Voice Caption",callback_data="delvoicecap")],

        [InlineKeyboardButton("👥 Total Users",callback_data="users")]
    ])

# ================= PANEL CMD =================
@app.on_message(filters.command("panel"))
async def panel_cmd(client,message):
    if message.from_user.id not in admins:
        return
    await message.reply("👑 ADMIN PANEL",reply_markup=panel())

# ================= CALLBACK =================
@app.on_callback_query()
async def callbacks(client,query):
    global mode

    if query.from_user.id not in admins:
        return

    data=query.data

    if data=="addadmin":
        mode="addadmin"
        await query.message.reply("Send User ID")

    elif data=="deladmin":
        mode="deladmin"
        await query.message.reply("Send Admin ID")

    elif data=="setwelcome":
        mode="welcome"
        await query.message.reply("Send Welcome Message")

    elif data=="setphoto":
        mode="photo"
        await query.message.reply("Send Photos")

    elif data=="delphoto":
        db["photos"]=[]
        save()
        await query.answer("Deleted")

    elif data=="setphotocap":
        mode="photocap"
        await query.message.reply("Send Caption")

    elif data=="delphotocap":
        db["photo_caption"]=""
        save()
        await query.answer("Deleted")

    elif data=="setapk":
        mode="apk"
        await query.message.reply("Send APK")

    elif data=="delapk":
        db["apk"]=None
        save()
        await query.answer("Deleted")

    elif data=="setapkcap":
        mode="apkcap"
        await query.message.reply("Send Caption")

    elif data=="delapkcap":
        db["apk_caption"]=""
        save()
        await query.answer("Deleted")

    elif data=="setvideo":
        mode="video"
        await query.message.reply("Send Video")

    elif data=="delvideo":
        db["video"]=None
        save()
        await query.answer("Deleted")

    elif data=="setvideocap":
        mode="videocap"
        await query.message.reply("Send Caption")

    elif data=="delvideocap":
        db["video_caption"]=""
        save()
        await query.answer("Deleted")

    elif data=="setvoice":
        mode="voice"
        await query.message.reply("Send Voice")

    elif data=="delvoice":
        db["voice"]=None
        save()
        await query.answer("Deleted")

    elif data=="setvoicecap":
        mode="voicecap"
        await query.message.reply("Send Caption")

    elif data=="delvoicecap":
        db["voice_caption"]=""
        save()
        await query.answer("Deleted")

    elif data=="users":
        await query.answer(f"Users: {len(db['users'])}",True)

# ================= TEXT SAVE =================
@app.on_message(filters.text)
async def save_text(client,message):
    global mode

    if message.from_user.id not in db["admins"]:
        return

    if mode=="addadmin":
        db["admins"].append(int(message.text))
        save()
        await message.reply("Admin Added")

    elif mode=="deladmin":
        if int(message.text) in db["admins"]:
            db["admins"].remove(int(message.text))
            save()
            await message.reply("Admin Removed")

    elif mode=="welcome":
        db["welcome"]=message.text
        save()
        await message.reply("Saved")

    elif mode=="photocap":
        db["photo_caption"]=message.text
        save()
        await message.reply("Saved")

    elif mode=="apkcap":
        db["apk_caption"]=message.text
        save()
        await message.reply("Saved")

    elif mode=="videocap":
        db["video_caption"]=message.text
        save()
        await message.reply("Saved")

    elif mode=="voicecap":
        db["voice_caption"]=message.text
        save()
        await message.reply("Saved")

    mode=None

# ================= MEDIA SAVE =================
@app.on_message(filters.photo)
async def photo(client,message):
    if message.from_user.id in db["admins"] and mode=="photo":
        db["photos"].append(message.photo.file_id)
        save()
        await message.reply("Photo Added")

@app.on_message(filters.document)
async def apkf(client,message):
    if message.from_user.id in db["admins"] and mode=="apk":
        db["apk"]=message.document.file_id
        save()
        await message.reply("APK Saved")

@app.on_message(filters.video)
async def videof(client,message):
    if message.from_user.id in db["admins"] and mode=="video":
        db["video"]=message.video.file_id
        save()
        await message.reply("Video Saved")

@app.on_message(filters.voice)
async def voicef(client,message):
    if message.from_user.id in db["admins"] and mode=="voice":
        db["voice"]=message.voice.file_id
        save()
        await message.reply("Voice Saved")

# ================= JOIN =================
@app.on_chat_join_request()
async def join(client,req):
    user_id=req.from_user.id
    name=req.from_user.first_name

    if user_id not in db["users"]:
        db["users"].append(user_id)
        save()

    try:
        await client.send_message(user_id, db["welcome"].replace("{name}",name))

        if db["photos"]:
            media=[]
            for i,p in enumerate(db["photos"]):
                if i==len(db["photos"])-1:
                    media.append(InputMediaPhoto(p,caption=db["photo_caption"]))
                else:
                    media.append(InputMediaPhoto(p))
            await client.send_media_group(user_id,media)

        if db["video"]:
            await client.send_video(user_id,db["video"],caption=db["video_caption"])

        if db["apk"]:
            await client.send_document(user_id,db["apk"],caption=db["apk_caption"])

        if db["voice"]:
            await client.send_voice(user_id,db["voice"],caption=db["voice_caption"])

    except:
        pass

app.run()

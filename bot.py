import os
import random
import datetime
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import ChatBannedRights

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

warnings = {}
points = {}

print("🤖 البوت شغال دلوقتي!")

# ================= ترحيب =================
@bot.on(events.ChatAction)
async def welcome(event):
    if event.user_joined or event.user_added:
        user = await event.get_user()
        await event.reply(f"👋 أهلاً يا {user.first_name} نورت الجروب 🔥")

# ================= ايدي =================
@bot.on(events.NewMessage(pattern="ايدي"))
async def myid(event):
    await event.reply(f"🆔 ايديك: {event.sender_id}")

# ================= كتم =================
@bot.on(events.NewMessage(pattern="كتم"))
async def mute_handler(event):
    if not event.is_group:
        return

    reply = await event.get_reply_message()
    if not reply:
        await event.reply("❌ اعمل Reply على العضو")
        return

    rights = ChatBannedRights(
        until_date=datetime.timedelta(minutes=10),
        send_messages=True
    )

    try:
        await bot.edit_permissions(event.chat_id, reply.sender_id, rights)
        await event.reply("🔇 تم كتمه 10 دقايق")
    except:
        await event.reply("❌ مش قادر أكتمه")

# ================= فك كتم =================
@bot.on(events.NewMessage(pattern="فك"))
async def unmute(event):
    reply = await event.get_reply_message()
    if not reply:
        return

    rights = ChatBannedRights(until_date=None)
    await bot.edit_permissions(event.chat_id, reply.sender_id, rights)
    await event.reply("✅ تم فك الكتم")

# ================= طرد =================
@bot.on(events.NewMessage(pattern="طرد"))
async def kick_handler(event):
    reply = await event.get_reply_message()
    if not reply:
        return
    await bot.kick_participant(event.chat_id, reply.sender_id)
    await event.reply("🚪 اتطرد بنجاح")

# ================= تحذير =================
@bot.on(events.NewMessage(pattern="تحذير"))
async def warn(event):
    reply = await event.get_reply_message()
    if not reply:
        return

    user_id = reply.sender_id
    warnings[user_id] = warnings.get(user_id, 0) + 1

    if warnings[user_id] >= 3:
        rights = ChatBannedRights(
            until_date=datetime.timedelta(minutes=5),
            send_messages=True
        )
        await bot.edit_permissions(event.chat_id, user_id, rights)
        warnings[user_id] = 0
        await event.reply("🚫 3 تحذيرات = كتم 5 دقايق")
    else:
        await event.reply(f"⚠ تحذير رقم {warnings[user_id]}")

# ================= نقاط =================
@bot.on(events.NewMessage(pattern="نقاط"))
async def show_points(event):
    user_id = event.sender_id
    pts = points.get(user_id, 0)
    await event.reply(f"⭐ نقاطك: {pts}")

@bot.on(events.NewMessage)
async def give_points(event):
    if event.is_group:
        user_id = event.sender_id
        points[user_id] = points.get(user_id, 0) + 1

# ================= منع لينكات =================
@bot.on(events.NewMessage)
async def block_links(event):
    if event.is_group:
        text = event.raw_text
        if "http" in text or "t.me/" in text:
            try:
                await event.delete()
                await event.reply("🚫 ممنوع لينكات")
            except:
                pass

# ================= تاك الكل =================
@bot.on(events.NewMessage(pattern="تاك"))
async def tag_all(event):
    members = await bot.get_participants(event.chat_id)
    text = ""
    for m in members[:50]:
        text += f"[{m.first_name}](tg://user?id={m.id}) "
    await event.reply(text)

# ================= ألعاب =================
@bot.on(events.NewMessage(pattern="زهر"))
async def dice_game(event):
    await event.reply(f"🎲 {random.randint(1,6)}")

@bot.on(events.NewMessage(pattern="عملة"))
async def coin_game(event):
    await event.reply(f"🪙 {random.choice(['رأس','كتابة'])}")

bot.run_until_disconnected()

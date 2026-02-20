import os
from telethon import TelegramClient, events
from telethon.tl.types import MessageEntityUrl
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

print("🤖 البوت شغال دلوقتي!")

# 👋 ترحيب العضو الجديد
@bot.on(events.ChatAction)
async def welcome(event):
    if event.user_added or event.user_joined:
        await event.reply(f"👋 أهلاً بيك يا {event.user.first_name}! نورت الجروب ✨")

# 🚀 أمر /start
@bot.on(events.NewMessage(pattern="^/start$"))
async def start(event):
    await event.reply("🤖 البوت شغال! جاهز للحماية والألعاب 🚀")

# 🔇 كتم عن طريق reply
@bot.on(events.NewMessage(pattern="^/كت$"))
async def mute_handler(event):
    if not event.is_group:
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("❌ لازم تعمل reply على رسالة العضو!")
        return
    await bot.edit_permissions(event.chat_id, reply.sender_id, send_messages=False)
    await event.reply(f"🔇 {reply.sender.first_name} اتكتم بنجاح!")

# 🚪 طرد عن طريق reply
@bot.on(events.NewMessage(pattern="^/طرد$"))
async def kick_handler(event):
    if not event.is_group:
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("❌ لازم تعمل reply على رسالة العضو!")
        return
    await bot.kick_participant(event.chat_id, reply.sender_id)
    await event.reply(f"🚪 {reply.sender.first_name} اتطرد من الجروب!")

# 🔗 منع نشر لينكات
@bot.on(events.NewMessage)
async def block_links(event):
    if not event.is_group:
        return
    text = event.raw_text
    if "t.me/" in text or "http" in text:
        try: 
            await event.delete()
            await event.reply("🚫 ممنوع نشر لينكات!")
        except:
            pass

# 📢 تاك الكل
@bot.on(events.NewMessage(pattern="تاك منورين"))
async def tag_all(event):
    if not event.is_group:
        return
    members = await bot.get_participants(event.chat_id)
    mentions = " ".join([f"@{m.username}" if m.username else f"[{m.first_name}](tg://user?id={m.id})" for m in members])
    await event.reply(f"📢 منورين يا جماعة:\n{mentions}")

# 🎲 ألعاب بسيطة
@bot.on(events.NewMessage(pattern="!زهر"))
async def dice_game(event):
    await event.reply(f"🎲 زهر: {random.randint(1,6)}")

@bot.on(events.NewMessage(pattern="!عملة"))
async def coin_game(event):
    choice = random.choice(["رأس", "كتابة"])
    await event.reply(f"🪙 العملة: {choice}")

# 启動
bot.run_until_disconnected()
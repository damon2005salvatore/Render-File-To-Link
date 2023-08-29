#(c) Adarsh-Goel
import os
import asyncio
from asyncio import TimeoutError
from Adarsh.bot import StreamBot
from Adarsh.utils.database import Database
from Adarsh.utils.human_readable import humanbytes
from Adarsh.vars import Var
from urllib.parse import quote_plus
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


MY_PASS = os.environ.get("MY_PASS",None)
pass_dict = {}
pass_db = Database(Var.DATABASE_URL, "ag_passwords")


@StreamBot.on_message((filters.regex("ʟᴏɢɪɴ🔑") | filters.command("login")) & ~filters.edited, group=4)
async def login_handler(c: Client, m: Message):
    try:
        try:
            ag = await m.reply_text("**ɴᴏᴡ sᴇɴᴅ ᴍᴇ ᴘᴀssᴡᴏʀᴅ.**\n\n **ɪғ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴄʜᴇᴄᴋ ᴛʜᴇ** MY_PASS **ᴠᴀʀɪᴀʙʟᴇ ɪɴ ʜᴇʀᴏᴋᴜ** \n\n(ʏᴏᴜ ᴄᴀɴ ᴜsᴇ /cancel ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇss)")
            _text = await c.listen(m.chat.id, filters=filters.text, timeout=90)
            if _text.text:
                textp = _text.text
                if textp=="/cancel":
                   await ag.edit("**ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ**")
                   return
            else:
                return
        except TimeoutError:
            await ag.edit("**ɪ ᴄᴀɴ'ᴛ ᴡᴀɪᴛ ᴍᴏʀᴇ ғᴏʀ ᴘᴀssᴡᴏʀᴅ, ᴛʀʏ ᴀɢᴀɪɴ**")
            return
        if textp == MY_PASS:
            await pass_db.add_user_pass(m.chat.id, textp)
            ag_text = "**ʏᴇᴀʜ ! ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ᴛʜᴇ ᴘᴀssᴡᴏʀᴅ ᴄᴏʀʀᴇᴄᴛʟʏ**"
        else:
            ag_text = "**ᴡʀᴏɴɢ ᴘᴀssᴡᴏʀᴅ, ᴛʀʏ ᴀɢᴀɪɴ**"
        await ag.edit(ag_text)
    except Exception as e:
        print(e)

@StreamBot.on_message((filters.private) & (filters.document | filters.video | filters.audio | filters.photo) & ~filters.edited, group=4)
async def private_receive_handler(c: Client, m: Message):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(m.chat.id)
        if check_pass== None:
            await m.reply_text("**ʟᴏɢɪɴ ғɪʀsᴛ ᴜsɪɴɢ /login ᴄᴍᴅ** \n**ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴛʜᴇ ᴘᴀssᴡᴏʀᴅ ᴄᴏɴᴛᴀᴄᴛ @themastertheblaster**")
            return
        if check_pass != MY_PASS:
            await pass_db.delete_user(m.chat.id)
            return
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ : \n\n Nᴀᴍᴇ : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.chat.id,
                    text="**ʏᴏᴜ'ʀᴇ ʙᴀɴɴᴇᴅ..**",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return 
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="""<i>ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ..**</i>""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("ᴊᴏɪɴ ɴᴏᴡ", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="HTML"
            )
            return
        except Exception as e:
            await m.reply_text(e)
            await c.send_message(
                chat_id=m.chat.id,
                text="**ᴀᴅᴅ ғᴏʀᴄᴇ sᴜʙ ᴛᴏ ᴀɴʏ ᴄʜᴀɴɴᴇʟ**",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    try:

        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.message_id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        
        online_link = f"{Var.URL}{str(log_msg.message_id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
       
        
        

        msg_text ="""
<b>ʏᴏᴜʀ ʟɪɴᴋ ɪs ɢᴇɴᴇʀᴀᴛᴇᴅ...</b>⚡

<b>📧 ғɪʟᴇ ɴᴀᴍᴇ :- </b> <i><b>{}</b></i>

<b>📦 ғɪʟᴇ sɪᴢᴇ :- </b> <i><b>{}</b></i>

<b>💌 ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ :- </b> <i><b>{}</b></i>

<b>🖥 ᴡᴀʏᴄʜ ᴏɴʟɪɴᴇ :- </b> <i><b>{}</b></i>

<b>🪩 ᴛʜɪs ʟɪɴᴋ ɪs ᴘᴇʀᴍᴀɴᴇɴᴛ ᴀɴᴅ ᴡᴏɴ'ᴛ ɢᴇᴛs ᴇxᴘɪʀᴇᴅ ♻️\n\n@mkv_blasters</b>"""

        await log_msg.reply_text(text=f"**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uꜱᴇʀ ɪᴅ :** `{m.from_user.id}`\n**sᴛʀᴇᴀᴍ ʟɪɴᴋ :** {stream_link}", disable_web_page_preview=True, parse_mode="Markdown", quote=True)
        await m.reply_text(
            text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(m)), online_link, stream_link),
            parse_mode="HTML", 
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🖥️ ᴡᴀᴛᴄʜ 🖥️", url=stream_link), #Stream Link
                                                InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=online_link)]]) #online Link
        )
    except FloodWait as e:
        print(f"**sʟᴇᴇᴘɪɴɢ ғᴏʀ** {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**𝚄𝚜𝚎𝚛 𝙸𝙳 :** `{str(m.from_user.id)}`", disable_web_page_preview=True, parse_mode="Markdown")


@StreamBot.on_message(filters.channel & ~filters.group & (filters.document | filters.video | filters.photo) & ~filters.edited & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(broadcast.chat.id)
        if check_pass == None:
            await broadcast.reply_text("**ʟᴏɢɪɴ ғɪʀsᴛ ᴜsɪɴɢ /login ᴄᴍᴅ** \n**ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴛʜᴇ ᴘᴀss ? ʀᴇϙᴜᴇsᴛ ɪᴛ ғʀᴏᴍ @themastertheblaster**")
            return
        if check_pass != MY_PASS:
            await broadcast.reply_text("**ᴡʀᴏɴɢ ᴘᴀssᴡᴏʀᴅ , ʟᴏɢɪɴ ᴀɢᴀɪɴ**")
            await pass_db.delete_user(broadcast.chat.id)
            return
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.message_id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"       
        online_link = f"{Var.URL}{str(log_msg.message_id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        await log_msg.reply_text(
            text=f"**Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** `{broadcast.chat.title}`\n**Cʜᴀɴɴᴇʟ ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** {stream_link}",
            quote=True,
            parse_mode="Markdown"
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.message_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🖥️ ᴡᴀᴛᴄʜ 🖥️", url=stream_link), #Stream Link
                     InlineKeyboardButton("📥 ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=online_link)]]) #Online Link
        )
    except FloodWait as w:
        print(f"**sʟᴇᴇᴘɪɴɢ ғᴏʀ** {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(w.x)}s from {broadcast.chat.title}\n\n**Cʜᴀɴɴᴇʟ ID:** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True, parse_mode="Markdown")
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `{e}`", disable_web_page_preview=True, parse_mode="Markdown")
        print(f"Cᴀɴ'ᴛ Eᴅɪᴛ Bʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ!\nEʀʀᴏʀ:  **Give me edit permission in updates and bin Chanell{e}**")

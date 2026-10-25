"""Clean SearchMovie user interface; admin and delivery logic stay unchanged."""
import html
import math
from urllib.parse import quote

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

RESULTS_PER_PAGE = 5

SEARCH_HELP = """📨 Sᴇɴᴅ Mᴏᴠɪᴇ Oʀ Sᴇʀɪᴇs Nᴀᴍᴇ ᴀɴᴅ Yᴇᴀʀ Aꜱ Pᴇʀ Gᴏᴏɢʟᴇ Sᴘᴇʟʟɪɴɢ..!! 👍

⚠️ Exᴀᴍᴘʟᴇ Fᴏʀ Mᴏᴠɪᴇ 👇

👉 Jailer
👉 Jailer 2023

⚠️ Exᴀᴍᴘʟᴇ Fᴏʀ WᴇʙSᴇʀɪᴇs👇

👉 Stranger Things
👉 Stranger Things S02 E04

⚠️ ᴅᴏɴ'ᴛ ᴀᴅᴅ ᴇᴍᴏᴊɪꜱ ᴀɴᴅ ꜱʏᴍʙᴏʟꜱ ɪɴ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ, ᴜꜱᴇ ʟᴇᴛᴛᴇʀꜱ ᴏɴʟʏ..!! ❌"""

NOT_FOUND = """● I could not find the file you requested😕

● Is the movie you asked about released OTT..?

● Pay attention to the following…

● Ask for correct spelling.

● Do not ask for movies that are not released on OTT platforms.

● Also ask [movie name, language] like this....

● If you not get any movie request by using /request"""


def start_text(name):
    name = html.escape(str(name or "User"))
    return f"""SearchMovie 🍿:

Hey 👋 {name}🤩

🍿 Wᴇʟᴄᴏᴍᴇ Tᴏ Tʜᴇ Wᴏʀʟᴅ's Cᴏᴏʟᴇsᴛ Sᴇᴀʀᴄʜ Eɴɢɪɴᴇ!

Here You Can Request Movie's, Just Sent Movie OR WebSeries Name With Proper Google Spelling..!!"""


def start_markup(bot_username):
    bot_url = f"https://t.me/{bot_username}"
    share_url = (
        "https://t.me/share/url?url=" + quote(bot_url, safe="")
        + "&text=" + quote("SearchMovie 🍿 - Movie and WebSeries Search Bot", safe="")
    )
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Search movie or webseries", callback_data="search_help")],
        [InlineKeyboardButton("Share now", url=share_url)],
    ])


def result_text(name, title):
    name = html.escape(str(name or "User"))
    title = html.escape(str(title or "Your Search"))
    return f"""Hey {name}👋🏻

⭕️Rotate your 🔄 phone to see files' full name.......................................⭕️

Title : {title}
Your Files is Ready Now"""


def result_markup(files, file_button_text, pre, total, next_offset, user_id, key, offset=0):
    """Five existing-delivery file buttons and one Previous/page/Next row."""
    rows = [
        [InlineKeyboardButton(file_button_text(file), callback_data=f"{pre}#{file['file_id']}")]
        for file in files[:RESULTS_PER_PAGE]
    ]
    try:
        current_offset = max(0, int(offset or 0))
    except (TypeError, ValueError):
        current_offset = 0
    try:
        next_value = int(next_offset) if next_offset not in ("", None) else 0
    except (TypeError, ValueError):
        next_value = 0
    pages = max(1, math.ceil(int(total or 0) / RESULTS_PER_PAGE))
    current_page = current_offset // RESULTS_PER_PAGE + 1
    previous_data = (
        f"next_{user_id}_{key}_{max(0, current_offset - RESULTS_PER_PAGE)}"
        if current_offset > 0 else "pages"
    )
    next_data = f"next_{user_id}_{key}_{next_value}" if next_value > 0 else "pages"
    rows.append([
        InlineKeyboardButton("Previous", callback_data=previous_data),
        InlineKeyboardButton(f"{current_page}/{pages}", callback_data="pages"),
        InlineKeyboardButton("Next", callback_data=next_data),
    ])
    return InlineKeyboardMarkup(rows)

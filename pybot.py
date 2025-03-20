import os
import logging
import random
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from collections import defaultdict

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7902753373:AAEmT26RezzQQlEzf6AtPiM6xjm0etcba0A")

# Track user usage
user_usage = defaultdict(int)
MAX_FREE_USES = 3  # Changed from previous value to limit to 3 uses lifetime

# Message templates
WELCOME_MESSAGE = """<b>✨ 𝐂𝐡𝐨𝐨𝐬𝐞 𝐘𝐨𝐮𝐫 𝐏𝐚𝐭𝐡 𝐭𝐨 𝐖𝐞𝐚𝐥𝐭𝐡 ✨</b>

<b>🔶 𝐏𝐀𝐈𝐃 𝐁𝐎𝐓 (💯 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐄𝐱𝐩𝐞𝐫𝐢𝐞𝐧𝐜𝐞)</b>
<b>✔ 𝟖𝟓-𝟏𝟎𝟎% 𝐀𝐜𝐜𝐮𝐫𝐚𝐜𝐲 🔥</b>
<b>✔ 𝐄𝐱𝐜𝐥𝐮𝐬𝐢𝐯𝐞 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐏𝐥𝐚𝐧𝐬 💎</b>
<b>✔ 𝐇𝐢𝐠𝐡𝐞𝐫 𝐖𝐢𝐧𝐧𝐢𝐧𝐠 𝐑𝐚𝐭𝐞 🚀</b>
<b>✔ 𝐏𝐫𝐢𝐨𝐫𝐢𝐭𝐲 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 🏆</b>

<b>🔷 𝐅𝐑𝐄𝐄 𝐁𝐎𝐓 (🔹 𝐁𝐚𝐬𝐢𝐜 𝐀𝐜𝐜𝐞𝐬𝐬)</b>
<b>✔ 𝟖𝟐% 𝐀𝐜𝐜𝐮𝐫𝐚𝐜𝐲 📈</b>
<b>✔ 𝐄𝐬𝐬𝐞𝐧𝐭𝐢𝐚𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 🎯</b>
<b>✔ 𝐒𝐭𝐚𝐧𝐝𝐚𝐫𝐝 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 📩</b>
<b>✔ 𝐋𝐢𝐦𝐢𝐭𝐞𝐝 𝐌𝐢𝐧𝐞 𝐎𝐩𝐭𝐢𝐨𝐧𝐬 ⚡</b>

<b>💬 𝐅𝐨𝐫 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐜𝐞: <a href="https://t.me/RichieRichKunal">@𝐑𝐢𝐜𝐡𝐢𝐞𝐑𝐢𝐜𝐡𝐊𝐮𝐧𝐚𝐥</a></b>
<b>📢 𝐒𝐭𝐚𝐲 𝐔𝐩𝐝𝐚𝐭𝐞𝐝: <a href="https://t.me/RichieRichKunalStore">@𝐑𝐢𝐜𝐡𝐢𝐞𝐑𝐢𝐜𝐡𝐊𝐮𝐧𝐚𝐥𝐒𝐭𝐨𝐫𝐞</a></b>

<b>⚡ 𝐘𝐨𝐮𝐫 𝐖𝐞𝐚𝐥𝐭𝐡 𝐉𝐨𝐮𝐫𝐧𝐞𝐲 𝐁𝐞𝐠𝐢𝐧𝐬 𝐍𝐨𝐰! ⚡</b>"""

VIDEO_MESSAGE = """<b>💲💰⬇️ 𝐂𝐥𝐢𝐜𝐤 𝐎𝐧 𝐓𝐡𝐞 𝐁𝐞𝐥𝐨𝐰 𝐋𝐢𝐧𝐤 𝐓𝐨 𝐄𝐚𝐫𝐧 𝐓𝐨𝐧𝐬 𝐎𝐟 𝐌𝐨𝐧𝐞𝐲 𝐁𝐲 𝐇𝐚𝐜𝐤𝐢𝐧𝐠 𝐒𝐭𝐚𝐤𝐞 𝐔𝐬𝐢𝐧𝐠 𝐓𝐡𝐢𝐬 𝐁𝐨𝐭 🤑💵⬇️</b>"""
VIDEO_MESSAGE_AFTER = """<b>💲💰⬆️ 𝐂𝐥𝐢𝐜𝐤 𝐎𝐧 𝐓𝐡𝐞 𝐀𝐛𝐨𝐯𝐞 𝐋𝐢𝐧𝐤 𝐓𝐨 𝐄𝐚𝐫𝐧 𝐓𝐨𝐧𝐬 𝐎𝐟 𝐌𝐨𝐧𝐞𝐲 𝐁𝐲 𝐇𝐚𝐜𝐤𝐢𝐧𝐠 𝐒𝐭𝐚𝐤𝐞 𝐔𝐬𝐢𝐧𝐠 𝐓𝐡𝐢𝐬 𝐁𝐨𝐭 🤑💵⬆️</b>"""

INFO_MESSAGE = """<b>𝐈𝐍𝐅𝐎 ℹ️</b>

<b>👑 𝐕𝐈𝐏 𝐁𝐎𝐓 98.99% 𝐀𝐂𝐂𝐔𝐑𝐀𝐂𝐘 🎯 𝐀𝐍𝐃 𝐔𝐍𝐋𝐈𝐌𝐈𝐓𝐄𝐃 𝐔𝐒𝐄𝐒 ⚡</b>

<b>𝐎𝐰𝐧𝐞𝐫 - <a href="https://t.me/RichieRichKunal">@𝐑𝐢𝐜𝐡𝐢𝐞𝐑𝐢𝐜𝐡𝐊𝐮𝐧𝐚𝐥</a></b>

<b>⭐ 𝐅𝐑𝐄𝐄 𝐁𝐎𝐓 72.7% 𝐀𝐂𝐂𝐔𝐑𝐀𝐂𝐘 🎯 𝐀𝐍𝐃 𝐎𝐍𝐋𝐘 3 𝐓𝐈𝐌𝐄𝐒 𝐔𝐒𝐄 𝐅𝐎𝐑 𝐋𝐈𝐅𝐄𝐓𝐈𝐌𝐄 🚫</b>"""

PLAN_MESSAGES = {
    "499": """<b>🔹 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐁𝐨𝐭 (₹𝟒𝟗𝟗)</b>
<b>✔️ 𝐀𝐜𝐜𝐮𝐫𝐚𝐜𝐲: 𝟖𝟓-𝟗𝟎%</b>
<b>🎮 𝐆𝐚𝐦𝐞𝐬: 𝟑 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞</b>
<b>💰 𝐃𝐚𝐢𝐥𝐲 𝐁𝐞𝐭𝐬: 𝐔𝐩 𝐭𝐨 𝟓𝟎𝟎</b>
<b>📅 𝐕𝐚𝐥𝐢𝐝𝐢𝐭𝐲: 𝟑 𝐦𝐨𝐧𝐭𝐡𝐬</b>
<b>🛡️ 𝐑𝐢𝐬𝐤 𝐑𝐞𝐝𝐮𝐜𝐭𝐢𝐨𝐧 𝐅𝐞𝐚𝐭𝐮𝐫𝐞</b>""",

    "999": """<b>🔹 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐏𝐥𝐮𝐬 𝐁𝐨𝐭 (₹𝟗𝟗𝟗)</b>
<b>✔️ 𝐀𝐜𝐜𝐮𝐫𝐚𝐜𝐲: 𝟗𝟗-𝟏𝟎𝟎%</b>
<b>🎮 𝐆𝐚𝐦𝐞𝐬: 𝟓 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞</b>
<b>💰 𝐃𝐚𝐢𝐥𝐲 𝐁𝐞𝐭𝐬: 𝐔𝐧𝐥𝐢𝐦𝐢𝐭𝐞𝐝</b>
<b>📅 𝐕𝐚𝐥𝐢𝐝𝐢𝐭𝐲: 𝟒 𝐦𝐨𝐧𝐭𝐡𝐬</b>
<b>⚡ 𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐔𝐧𝐥𝐨𝐜𝐤𝐞𝐝</b>""",

    "1999": """<b>🔥 𝐏𝐞𝐫𝐬𝐨𝐧𝐚𝐥 𝐁𝐨𝐭 (₹𝟏𝟗𝟗𝟗) 🔥</b>
<b>🖥️ 𝐃𝐞𝐝𝐢𝐜𝐚𝐭𝐞𝐝 𝐏𝐞𝐫𝐬𝐨𝐧𝐚𝐥 𝐒𝐞𝐫𝐯𝐞𝐫</b>
<b>✔️ 𝐀𝐜𝐜𝐮𝐫𝐚𝐜𝐲: 𝟏𝟎𝟎%</b>
<b>🎮 𝐆𝐚𝐦𝐞𝐬: 𝟓 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞</b>
<b>💰 𝐃𝐚𝐢𝐥𝐲 𝐁𝐞𝐭𝐬: 𝐔𝐧𝐥𝐢𝐦𝐢𝐭𝐞𝐝</b>
<b>📅 𝐕𝐚𝐥𝐢𝐝𝐢𝐭𝐲: 𝟑 𝐦𝐨𝐧𝐭𝐡𝐬</b>
<b>🚀 𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐔𝐧𝐥𝐨𝐜𝐤𝐞𝐝</b>"""
}

PAYMENT_INFO = """𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐚𝐲 𝐮𝐬𝐢𝐧𝐠 𝐭𝐡𝐞 𝐟𝐨𝐥𝐥𝐨𝐰𝐢𝐧𝐠 𝐔𝐏𝐈 𝐈𝐃:

`baccax3@axl`

𝐀𝐟𝐭𝐞𝐫 𝐩𝐚𝐲𝐦𝐞𝐧𝐭, 𝐜𝐥𝐢𝐜𝐤 '𝐃𝐨𝐧𝐞 𝐏𝐚𝐲𝐦𝐞𝐧𝐭' 𝐚𝐧𝐝 𝐬𝐞𝐧𝐝 𝐭𝐡𝐞 𝐬𝐜𝐫𝐞𝐞𝐧𝐬𝐡𝐨𝐭 𝐭𝐨 𝐩𝐫𝐨𝐜𝐞𝐞𝐝.
𝐘𝐨𝐮𝐫 𝐩𝐥𝐚𝐧 𝐰𝐢𝐥𝐥 𝐛𝐞 𝐚𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝 𝐰𝐢𝐭𝐡𝐢𝐧 𝟓 𝐦𝐢𝐧𝐮𝐭𝐞𝐬 𝐚𝐟𝐭𝐞𝐫 𝐯𝐞𝐫𝐢𝐟𝐢𝐜𝐚𝐭𝐢𝐨𝐧."""

SUPPORT_MESSAGE = """<b>𝐓𝐡𝐚𝐧𝐤 𝐲𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐩𝐚𝐲𝐦𝐞𝐧𝐭!</b>

<b>𝐈𝐦𝐩𝐨𝐫𝐭𝐚𝐧𝐭 𝐍𝐨𝐭𝐞:</b>
<b>𝐈𝐟 𝐲𝐨𝐮𝐫 𝐩𝐥𝐚𝐧 𝐢𝐬 𝐧𝐨𝐭 𝐚𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝 𝐰𝐢𝐭𝐡𝐢𝐧 𝟓 𝐦𝐢𝐧𝐮𝐭𝐞𝐬, 𝐩𝐥𝐞𝐚𝐬𝐞:</b>
<b>𝟏. 𝐓𝐚𝐤𝐞 𝐚 𝐬𝐜𝐫𝐞𝐞𝐧𝐬𝐡𝐨𝐭 𝐨𝐟 𝐲𝐨𝐮𝐫 𝐩𝐚𝐲𝐦𝐞𝐧𝐭</b>
<b>𝟐. 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐨𝐮𝐫 𝐬𝐮𝐩𝐩𝐨𝐫𝐭 𝐭𝐞𝐚𝐦 𝐮𝐬𝐢𝐧𝐠 𝐭𝐡𝐞 𝐛𝐮𝐭𝐭𝐨𝐧 𝐛𝐞𝐥𝐨𝐰</b>
<b>𝟑. 𝐒𝐡𝐚𝐫𝐞 𝐛𝐨𝐭𝐡 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐚𝐧𝐝 𝐜𝐡𝐚𝐭 𝐬𝐜𝐫𝐞𝐞𝐧𝐬𝐡𝐨𝐭𝐬</b>

<b>𝐎𝐮𝐫 𝐬𝐮𝐩𝐩𝐨𝐫𝐭 𝐭𝐞𝐚𝐦 𝐰𝐢𝐥𝐥 𝐚𝐬𝐬𝐢𝐬𝐭 𝐲𝐨𝐮 𝐢𝐦𝐦𝐞𝐝𝐢𝐚𝐭𝐞𝐥𝐲.</b>"""

QR_CODES = {
    "499": "https://postimg.cc/S2XSLJ1W",
    "999": "https://postimg.cc/2LhCJgDy",
    "1999": "https://postimg.cc/8jbS6Rk2"
}

# Update the MINE_IMAGES lists with direct image URLs
MINE_IMAGES_1 = [
    "https://i.postimg.cc/c6m54cB2/image.jpg",
    "https://i.postimg.cc/Pvt3QLTS/image.jpg",
    "https://i.postimg.cc/nMZPJWBq/image.jpg",
    "https://i.postimg.cc/ZBPsNPt9/image.jpg",
    "https://i.postimg.cc/phM1yG7b/image.jpg",
    "https://i.postimg.cc/67vmWJMf/image.jpg",
    "https://i.postimg.cc/3k6qQJFw/image.jpg",
    "https://i.postimg.cc/9DzkkqTS/image.jpg",
    "https://i.postimg.cc/Mv94tYcV/image.jpg",
    "https://i.postimg.cc/nCFgvWLn/image.jpg",
    "https://i.postimg.cc/DmdR4hnC/image.jpg",
    "https://i.postimg.cc/K4ydYjSk/image.jpg",
    "https://i.postimg.cc/QKbg80Lb/image.jpg",
    "https://i.postimg.cc/SYq7bHPR/image.jpg",
    "https://i.postimg.cc/k6WFZ7fL/image.jpg",
    "https://i.postimg.cc/gwCHNxqv/image.jpg",
    "https://i.postimg.cc/Z9BL883b/image.jpg",
    "https://i.postimg.cc/87nHfK7X/image.jpg",
    "https://i.postimg.cc/0zNnQRyJ/image.jpg",
    "https://i.postimg.cc/QHmShxh3/image.jpg",
    "https://i.postimg.cc/RN4Gknrd/image.jpg",
    "https://i.postimg.cc/YLw8qvvp/image.jpg",
    "https://i.postimg.cc/CnH7Zw8b/image.jpg",
    "https://i.postimg.cc/bDn3hxNC/image.jpg",
    "https://i.postimg.cc/4nzB2Q0n/image.jpg",
    "https://i.postimg.cc/06FcFWxK/image.jpg"
]

MINE_IMAGES_2 = [
    "https://i.postimg.cc/HVMzr9jQ/image.jpg",
    "https://postimg.cc/Rq7q3WWj",
    "https://postimg.cc/tnNg8c0X",
    "https://postimg.cc/7Cjbz7My",
    "https://postimg.cc/Hc5n9xB8",
    "https://postimg.cc/5HX6jpz3",
    "https://postimg.cc/Js6s1Ss0",
    "https://postimg.cc/LJ6qFm6G",
    "https://postimg.cc/MvYcLnxy",
    "https://postimg.cc/pyz5D06c",
    "https://postimg.cc/XpWGxfMj",
    "https://postimg.cc/30XyYRGQ",
    "https://postimg.cc/0KR6TmbC",
    "https://postimg.cc/hfRx6Fmq",
    "https://postimg.cc/7b20KPfV",
    "https://postimg.cc/jDsfqzvg",
    "https://postimg.cc/hf8xqC8Q",
    "https://postimg.cc/hXpdXf5S",
    "https://postimg.cc/rdHR97T3"
]

# Premium message template for both mine options
PREMIUM_MESSAGE = """<b>⚠️ 𝐈𝐌𝐏𝐎𝐑𝐓𝐀𝐍𝐓 𝐍𝐎𝐓𝐈𝐂𝐄 ⚠️</b>

<b>🎯 𝐅𝐫𝐞𝐞 𝐏𝐥𝐚𝐧 𝐀𝐜𝐜𝐮𝐫𝐚𝐜𝐲: 𝟔𝟎-𝟕𝟓%</b>
<b>⚠️ 𝐁𝐞𝐭 𝐬𝐦𝐚𝐥𝐥 𝐚𝐦𝐨𝐮𝐧𝐭𝐬 𝐨𝐧𝐥𝐲</b>
<b>⚡ 𝐏𝐥𝐚𝐲 𝐚𝐭 𝐲𝐨𝐮𝐫 𝐨𝐰𝐧 𝐫𝐢𝐬𝐤</b>

<b>💎 𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐭𝐨 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐟𝐨𝐫:</b>
<b>✅ 𝟏𝟎𝟎% 𝐀𝐜𝐜𝐮𝐫𝐚𝐜𝐲</b>
<b>✅ 𝐆𝐮𝐚𝐫𝐚𝐧𝐭𝐞𝐞𝐝 𝐖𝐢𝐧𝐬</b>
<b>✅ 𝐏𝐫𝐢𝐨𝐫𝐢𝐭𝐲 𝐒𝐮𝐩𝐩𝐨𝐫𝐭</b>

<b>👇 𝐂𝐥𝐢𝐜𝐤 𝐁𝐞𝐥𝐨𝐰 𝐭𝐨 𝐔𝐩𝐠𝐫𝐚𝐝𝐞 👇</b>"""


def start(update: Update, context: CallbackContext) -> None:
    """Handle the /start command."""
    try:
        # Send logo
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo="https://i.postimg.cc/tsdqqK8H/logo.png"
        )

        # Create start button
        keyboard = [[InlineKeyboardButton("🚀 𝐒𝐓𝐀𝐑𝐓 𝐍𝐎𝐖 🚀", callback_data="start_trading")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send welcome message
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=WELCOME_MESSAGE,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Error in start command: {str(e)}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="𝐒𝐨𝐫𝐫𝐲, 𝐬𝐨𝐦𝐞𝐭𝐡𝐢𝐧𝐠 𝐰𝐞𝐧𝐭 𝐰𝐫𝐨𝐧𝐠. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 𝐥𝐚𝐭𝐞𝐫."
        )


def button_callback(update: Update, context: CallbackContext) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    try:
        query.answer()  # Acknowledge the button press
        
        # Store the mines number if it's a mines selection
        if query.data.startswith("mines_"):
            mines_number = int(query.data.split("_")[1])
            context.user_data['selected_mines'] = mines_number

        if query.data == "start_trading":
            # Send video message
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=VIDEO_MESSAGE,
                parse_mode=ParseMode.HTML
            )

            # Send video thumbnail
            keyboard = [[InlineKeyboardButton("𝐖𝐀𝐓𝐂𝐇 𝐓𝐇𝐈𝐒 𝐕𝐈𝐃𝐄𝐎 𝐓𝐎 𝐊𝐍𝐎𝐖 𝐇𝐎𝐖 𝐓𝐎 𝐔𝐒𝐄 𝐓𝐇𝐈𝐒 𝐁𝐎𝐓", url="https://www.youtube.com/watch?v=r9Y35xwNPiI")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=f"https://img.youtube.com/vi/r9Y35xwNPiI/maxresdefault.jpg",
                reply_markup=reply_markup
            )

            # Send continue button
            keyboard = [[InlineKeyboardButton("🔄 𝐂𝐎𝐍𝐓𝐈𝐍𝐔𝐄 🔄", callback_data="continue_info")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=VIDEO_MESSAGE_AFTER,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )

        elif query.data == "continue_info":
            # Show VIP/FREE selection
            keyboard = [
                [
                    InlineKeyboardButton("👑 𝐕𝐈𝐏 𝐁𝐎𝐓 👑", callback_data="vip_selected"),
                    InlineKeyboardButton("⭐ 𝐅𝐑𝐄𝐄 𝐁𝐎𝐓 ⭐", callback_data="free_selected")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=INFO_MESSAGE,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )

        elif query.data == "vip_selected":
            # Show VIP plans
            keyboard = [
                [InlineKeyboardButton("₹𝟒𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_499")],
                [InlineKeyboardButton("₹𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_999")],
                [InlineKeyboardButton("₹𝟏𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_1999")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="𝐂𝐡𝐨𝐨𝐬𝐞 𝐲𝐨𝐮𝐫 𝐕𝐈𝐏 𝐩𝐥𝐚𝐧:",
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )

        elif query.data == "free_selected":
            # Check user's lifetime usage first
            user_id = update.effective_user.id
            if user_usage[user_id] >= MAX_FREE_USES:
                # User has exceeded lifetime free uses, show VIP plans
                keyboard = [
                    [InlineKeyboardButton("₹𝟒𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_499")],
                    [InlineKeyboardButton("₹𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_999")],
                    [InlineKeyboardButton("₹𝟏𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_1999")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="*⚠️ 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐞𝐱𝐡𝐚𝐮𝐬𝐭𝐞𝐝 𝐲𝐨𝐮𝐫 𝐥𝐢𝐟𝐞𝐭𝐢𝐦𝐞 𝐟𝐫𝐞𝐞 𝐮𝐬𝐞𝐬\! ⚠️*\n\n"
                         "*✅ 𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐭𝐨 𝐕𝐈𝐏 𝐭𝐨 𝐠𝐞𝐭:*\n"
                         "*✅ 𝐔𝐧𝐥𝐢𝐦𝐢𝐭𝐞𝐝 𝐮𝐬𝐞𝐬*\n"
                         "*✅ 𝐇𝐢𝐠𝐡𝐞𝐫 𝐚𝐜𝐜𝐮𝐫𝐚𝐜𝐲*\n"
                         "*✅ 𝐏𝐫𝐢𝐨𝐫𝐢𝐭𝐲 𝐬𝐮𝐩𝐩𝐨𝐫𝐭*\n"
                         "*✅ 𝐀𝐜𝐜𝐞𝐬𝐬 𝐭𝐨 𝐚𝐥𝐥 𝐦𝐢𝐧𝐞 𝐨𝐩𝐭𝐢𝐨𝐧𝐬*\n\n"
                         "*𝐂𝐡𝐨𝐨𝐬𝐞 𝐲𝐨𝐮𝐫 𝐕𝐈𝐏 𝐩𝐥𝐚𝐧 𝐛𝐞𝐥𝐨𝐰:*",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN_V2
                )
                return

            # Show full mine selection range with FREE and VIP options
            keyboard = [
                [InlineKeyboardButton("1️⃣ [𝐅𝐑𝐄𝐄] 🎮", callback_data="mines_1")],
                [InlineKeyboardButton("2️⃣ [𝐅𝐑𝐄𝐄] 🎮", callback_data="mines_2")],
                [InlineKeyboardButton("3️⃣ [VIP] 🎮", callback_data="mines_3")],
                [InlineKeyboardButton("4️⃣ [VIP] 🎮", callback_data="mines_4")],
                [InlineKeyboardButton("5️⃣ [VIP] 🎮", callback_data="mines_5")],
                [InlineKeyboardButton("6️⃣ [VIP] 🎮", callback_data="mines_6")],
                [InlineKeyboardButton("7️⃣ [VIP] 🎮", callback_data="mines_7")],
                [InlineKeyboardButton("8️⃣ [VIP] 🎮", callback_data="mines_8")],
                [InlineKeyboardButton("9️⃣ [VIP] 🎮", callback_data="mines_9")],
                [InlineKeyboardButton("🔟 [VIP] 🎮", callback_data="mines_10")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="𝐒𝐞𝐥𝐞𝐜𝐭 𝐭𝐡𝐞 𝐧𝐮𝐦𝐛𝐞𝐫 𝐨𝐟 𝐦𝐢𝐧𝐞𝐬 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐠𝐚𝐦𝐞:",
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )

        elif query.data.startswith("plan_"):
            # Handle plan selection
            plan_id = query.data.split("_")[1]
            
            # Display plan details
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=PLAN_MESSAGES[plan_id],
                parse_mode=ParseMode.HTML
            )
            
            # Display QR code for payment
            keyboard = [
                [InlineKeyboardButton("✅ 𝐃𝐨𝐧𝐞 𝐏𝐚𝐲𝐦𝐞𝐧𝐭", callback_data=f"payment_done_{plan_id}")],
                [InlineKeyboardButton("❌ 𝐂𝐚𝐧𝐜𝐞𝐥", callback_data="cancel_payment")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send QR code image
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=QR_CODES[plan_id],
                caption=PAYMENT_INFO,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
            
        elif query.data.startswith("payment_done_"):
            # Handle payment confirmation
            plan_id = query.data.split("_")[2]
            
            # Ask for a screenshot of payment
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="📸 𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝 𝐚 𝐬𝐜𝐫𝐞𝐞𝐧𝐬𝐡𝐨𝐭 𝐨𝐟 𝐲𝐨𝐮𝐫 𝐩𝐚𝐲𝐦𝐞𝐧𝐭 𝐟𝐨𝐫 𝐯𝐞𝐫𝐢𝐟𝐢𝐜𝐚𝐭𝐢𝐨𝐧.",
                parse_mode=ParseMode.HTML
            )
            
        elif query.data == "cancel_payment":
            # Return to plan selection
            keyboard = [
                [InlineKeyboardButton("₹𝟒𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_499")],
                [InlineKeyboardButton("₹𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_999")],
                [InlineKeyboardButton("₹𝟏𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_1999")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐜𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝. 𝐖𝐨𝐮𝐥𝐝 𝐲𝐨𝐮 𝐥𝐢𝐤𝐞 𝐭𝐨 𝐜𝐡𝐨𝐨𝐬𝐞 𝐚𝐧𝐨𝐭𝐡𝐞𝐫 𝐩𝐥𝐚𝐧?",
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            
        elif query.data.startswith("mines_"):
            # Handle mine game selection
            mines_number = query.data.split("_")[1]
            
            # Check if user has free uses left
            user_id = update.effective_user.id
            if user_usage[user_id] >= MAX_FREE_USES:
                # User has exceeded lifetime free uses, show VIP plans
                keyboard = [
                    [InlineKeyboardButton("₹𝟒𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_499")],
                    [InlineKeyboardButton("₹𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_999")],
                    [InlineKeyboardButton("₹𝟏𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_1999")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="*⚠️ 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐞𝐱𝐡𝐚𝐮𝐬𝐭𝐞𝐝 𝐲𝐨𝐮𝐫 𝐥𝐢𝐟𝐞𝐭𝐢𝐦𝐞 𝐟𝐫𝐞𝐞 𝐮𝐬𝐞𝐬\! ⚠️*\n\n"
                         "*✅ 𝐁𝐮𝐲 𝐕𝐈𝐏, 𝐲𝐨𝐮𝐫 𝐚𝐥𝐥 𝐟𝐫𝐞𝐞 𝐜𝐫𝐞𝐝𝐢𝐭𝐬 𝐚𝐫𝐞 𝐨𝐯𝐞𝐫\.*\n\n"
                         "*💎 𝐂𝐡𝐨𝐨𝐬𝐞 𝐲𝐨𝐮𝐫 𝐕𝐈𝐏 𝐩𝐥𝐚𝐧 𝐛𝐞𝐥𝐨𝐰:*",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN_V2
                )
                return
            
            # Check if it's a VIP option
            if int(mines_number) > 2:
                # Show premium plans for VIP options
                keyboard = [
                    [InlineKeyboardButton("₹𝟒𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_499")],
                    [InlineKeyboardButton("₹𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_999")],
                    [InlineKeyboardButton("₹𝟏𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_1999")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="⚠️ 𝐕𝐈𝐏 𝐅𝐞𝐚𝐭𝐮𝐫𝐞 ⚠️\n\n𝐓𝐡𝐢𝐬 𝐦𝐢𝐧𝐞 𝐨𝐩𝐭𝐢𝐨𝐧 𝐢𝐬 𝐨𝐧𝐥𝐲 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐟𝐨𝐫 𝐕𝐈𝐏 𝐮𝐬𝐞𝐫𝐬.\n𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐧𝐨𝐰 𝐭𝐨 𝐮𝐧𝐥𝐨𝐜𝐤 𝐚𝐥𝐥 𝐦𝐢𝐧𝐞 𝐨𝐩𝐭𝐢𝐨𝐧𝐬!",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Save mines selection in user_data
            context.user_data['selected_mines'] = int(mines_number)
            
            # Ask user to enter server seed
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="*📝 𝐄𝐧𝐭𝐞𝐫 𝐬𝐞𝐫𝐯𝐞𝐫 𝐬𝐞𝐞𝐝 𝐧𝐨𝐰\.*\n\n"
                     "*🔑 𝐒𝐞𝐞𝐝 𝐦𝐮𝐬𝐭 𝐛𝐞 𝐞𝐱𝐚𝐜𝐭𝐥𝐲 𝟔𝟒 𝐜𝐡𝐚𝐫𝐚𝐜𝐭𝐞𝐫𝐬 𝐥𝐨𝐧𝐠\.*\n"
                     "*📊 𝐄𝐱𝐚𝐦𝐩𝐥𝐞: 𝟏𝟖𝐚𝐛𝐚𝐜𝐟𝐜𝟕𝟖𝐜𝐚𝟏𝟒𝟑𝐛𝐛𝟒𝟔𝐞𝟗𝟕𝐞𝟐𝐚𝟖𝟖𝟖𝟐𝟖𝟏𝐞𝟔𝟕𝐜𝟖𝟗𝐞𝟗𝐞𝟔𝟗𝐜𝐝𝟒𝐚𝟗𝟓𝟖𝐜𝐝𝐟𝟖𝐟𝟑𝐚𝟗𝟐𝟕𝟏𝐞𝟎𝐟𝟒*",
                parse_mode=ParseMode.MARKDOWN_V2
            )
            
            # Set the waiting_for_seed flag
            context.user_data['waiting_for_seed'] = True
            
            # Record the mines number selection
            uses_left = MAX_FREE_USES - user_usage[user_id]
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"*🎮 𝐌𝐢𝐧𝐞𝐬 {mines_number} 𝐬𝐞𝐥𝐞𝐜𝐭𝐞𝐝\. 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 {uses_left} 𝐟𝐫𝐞𝐞 𝐮𝐬𝐞𝐬 𝐥𝐞𝐟𝐭\.*",
                parse_mode=ParseMode.MARKDOWN_V2
            )
            
        elif query.data.startswith("new_pattern_"):
            # Handle new pattern generation
            mines_number = query.data.split("_")[2]
            
            # Check user's lifetime usage first
            user_id = update.effective_user.id
            if user_usage[user_id] >= MAX_FREE_USES:
                # User has exceeded lifetime free uses, show VIP plans
                keyboard = [
                    [InlineKeyboardButton("₹𝟒𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_499")],
                    [InlineKeyboardButton("₹𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_999")],
                    [InlineKeyboardButton("₹𝟏𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_1999")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="*⚠️ 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐞𝐱𝐡𝐚𝐮𝐬𝐭𝐞𝐝 𝐲𝐨𝐮𝐫 𝐥𝐢𝐟𝐞𝐭𝐢𝐦𝐞 𝐟𝐫𝐞𝐞 𝐮𝐬𝐞𝐬\! ⚠️*\n\n"
                         "*✅ 𝐁𝐮𝐲 𝐕𝐈𝐏, 𝐲𝐨𝐮𝐫 𝐚𝐥𝐥 𝐟𝐫𝐞𝐞 𝐜𝐫𝐞𝐝𝐢𝐭𝐬 𝐚𝐫𝐞 𝐨𝐯𝐞𝐫\.*\n\n"
                         "*💎 𝐂𝐡𝐨𝐨𝐬𝐞 𝐲𝐨𝐮𝐫 𝐕𝐈𝐏 𝐩𝐥𝐚𝐧 𝐛𝐞𝐥𝐨𝐰:*",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN_V2
                )
                return
                
            # Increment user usage for free options
            user_usage[user_id] += 1
            
            # Get images for the selected mine option
            mine_images = MINE_IMAGES_1 if mines_number == "1" else MINE_IMAGES_2
            
            # Premium upgrade button
            keyboard = [
                [InlineKeyboardButton("💎 𝐔𝐩𝐠𝐫𝐚𝐝𝐞 𝐭𝐨 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 💎", callback_data="vip_selected")],
                [InlineKeyboardButton("🔄 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞 𝐍𝐞𝐰 𝐏𝐚𝐭𝐭𝐞𝐫𝐧 🔄", callback_data=f"new_pattern_{mines_number}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send premium message
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=PREMIUM_MESSAGE,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            
            # Send random mine image
            selected_image = random.choice(mine_images)
            uses_left = MAX_FREE_USES - user_usage[user_id]
            
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=selected_image,
                caption=f"*🎮 𝐍𝐞𝐰 𝐌𝐢𝐧𝐞𝐬 𝐏𝐚𝐭𝐭𝐞𝐫𝐧 \\({mines_number}\\) 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞𝐝*\n\n*⚠️ 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 {uses_left} 𝐟𝐫𝐞𝐞 𝐮𝐬𝐞𝐬 𝐥𝐞𝐟𝐭\\.*",
                parse_mode=ParseMode.MARKDOWN_V2
            )
            
        elif query.data == "validate_server_seed":
            # Show server seed validation message
            validate_server_seed(update, context)
            
    except Exception as e:
        logger.error(f"Error in button callback: {str(e)}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="𝐒𝐨𝐫𝐫𝐲, 𝐬𝐨𝐦𝐞𝐭𝐡𝐢𝐧𝐠 𝐰𝐞𝐧𝐭 𝐰𝐫𝐨𝐧𝐠. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 𝐥𝐚𝐭𝐞𝐫."
        )


def validate_server_seed(update: Update, context: CallbackContext) -> None:
    """Validate server seed and show mine selection."""
    try:
        # Check if user has free uses left
        user_id = update.effective_user.id
        if user_usage[user_id] >= MAX_FREE_USES:
            # User has exceeded lifetime free uses, show VIP plans
            keyboard = [
                [InlineKeyboardButton("₹𝟒𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_499")],
                [InlineKeyboardButton("₹𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_999")],
                [InlineKeyboardButton("₹𝟏𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_1999")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="*⚠️ 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐞𝐱𝐡𝐚𝐮𝐬𝐭𝐞𝐝 𝐲𝐨𝐮𝐫 𝐥𝐢𝐟𝐞𝐭𝐢𝐦𝐞 𝐟𝐫𝐞𝐞 𝐮𝐬𝐞𝐬\! ⚠️*\n\n"
                     "*✅ 𝐁𝐮𝐲 𝐕𝐈𝐏, 𝐲𝐨𝐮𝐫 𝐚𝐥𝐥 𝐟𝐫𝐞𝐞 𝐜𝐫𝐞𝐝𝐢𝐭𝐬 𝐚𝐫𝐞 𝐨𝐯𝐞𝐫\.*\n\n"
                     "*💎 𝐂𝐡𝐨𝐨𝐬𝐞 𝐲𝐨𝐮𝐫 𝐕𝐈𝐏 𝐩𝐥𝐚𝐧 𝐛𝐞𝐥𝐨𝐰:*",
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN_V2
            )
            return
        
        # Set seed validation mode
        context.user_data['waiting_for_seed'] = True

        # Send validation message
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*🔄 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐬𝐞𝐫𝐯𝐞𝐫 𝐬𝐞𝐞𝐝\.\.\.*",
            parse_mode=ParseMode.MARKDOWN_V2
        )
        
        # Send success message
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*✅ 𝐕𝐚𝐥𝐢𝐝𝐚𝐭𝐞𝐝*",
            parse_mode=ParseMode.MARKDOWN_V2
        )
        
        # Wait using sleep instead of asyncio
        time.sleep(1)
        
        # Send hacking message
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*🔓 𝐇𝐀𝐂𝐊𝐈𝐍𝐆*",
            parse_mode=ParseMode.MARKDOWN_V2
        )
        
        time.sleep(2)
        
        # Send processing message
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*⚡ 𝐏𝐑𝐎𝐂𝐄𝐒𝐒𝐈𝐍𝐆*",
            parse_mode=ParseMode.MARKDOWN_V2
        )
        
        time.sleep(2)
        
        # Show mine selection
        keyboard = [
            [InlineKeyboardButton("1️⃣ [𝐅𝐑𝐄𝐄] 🎮", callback_data="mines_1")],
            [InlineKeyboardButton("2️⃣ [𝐅𝐑𝐄𝐄] 🎮", callback_data="mines_2")],
            [InlineKeyboardButton("3️⃣ [VIP] 🎮", callback_data="mines_3")],
            [InlineKeyboardButton("4️⃣ [VIP] 🎮", callback_data="mines_4")],
            [InlineKeyboardButton("5️⃣ [VIP] 🎮", callback_data="mines_5")],
            [InlineKeyboardButton("6️⃣ [VIP] 🎮", callback_data="mines_6")],
            [InlineKeyboardButton("7️⃣ [VIP] 🎮", callback_data="mines_7")],
            [InlineKeyboardButton("8️⃣ [VIP] 🎮", callback_data="mines_8")],
            [InlineKeyboardButton("9️⃣ [VIP] 🎮", callback_data="mines_9")],
            [InlineKeyboardButton("🔟 [VIP] 🎮", callback_data="mines_10")],
            [InlineKeyboardButton("📞 𝐍𝐞𝐞𝐝 𝐇𝐞𝐥𝐩?", url="https://t.me/RichieRichKunal")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send message showing remaining free uses
        remaining_uses = MAX_FREE_USES - user_usage[user_id]
        
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"*𝐒𝐞𝐥𝐞𝐜𝐭 𝐭𝐡𝐞 𝐇𝐨𝐰 𝐌𝐚𝐧𝐲 𝐌𝐢𝐧𝐞𝐬⬇️*\n\n"
                 f"*📝 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 {remaining_uses} 𝐟𝐫𝐞𝐞 𝐮𝐬𝐞𝐬 𝐫𝐞𝐦𝐚𝐢𝐧𝐢𝐧𝐠\.*\n"
                 f"*💎 𝐂𝐨𝐧𝐬𝐢𝐝𝐞𝐫 𝐮𝐩𝐠𝐫𝐚𝐝𝐢𝐧𝐠 𝐭𝐨 𝐕𝐈𝐏 𝐟𝐨𝐫 𝐮𝐧𝐥𝐢𝐦𝐢𝐭𝐞𝐝 𝐚𝐜𝐜𝐞𝐬𝐬\!*",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN_V2
        )
        
    except Exception as e:
        logger.error(f"Error in validate_server_seed: {str(e)}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*❌ 𝐄𝐫𝐫𝐨𝐫\. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧\.*",
            parse_mode=ParseMode.MARKDOWN_V2
        )


def handle_photo(update: Update, context: CallbackContext) -> None:
    """Handle photo messages (payment screenshots)."""
    try:
        # Support button
        keyboard = [[InlineKeyboardButton("📞 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐒𝐮𝐩𝐩𝐨𝐫𝐭", url="https://t.me/RichieRichKunal")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send the support message
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=SUPPORT_MESSAGE,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        logger.error(f"Error in handle_photo: {str(e)}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="𝐒𝐨𝐫𝐫𝐲, 𝐬𝐨𝐦𝐞𝐭𝐡𝐢𝐧𝐠 𝐰𝐞𝐧𝐭 𝐰𝐫𝐨𝐧𝐠. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 𝐥𝐚𝐭𝐞𝐫."
        )


def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle text messages."""
    try:
        # Get the message text
        message = update.message.text
        
        # Check if we're waiting for a seed
        if context.user_data.get('waiting_for_seed', False):
            # Check if the message is a valid hexadecimal hash (64 characters)
            if len(message) == 64 and all(c in '0123456789abcdef' for c in message.lower()):
                # Reset waiting for seed flag
                context.user_data['waiting_for_seed'] = False
                
                # Check if user has free uses left
                user_id = update.effective_user.id
                if user_usage[user_id] >= MAX_FREE_USES:
                    # User has exceeded lifetime free uses, show VIP plans
                    keyboard = [
                        [InlineKeyboardButton("₹𝟒𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_499")],
                        [InlineKeyboardButton("₹𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_999")],
                        [InlineKeyboardButton("₹𝟏𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_1999")]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="*⚠️ 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐞𝐱𝐡𝐚𝐮𝐬𝐭𝐞𝐝 𝐲𝐨𝐮𝐫 𝐥𝐢𝐟𝐞𝐭𝐢𝐦𝐞 𝐟𝐫𝐞𝐞 𝐮𝐬𝐞𝐬\! ⚠️*\n\n"
                             "*✅ 𝐁𝐮𝐲 𝐕𝐈𝐏, 𝐲𝐨𝐮𝐫 𝐚𝐥𝐥 𝐟𝐫𝐞𝐞 𝐜𝐫𝐞𝐝𝐢𝐭𝐬 𝐚𝐫𝐞 𝐨𝐯𝐞𝐫\.*\n\n"
                             "*💎 𝐂𝐡𝐨𝐨𝐬𝐞 𝐲𝐨𝐮𝐫 𝐕𝐈𝐏 𝐩𝐥𝐚𝐧 𝐛𝐞𝐥𝐨𝐰:*",
                        reply_markup=reply_markup,
                        parse_mode=ParseMode.MARKDOWN_V2
                    )
                    return
                
                # Increment usage counter
                user_usage[user_id] += 1
                
                # Send success message
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="*✅ 𝐕𝐚𝐥𝐢𝐝𝐚𝐭𝐞𝐝*",
                    parse_mode=ParseMode.MARKDOWN_V2
                )
                
                # Wait for 1 second
                time.sleep(1)
                
                # Send hacking message
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="*🔓 𝐇𝐀𝐂𝐊𝐈𝐍𝐆*",
                    parse_mode=ParseMode.MARKDOWN_V2
                )
                
                # Wait for 2 seconds
                time.sleep(2)
                
                # Send processing message
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="*⚡ 𝐏𝐑𝐎𝐂𝐄𝐒𝐒𝐈𝐍𝐆*",
                    parse_mode=ParseMode.MARKDOWN_V2
                )
                
                # Wait for 2 seconds
                time.sleep(2)
                
                try:
                    # Get the selected number of mines
                    selected_mines = context.user_data.get('selected_mines', 2)  # Default to 2 if not set
                    # Send random mine image based on selected mines
                    random_image = random.choice(MINE_IMAGES_1 if selected_mines == 1 else MINE_IMAGES_2)
                    context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=random_image,
                        caption="*🎯 𝐆𝐞𝐧𝐞𝐫𝐚𝐭𝐞𝐝 𝐌𝐢𝐧𝐞 𝐏𝐚𝐭𝐭𝐞𝐫𝐧*",
                        parse_mode=ParseMode.MARKDOWN_V2
                    )
                    
                    # Send premium plan message with VIP button
                    keyboard = [
                        [InlineKeyboardButton("💎 𝐁𝐮𝐲 𝐕𝐈𝐏 𝐏𝐥𝐚𝐧 💎", callback_data="vip_selected")]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=PREMIUM_MESSAGE,
                        reply_markup=reply_markup,
                        parse_mode=ParseMode.HTML
                    )
                    
                except Exception as e:
                    logger.error(f"Error sending mine image: {str(e)}", exc_info=True)
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="*❌ 𝐄𝐫𝐫𝐨𝐫\. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧\.*",
                        parse_mode=ParseMode.MARKDOWN_V2
                    )
                
            else:
                # Invalid seed format
                keyboard = [[InlineKeyboardButton("📞 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐒𝐮𝐩𝐩𝐨𝐫𝐭", url="https://t.me/RichieRichKunal")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="*❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐒𝐞𝐞𝐝\. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧\.*",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN_V2
                )
            
            return  # Exit after processing seed
        
        # Not in seed mode, check if message contains seed keywords
        message_text = update.message.text.lower()
        if "seed" in message_text or "hash" in message_text:
            validate_server_seed(update, context)
        else:
            # Send the standard welcome message with logo
            # Send logo first
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo="https://i.postimg.cc/tsdqqK8H/logo.png"
            )
            
            # Create start button
            keyboard = [[InlineKeyboardButton("🚀 𝐒𝐓𝐀𝐑𝐓 𝐍𝐎𝐖 🚀", callback_data="start_trading")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send welcome message
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=WELCOME_MESSAGE,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            
    except Exception as e:
        logger.error(f"Error in handle_message: {str(e)}")
        # Show VIP plans keyboard
        keyboard = [
            [InlineKeyboardButton("₹𝟒𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_499")],
            [InlineKeyboardButton("₹𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_999")],
            [InlineKeyboardButton("₹𝟏𝟗𝟗𝟗 𝐏𝐥𝐚𝐧", callback_data="plan_1999")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*⚠️ 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐞𝐱𝐡𝐚𝐮𝐬𝐭𝐞𝐝 𝐲𝐨𝐮𝐫 𝐥𝐢𝐟𝐞𝐭𝐢𝐦𝐞 𝐟𝐫𝐞𝐞 𝐮𝐬𝐞𝐬\! ⚠️*\n\n"
                 "*✅ 𝐁𝐮𝐲 𝐕𝐈𝐏, 𝐲𝐨𝐮𝐫 𝐚𝐥𝐥 𝐟𝐫𝐞𝐞 𝐜𝐫𝐞𝐝𝐢𝐭𝐬 𝐚𝐫𝐞 𝐨𝐯𝐞𝐫\.*\n\n"
                 "*💎 𝐂𝐡𝐨𝐨𝐬𝐞 𝐲𝐨𝐮𝐫 𝐕𝐈𝐏 𝐩𝐥𝐚𝐧 𝐛𝐞𝐥𝐨𝐰:*",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN_V2
        )


def main() -> None:
    """Start the bot."""
    try:
        # Create updater and pass it the bot's token
        updater = Updater(TOKEN)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # Add command handlers
        dispatcher.add_handler(CommandHandler("start", start))
        
        # Add button callback handler
        dispatcher.add_handler(CallbackQueryHandler(button_callback))
        
        # Add message handlers
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

        # Start the bot
        logger.info("Starting bot")
        updater.start_polling()
        
        # Run the bot until the user presses Ctrl-C
        updater.idle()
        
    except Exception as e:
        logger.error(f"Critical error in main: {str(e)}")


if __name__ == "__main__":
    main()
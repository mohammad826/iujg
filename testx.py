import nest_asyncio
import asyncio
import os
import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# تنظیمات لاگینگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# رفع مشکل event loop
nest_asyncio.apply()

# توکن ربات تلگرام از متغیر محیطی
token = token = '7382326726:AAFcagIRc5dlcGEm6o_iDsNISp35ho5IZhc'

# تابع برای ارسال منوی اصلی
async def send_main_menu(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    keyboard = [
        ['آموزش', 'خرید'],  
        ['درباره ما', 'تماس با ما']  
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await context.bot.send_message(chat_id=chat_id, text='لطفاً یکی از گزینه‌ها را انتخاب کنید:', reply_markup=reply_markup)

# تابع برای ارسال منوی آموزش
async def send_education_menu(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    keyboard = [
        ['گرفتن توکن با گوشی', 'گرفتن توکن با لپ‌تاپ'],
        ['بازگشت']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await context.bot.send_message(chat_id=chat_id, text='لطفاً یکی از گزینه‌ها را انتخاب کنید:', reply_markup=reply_markup)

# تابع برای ارسال منوی بازگشت
async def send_back_menu(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    keyboard = [['بازگشت']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await context.bot.send_message(chat_id=chat_id, text='لطفاً یکی از گزینه‌ها را انتخاب کنید:', reply_markup=reply_markup)

# مدیریت دستور /start
async def start(update: Update, context: CallbackContext):
    try:
        chat_id = update.message.chat_id
        welcome_text = """
        👋 سلام! خوش آمدید به ربات مدیریت وظایف GOATS!
        🤖 این ربات طراحی شده تا به شما کمک کند تسک‌ها و کارهای GOATS خود را به صورت اتوماتیک انجام دهید و زمان ارزشمندتان را ذخیره کنید.
        ⚙️ با استفاده از منوی زیر، امکانات و گزینه‌های مختلف را مشاهده و انتخاب کنید.
        """
        await context.bot.send_message(chat_id=chat_id, text=welcome_text)
        await send_main_menu(update, context)
    except Exception as e:
        logger.error(f"Error in start: {e}")
        await context.bot.send_message(chat_id=chat_id, text='متاسفانه خطایی پیش آمد. لطفاً دوباره تلاش کنید.')

# مدیریت پیام‌ها
async def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    try:
        if text == 'خرید':
            await context.bot.send_message(chat_id=chat_id, text="""\
🤖 یه ربات اومده خودش اتوماتیک همه کارای GOATS را برایت انجام می دهد 😵
⚙️ امکانات
📼 هر دقیقه برایت ویدیو ها را می بیند و ۲۰۰ GOATS برایت می گیرد 
📑 تمام تسک های GOATS را برایت انجام می دهد 
🪪 ربات هم روی توکن خودت ران می شود تا امنیت بیشتری داشته باشید و اما نگران نباشید روی سرور خودم برایتان ران می کنم
♾️ و ...
💠 [لینک ربات](https://t.me/miner_GOATS_BOT)
🏷 جهت خرید اشتراک ربات به آیدی زیر پیام دهید.
@Mxoprg""")
            await send_back_menu(update, context)

        elif text == 'آموزش':
            await send_education_menu(update, context)

        elif text == 'گرفتن توکن با گوشی':
            video_path = 'path/to/your/video_for_phone.mp4'  # مسیر ویدیو
            await context.bot.send_video(chat_id=chat_id, video=open(video_path, 'rb'), caption='آموزش گرفتن توکن با گوشی:')
            await send_back_menu(update, context)

        elif text == 'گرفتن توکن با لپ‌تاپ':
            video_path = 'path/to/your/video_for_laptop.mp4'  # مسیر ویدیو
            await context.bot.send_video(chat_id=chat_id, video=open(video_path, 'rb'), caption='آموزش گرفتن توکن با لپ‌تاپ:')
            await send_back_menu(update, context)

        elif text == 'بازگشت':
            await send_main_menu(update, context)

        elif text == 'تماس با ما':
            await context.bot.send_message(chat_id=chat_id, text='برای تماس با ما لطفاً به ایمیل aztdaz.12345@gmail.com پیام دهید.')
            await send_back_menu(update, context)

        elif text == 'درباره ما':
            await context.bot.send_message(chat_id=chat_id, text='این ربات برای کمک به کاربران در مدیریت وظایف روزانه طراحی شده است.')
            await send_back_menu(update, context)

    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        await context.bot.send_message(chat_id=chat_id, text='متاسفانه خطایی پیش آمد. لطفاً دوباره تلاش کنید.')

# راه‌اندازی ربات تلگرام
async def main():
    try:
        application = Application.builder().token(token).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        await application.run_polling()
    except Exception as e:
        logger.critical(f"Error in main: {e}")

if __name__ == '__main__':
    asyncio.run(main())

from telegram import Update, ChatMember
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext
import re

# ✅ توکن شما
TOKEN = '173684458:AAGT9ayDFlGLLiDICySaS8ekqh00y1uBWfo'

# ✅ لیست آیدی عددی کاربرانی که اجازه دارند لینک بفرستند
allowed_users = [914543964]

user_violations = {}

async def is_admin(update: Update, user_id: int):
    try:
        member = await update.message.chat.get_member(user_id)
        return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except:
        return False

async def check_message(update: Update, context: CallbackContext):
    if not update.message or not update.message.text:
        return

    # ✅ این خط را اضافه کردم تا هر بار کسی پیام بدهد، آیدی عددی و یوزرنیمش را ببینی
    username = update.message.from_user.username or "بدون یوزرنیم"
    user_id = update.message.from_user.id
    print(f"Username: @{username} — User ID: {user_id}")

    message = update.message.text
    chat_id = update.message.chat.id
    group_name = update.message.chat.title if update.message.chat.title else "گروه"

    if contains_link_or_id(message):
        # اگر کاربر مجاز بود یا مدیر بود لینک آزاد است
        if user_id in allowed_users or await is_admin(update, user_id):
            return

        # حذف پیام
        try:
            await update.message.delete()
        except Exception as e:
            print(f"خطا در حذف پیام: {e}")

        # ثبت تخلف
        user_violations[user_id] = user_violations.get(user_id, 0) + 1
        violations = user_violations[user_id]

        if violations >= 3:
            try:
                await context.bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
                await context.bot.send_message(chat_id=user_id,
                    text="با توجه به عدم رعایت قوانین گروه توسط شما و ارسال سه پیام حاوی لینک، "
                         "حساب کاربری شما در گروه مسدود شده است.\n"
                         "در صورت نیاز به رفع مسدودیت به مدیر گروه به آدرس @sharifsoft_chat پیام دهید.\n"
                         "متشکرم.")
            except Exception as e:
                print(f"خطا در بلاک کردن یا ارسال پیام خصوصی: {e}")
        else:
            try:
                await context.bot.send_message(chat_id=user_id,
                    text=f"با توجه به ارسال لینک در گروه {group_name} توسط شما که مغایر با قوانین گروه است، "
                         "پیام شما توسط ربات پاک شد.\n"
                         "لطفاً از ارسال هرگونه لینک در گروه خودداری فرمایید.\n"
                         "در صورت ارسال مجدد لینک متاسفانه در گروه بلاک خواهید شد.\n"
                         "متشکرم.")
            except Exception as e:
                print(f"خطا در ارسال پیام خصوصی: {e}")

def contains_link_or_id(text):
    # ✅ این الگو لینک‌هایی با یا بدون http یا www و همچنین آیدی تلگرامی را شناسایی می‌کند
    link_pattern = r'((http|https):\/\/[^\s]+|www\.[^\s]+|\b[\w\-]+\.(com|ir|net|org|info|co|me|site|online)\b|t\.me\/[^\s]+|@[\w\d_]+)'
    return re.search(link_pattern, text, re.IGNORECASE) is not None

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
    app.run_polling()

if __name__ == '__main__':
    main()

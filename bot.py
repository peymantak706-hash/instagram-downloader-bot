# bot.py - ربات دانلود اینستاگرام (از صفر)
import os
from instagrapi import Client
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# توکن ربات تلگرام
TOKEN = "8091200704:AAERTcMQUNbYqr_Uj1t1Cb169yPw_8ydeHg"

# فایل session ذخیره‌شده
SESSION_FILE = "session.json"
DOWNLOAD_FOLDER = "downloads"

# ایجاد پوشه دانلود
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# اتصال به اینستاگرام
cl = Client()
if os.path.exists(SESSION_FILE):
    cl.load_settings(SESSION_FILE)
else:
    print("❌ فایل session.json وجود ندارد! ابتدا login.py را اجرا کنید.")
    exit()

print("🤖 ربات در حال راه‌اندازی...")

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📥 سلام! لینک اینستاگرام رو بفرست تا برات دانلود کنم!\n"
        "پست، استوری یا هایلایت — همه چیز!"
    )

# پردازش لینک
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if "instagram.com" not in url:
        await update.message.reply_text("🚫 لطفاً یک لینک معتبر اینستاگرام بفرستید.")
        return

    try:
        await update.message.reply_text("⏳ در حال دریافت اطلاعات از اینستاگرام...")

        # پاک کردن فایل‌های قبلی
        for file in os.listdir(DOWNLOAD_FOLDER):
            file_path = os.path.join(DOWNLOAD_FOLDER, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # تشخیص نوع لینک
        if "/p/" in url or "/reel/" in url or "/tv/" in url:
            media_pk = cl.media_pk_from_url(url)
            media_info = cl.media_info(media_pk)

            if media_info.media_type == 1:  # عکس
                file_path = cl.photo_download(media_pk, folder=DOWNLOAD_FOLDER)
                with open(file_path, 'rb') as f:
                    await update.message.reply_photo(f, caption="✅ عکس دانلود شد!")
                os.remove(file_path)

            elif media_info.media_type == 2 and media_info.product_type != "clip":  # ویدیو
                file_path = cl.video_download(media_pk, folder=DOWNLOAD_FOLDER)
                with open(file_path, 'rb') as f:
                    await update.message.reply_video(f, caption="✅ ویدیو دانلود شد!")
                os.remove(file_path)

            else:
                await update.message.reply_text("نوع محتوا پشتیبانی نمی‌شود.")

        elif "/stories/" in url:
            user_id = url.split("/stories/")[1].split("/")[0]
            stories = cl.user_stories(user_id)
            if not stories:
                await update.message.reply_text("❌ استوری‌ای یافت نشد.")
                return
            for story in stories:
                if story.media_type == 1:
                    file_path = cl.story_download(story.pk, folder=DOWNLOAD_FOLDER)
                    with open(file_path, 'rb') as f:
                        await update.message.reply_photo(f)
                    os.remove(file_path)
                elif story.media_type == 2:
                    file_path = cl.story_download(story.pk, folder=DOWNLOAD_FOLDER)
                    with open(file_path, 'rb') as f:
                        await update.message.reply_video(f)
                    os.remove(file_path)
            await update.message.reply_text("✅ استوری دانلود شد!")

        elif "/highlights/" in url:
            highlight_id = url.split("highlights/")[-1].split("/")[0]
            highlights = cl.highlights_stories(highlight_id)
            if not highlights:
                await update.message.reply_text("❌ هایلایت یافت نشد.")
                return
            for item in highlights:
                if item.media_type == 1:
                    file_path = cl.story_download(item.pk, folder=DOWNLOAD_FOLDER)
                    with open(file_path, 'rb') as f:
                        await update.message.reply_photo(f)
                    os.remove(file_path)
                elif item.media_type == 2:
                    file_path = cl.story_download(item.pk, folder=DOWNLOAD_FOLDER)
                    with open(file_path, 'rb') as f:
                        await update.message.reply_video(f)
                    os.remove(file_path)
            await update.message.reply_text("✅ هایلایت دانلود شد!")

        else:
            await update.message.reply_text("🔗 این نوع لینک پشتیبانی نمی‌شود.")

    except Exception as e:
        await update.message.reply_text(f"❌ خطایی رخ داد: {str(e)}")

# اجرای ربات
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    print("🚀 ربات با موفقیت راه‌اندازی شد! (/start کنید)")
    app.run_polling()

if __name__ == "__main__":
    main()
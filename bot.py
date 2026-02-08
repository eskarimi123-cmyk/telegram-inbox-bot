import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("8563381643:AAGWcP1XOHR3lb6yTUMfyMFnDEZDbQAeT8A")
ADMINS = {93457614}  # آیدی عددی خودت

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "پیام‌تون رو بنویسید؛ به ادمین ارسال می‌شه و پاسخ همینجا میاد."
    )

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text or "[پیام غیرمتنی]"

    msg = (
        f"📩 پیام جدید\n"
        f"از: {user.full_name} (@{user.username})\n"
        f"user_id: {user.id}\n\n"
        f"{text}"
    )

    for admin in ADMINS:
        await context.bot.send_message(chat_id=admin, text=msg)

    await update.message.reply_text("✅ پیام شما ارسال شد.")

async def admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    await update.message.reply_text("برای پاسخ از دستور /reply استفاده کن.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.User(list(ADMINS)), user_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.User(list(ADMINS)), admin_message))
    app.run_polling()

if __name__ == "__main__":
    main()

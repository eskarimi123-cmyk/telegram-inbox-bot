import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "پیامت رو همینجا بنویس. به ادمین ارسال میشه و پاسخ هم همینجا میاد."
    )

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # اگر خود ادمین پیام داد، این handler نباید اجرا بشه
    if update.effective_user and update.effective_user.id == ADMIN_ID:
        return

    user = update.effective_user
    text = update.message.text or "[پیام غیرمتنی]"

    msg_to_admin = (
        f"📩 پیام جدید\n"
        f"از: {user.full_name} (@{user.username})\n"
        f"user_id: {user.id}\n\n"
        f"{text}"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=msg_to_admin)
    await update.message.reply_text("✅ پیام شما ارسال شد.")

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # فقط ادمین اجازه پاسخ
    if update.effective_user.id != ADMIN_ID:
        return

    # باید روی پیام قبلی (که user_id داخلش هست) ریپلای کنی
    if not update.message.reply_to_message:
        await update.message.reply_text("برای جواب دادن، روی پیام کاربر ریپلای کن.")
        return

    original = update.message.reply_to_message.text or ""

    # user_id را از متن پیدا می‌کنیم
    target_user_id = None
    for line in original.splitlines():
        if line.strip().startswith("user_id:"):
            try:
                target_user_id = int(line.split(":", 1)[1].strip())
            except:
                target_user_id = None
            break

    if not target_user_id:
        await update.message.reply_text("user_id پیدا نشد. روی پیام اصلی کاربر ریپلای کن.")
        return

    reply_text = update.message.text or ""
    await context.bot.send_message(chat_id=target_user_id, text=f"✉️ پاسخ ادمین:\n{reply_text}")
    await update.message.reply_text("✅ پاسخ ارسال شد.")

def main():
    if not TOKEN or ADMIN_ID == 0:
        raise RuntimeError("TOKEN و ADMIN_ID باید به صورت Environment Variables تنظیم شوند.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_message))
    # پاسخ ادمین فقط وقتی ریپلای کرده باشد
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, admin_reply))

    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()

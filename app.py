from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Replace this with your Bot Token from BotFather
BOT_TOKEN = "7600496017:AAGD6_VhsgFMbWhr89E2_SCUH87nZobgeT8"

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello, Welcome to the Bot! Use /help to see available commands."
    )

# Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Available Commands:
/youtube - To get the YouTube URL
/linkedin - To get the LinkedIn profile URL
/gmail - To get the Gmail URL
/geeks - To get the GeeksforGeeks URL""")

# Custom Command: YouTube Link
async def youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("YouTube Link => https://www.youtube.com/")

# Custom Command: LinkedIn Link
async def linkedin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("LinkedIn URL => https://www.linkedin.com/")

# Custom Command: Gmail Link
async def gmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gmail Link => https://www.gmail.com/")

# Custom Command: GeeksforGeeks Link
async def geeks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("GeeksforGeeks URL => https://www.geeksforgeeks.org/")

# Unknown Command Handler
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Sorry, '{update.message.text}' is not a valid command. Use /help to see available commands."
    )

# Unknown Text Handler
async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Sorry, I can't understand you. You said: '{update.message.text}'"
    )

def main():
    # Create the Application and pass the bot token
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("youtube", youtube))
    app.add_handler(CommandHandler("linkedin", linkedin))
    app.add_handler(CommandHandler("gmail", gmail))
    app.add_handler(CommandHandler("geeks", geeks))

    # Add message handlers for unknown commands and texts
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_text))

    # Start the bot
    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()

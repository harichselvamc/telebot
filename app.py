import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Telegram Bot Token
BOT_TOKEN = "7600496017:AAGD6_VhsgFMbWhr89E2_SCUH87nZobgeT8"


# Check for GPU availability and set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load Qwen Model and Tokenizer
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
print("Loading the model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, 
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map=None  # Disable automatic device map
).to(device)  # Move the model explicitly to the selected device
print("Model loaded successfully!")

# Helper function to generate response using Qwen
def generate_llm_response(user_input):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input}
    ]

    # Prepare input using the chat template
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    
    # Tokenize and send input to model
    inputs = tokenizer([text], return_tensors="pt").to(device)
    output_ids = model.generate(
        **inputs, 
        max_new_tokens=200, 
        do_sample=True, 
        temperature=0.7
    )
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your AI assistant powered by Qwen LLM. Send me any text, and I will respond!")

# Handle User Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await update.message.reply_text("🤖 Generating response... Please wait.")

    # Generate response using LLM
    response = generate_llm_response(user_input)
    await update.message.reply_text(response)

# Unknown Command Handler
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sorry, I did not understand that command. Use /start to begin.")

# Main Function
def main():
    print("Starting the bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Run the bot
    print("Bot is running. Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()

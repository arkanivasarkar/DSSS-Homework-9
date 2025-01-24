import asyncio
import nest_asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai


TELEGRAM_BOT_API_KEY = "7973329175:AAG-sjol8gBS1Uba-cpTPpPB67zAZIqbD0s"
GEMINI_API_KEY = "AIzaSyBaHQJxdszWX0TsWeEkwExVpbIPnEhlPFk"


# Apply nest_asyncio for interactive environments
nest_asyncio.apply()


# Gemini API Configuration
genai.configure(api_key=GEMINI_API_KEY)
GEMINI_LLM_MODEL = genai.GenerativeModel("gemini-1.5-flash")


# Function to query Gemini API to use Gemini LLM
def query_gemini(prompt: str) -> str:
    """
    Sends the user input (prompt) to the Gemini API and returns the response.
    """
    response = GEMINI_LLM_MODEL.generate_content(prompt,
                                                 generation_config = genai.GenerationConfig(
                                                     max_output_tokens=1000,
                                                     temperature=0.7)
                                                 ) 
    return response.text



# Telegram Command: Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends a greeting message when the /start command is issued.
    """
    await update.message.reply_text(
        "Hi there! I'm your AI Assistant. Ask me anything, like sharing facts about your favorite animal!"
    )


# Telegram Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Processes user messages, queries the LLM, and sends the response.
    """
    # User's message
    user_message = update.message.text

    # Query the Gemini LLM with the user's message
    ai_response = query_gemini(user_message)

    # Respond back to the user with the LLM's answer
    await update.message.reply_text(ai_response)

    # Log the conversation to the console
    print(f"User: {user_message}")
    print(f"AI Assistant: {ai_response}")


# Main Function
async def main():

    # Set up the Telegram application
    application = Application.builder().token(TELEGRAM_BOT_API_KEY).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Telegram bot is running...")
    await application.run_polling()


# Run
if __name__ == "__main__":
    asyncio.run(main())

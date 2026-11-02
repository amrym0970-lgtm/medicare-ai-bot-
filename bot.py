
import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

ai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
You are MediCare AI, a helpful health information assistant.
Speak Arabic, Iraqi Arabic, or English depending on the user.
Provide general health information in simple language.
Never claim to diagnose diseases or prescribe medication.
For urgent or serious symptoms, advise contacting a medical professional.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بيك في MediCare AI!\n"
        "أنا مساعدك الذكي للمعلومات الصحية 🩺\n"
        "اسألني أي سؤال."
    )

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text

    try:
        response = ai.responses.create(
            model="gpt-4.1-mini",
            instructions=SYSTEM_PROMPT,
            input=question
        )

        await update.message.reply_text(response.output_text)

    except Exception:
        logging.exception("AI request failed")
        await update.message.reply_text(
            "عذراً، صار خطأ مؤقت. حاول مرة ثانية."
        )

def main():
    app = Application.builder().token(
        os.environ["TELEGRAM_BOT_TOKEN"]
    ).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

    app.run_polling()

if __name__ == "__main__":
    main()

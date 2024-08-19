import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv
import os
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import requests
import json
from database import Engine, FAQS, session
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

VOTE , AI_ROBOT  = range(2)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.message.reply_text(
        "🤖 من پاسخگو هوشمند هستم. سوالات شما را بر اساس داکیومنت زیر جواب میدهم. 🤖 \n"
        "https://filtershekan.sbs/ \n\n "
        "تمامی مکالمات و همچنین ای دی شما ذخیره می شود از ارسال اطلاعات شخصی و پسورد پرهیز کنید. \n\n"
        "برای کنسل کردن مکالمه /cancel را تایپ کنید.\n\n"
        "📞 سوالات خود را به صورت فارسی یا انگلیسی بپرسید. 📞",
    )
    
    return AI_ROBOT



def ai_curl(message : str ) :
    obj = {'text': message}

    try:
        x =  requests.post(os.environ.get("AI_URL"), json = obj)
    except Exception as e:
        logger.warning("AI Response Error: %s", str(e))
        return "" , "" , ""
        

    if x.status_code != 200:
        logger.warning("AI Response Error: %s", x.status_code)
        return "" , "" , ""
      
    json_message = json.loads(x.text)
    return json_message['message']
  




async def ai_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
  user = update.message.from_user
  message = update.message.text  
  await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ لطفا چند دقیقه صبر کنید")
  
  ai_response = ai_curl(message)
  
  if ai_response == "" :
      await context.bot.send_message(chat_id=update.effective_chat.id, text="Internal Error has been occurred") 
      return -1
    
  await context.bot.send_message(chat_id=update.effective_chat.id, text=ai_response)
    
  faq = FAQS(question=message,
             user_id=user.id,
             answer=ai_response)
  session.add(faq)
  session.commit()  
  
  context.user_data['faq'] = faq
  
  return AI_ROBOT
  
  
       
  
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
  
    

def main():
    
    load_dotenv(".env")
    application = ApplicationBuilder().token(os.environ.get("TOKEN")).build()

    # Add conversation handler with the states 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AI_ROBOT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ai_answer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == '__main__':
    main()
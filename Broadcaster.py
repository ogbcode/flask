import pymysql
import telegram
from telegram.ext import Updater, CommandHandler,Filters,MessageHandler
import Constants as keys
# Replace YOUR_TOKEN with your Telegram bot token
bot = telegram.Bot(token=keys.API_KEY)
mydb = pymysql.connect(
  host=keys.host,
  user=keys.user,
  port=keys.port,
  password=keys.dbpassword,
  database=keys.database
)

cursor = mydb.cursor()

def broadcast_start(update,context):
    chat_id = update.message.chat_id 
    if(chat_id==1591573930):
        cursor.execute("SELECT chatid from broadcast_table")
        rows = cursor.fetchall()
        global broadcast_chatid
        broadcast_chatid=[]
        for row in rows:
            broadcast_chatid.append(row[0])
        context.bot.send_message(chat_id=update.message.chat_id, text='send The message you would like to broadcast please send it precisely')
        global messx
        messx=MessageHandler(Filters.video | Filters.photo | Filters.text, broadcast_message)
        dp.add_handler(messx)
    else:
        context.bot.send_message(chat_id=chat_id,text="you dont have access to this command")
def broadcast_message(update, context):
    chat_id = update.message.chat_id 
    if(chat_id==1591573930):
        try:
            message = update.message
            caption = message.caption
            text = message.text if message.text else None
            photo = message.photo if message.photo else None
            video = message.video if message.video else None
            if photo:
                count=0
                fail=0
                for i in broadcast_chatid:
                    try:
                        message=context.bot.send_photo(chat_id=int(i), photo=photo[-1].file_id, caption=caption)
                        count=count+1
                    except:
                        fail=fail+1
                        continue
                context.bot.send_message(chat_id=1591573930,text=f"the photo message was succefully sent to {count} people and unsucesfully to {fail} people")
                dp.remove_handler(messx)
            elif video:
                count=0
                fail=0
                for i in broadcast_chatid:
                    try:
                        message=context.bot.send_video(chat_id=int(i), video=video.file_id,caption=caption)
                        count=count+1
                    except:
                        fail=fail+1
                        continue
                context.bot.send_message(chat_id=1591573930,text=f"the video message was succefully sent to {count} people unsucesfully to {fail} people")
                dp.remove_handler(messx)
            elif text:
                count=0
                fail=0
                message_tobroadcast =update.message.text
                for i in broadcast_chatid:
                    try:
                        message=context.bot.send_message(chat_id=int(i), text=message_tobroadcast)
                        count=count+1
                    except:
                        fail=fail+1
                        continue
                message=context.bot.send_message(chat_id=1591573930,text=f"the text message was succefully sent to {count} people unsucesfully to {fail} people")
                dp.remove_handler(messx)
            else:
                message=context.bot.send_message(chat_id=update.message.chat_id, text="i dont understand what you have sent please send a text ,image or video")
                dp.remove_handler(messx)
        except:
            context.bot.send_message(chat_id=1591573930,text="broadcast message failed")
    else:
        context.bot.send_message(chat_id=chat_id,text="you dont have access to this command")
def broadcasterror(update,context):
    err=str(f"Update{update} caused error {context.error}")
    context.bot.send_message(err)
    
def Broadcastermain(updater,dpw):
    global dp
    dp=dpw
    dp.add_error_handler(broadcasterror)
    dp.add_handler(CommandHandler('broadcast',broadcast_start))
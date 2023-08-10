from flask import Flask, jsonify
import os

app = Flask(__name__)

import json
import threading
import time
import pymysql
import requests
import VipMembership
from flask import Flask, request
import telegram
import hmac
import hashlib
from datetime import datetime, timedelta
import Constants as keys
import Broadcaster
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import Updater, CommandHandler,MessageHandler,Filters
# set up your Telegram bot
bot = telegram.Bot(token=keys.API_KEY)
group_chat_id =keys.groupchatid
membership_duration = 30

mydb = pymysql.connect(
  host=keys.host,
  user=keys.user,
  port=keys.port,
  password=keys.dbpassword,
  database=keys.database
)

cursor = mydb.cursor()
test_key=keys.test_key

app = Flask(__name__)
def verify_paystack_webhook(payload, secret_key, signature):
    generated_signature = hmac.new(
    secret_key.encode(),
    payload,
    hashlib.sha512
).hexdigest()
    # Compare the generated signature with the one sent with the webhook
    if generated_signature == signature:
        return True
    else:
        return False

def is_paystack_webhook(headers):
    if 'X-Paystack-Signature' in headers :
        return True
    else:
        return False
@app.route('/')
def test():
    return{"message":"Membership bot is up and running"}

@app.route('/paystackreceiver', methods=['POST'])
def webhook():
    event_data = json.loads(request.data)
    # Verify the event signature using your secret key
    headers = request.headers
    signature = request.headers.get('X-Paystack-Signature')
    verify_url = 'https://api.paystack.co/transaction/verify/%s' % (event_data['data']['reference'])
    response = requests.get(verify_url, headers={'Authorization': 'Bearer %s' % test_key})
    request_data = request.data
    response_data = response.json()
    if is_paystack_webhook(headers):
        if(verify_paystack_webhook(request_data,keys.test_key,signature)):
            if response_data['status'] != True or response_data['data']['status'] != 'success':
                return 'Verification failed', 400

            # Retrieve the payment status from the event data
            payment_status = event_data['data']['status']

            # Perform an action based on the payment status
            if payment_status == 'success':
                try:
                    # print(response_data)
                    d=response_data["data"]["metadata"]["custom_fields"]
                    global plan
                    plan=response_data["data"]["metadata"]["referrer"]
                    try:
                        for value in d:
                            chat_id=(value["value"])
                        query="SELECT chatid from broadcast_table where chatid= %s"
                        values=[chat_id]
                        cursor.execute(query,values)
                        rows = cursor.fetchall()
                        chatid=int(rows[0][0])
                        add_user_to_group(chatid)
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)

    return 'Webhook received', 200

# function to add user to group
def New_Memeber(update, context):
    try:
        new_member = update.message.new_chat_members[0]
        query=("INSERT INTO group_members VALUES (%s,%s,%s,%s)")
        now = datetime.now()
        join_date=now.strftime("%Y-%m-%d")
        if(plan==keys.twoweekssub):
            x=14
        elif(plan==keys.onemonthsub):
            x=30
        elif(plan==keys.lifetimesub):
            x=99999
        expirydate=now+timedelta(days=x)
        final_Expirydate=expirydate.strftime("%Y-%m-%d")
        chatid_user=new_member.id
        username=new_member.username
        first_name = new_member.first_name

        values=(str(first_name),str(chatid_user),join_date,final_Expirydate)
        cursor.execute(query,values)
        mydb.commit()
        context.bot.send_message(chat_id=new_member.id, text="Welcome to the group, " + new_member.first_name + "!"+" Click /status to view how many days you have left")
    except Exception as e:
        print(e)

def dbconnect(update,context):
    try:
        global mydb
        global cursor
        mydb.close()
        cursor.close()
        mydb = pymysql.connect(
        host=keys.host,
        user=keys.user,
        port=keys.port,
        password=keys.dbpassword,
        database=keys.database
        )
        cursor = mydb.cursor()
        context.bot.send_message(chat_id=update.effective_chat.id, text="db initiation was sucessfull")
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="db initiation not sucessfull")
def dbconnectfinal():
    while True:
        try:
            global mydb
            global cursor
            mydb.close()
            cursor.close()

            mydb = pymysql.connect(
            host=keys.host,
            user=keys.user,
            port=keys.port,
            password=keys.dbpassword,
            database=keys.database
            )
            cursor = mydb.cursor()
            bot.send_message(chat_id=1591573930, text="db initiation was sucessfull")
        except:
            bot.send_message(chat_id=1591573930, text="db initiation not sucessfull")
        time.sleep(43200)
def add_user_to_group(user_id):
    try:
        invite_link = bot.export_chat_invite_link(chat_id=group_chat_id, timeout=180)
        succesfull= InlineKeyboardButton(text="Join Vip Group🏆", url=invite_link)
        succesful_markup = InlineKeyboardMarkup([[succesfull]])
        bot.send_message(chat_id=user_id,text='Your Payment was succesful✅✅', reply_markup=succesful_markup)
    except Exception as e:
        print(e)

def remove_user_from_group():
    cursor.execute("SELECT * from  group_members")
    rows = cursor.fetchall()
    for i in rows:
        chatid=int(i[1])
        username=i[0]
        expiry_date= datetime.strptime(i[3],'%Y-%m-%d')
        timeleft=expiry_date-datetime.now()
        if timeleft<=timedelta(days=0):
            try:
                bot.send_message(chat_id=chatid, text="Your 💰VIP membership subscription has ended and you have been removed from the VIP group click 👉👉👉 /start 👈👈👈 to Renew it")
                bot.kick_chat_member(chat_id=group_chat_id, user_id=chatid)
                query="DELETE FROM group_members WHERE chatid = %s"
                value=[(str(chatid))]
                cursor.execute(query,value)
                mydb.commit()
                bot.send_message(chat_id=1591573930, text=f"User {username} subscription has expired and has been removed from the vip group✅")
            except Exception as e:
                print(e)
                continue
        else:
            pass
def checkallmembers(update,context):
    if (update.effective_chat.id==1591573930):
        remove_user_from_group()
        allcheck()
    else:
        bot.send_message(chat_id=update.effective_chat.id,text="you dont have access to this command")
def all_commands(update, context):
    if (update.effective_chat.id==1591573930):
        allcommands="/start\n/checkallmembers-Check VIP memebers\n/status-Shows Vip status\n/startdb-restart database\n/broadcast-Broadcast message\n/help-help"
        bot.send_message(chat_id=update.effective_chat.id,text=allcommands)
    else:
        bot.send_message(chat_id=update.effective_chat.id,text="you dont have access to this command")
def membershipwarning():
    cursor.execute("SELECT * from  group_members")
    rows = cursor.fetchall()
    for i in rows:
        chatid=int(i[1])
        expiry_date= datetime.strptime(i[3],'%Y-%m-%d')
        timeleft=expiry_date-datetime.now()
        if timedelta(days=0)<timeleft<=timedelta(days=4):
            try:
                timeleft=str(timeleft)
                daysleft=timeleft.split(",")
                bot.send_message(chat_id=chatid, text="Reminder you have" + " "+ daysleft[0] +" "+ "in the the Vip channel!\n Click /start /start /start To renew it when it Ends💰")
            except:
                continue
def allcheck():
    queryx="SELECT * from  group_members"
    cursor.execute(queryx)
    rows = cursor.fetchall()
    for i in rows:
        username=i[0]
        expiry_date= datetime.strptime(i[3],'%Y-%m-%d')
        timeleft=expiry_date-datetime.now()
        timeleft=str(timeleft)
        daysleft=timeleft.split(",")
        time_days=daysleft[0].split("days")
        years = int(time_days[0]) //365
        days = int(time_days[0]) % 365
        if(years==0):
            bot.send_message(chat_id=1591573930,  text=f"{username} has {days} days left in the vip channel✅")
        else:
            bot.send_message(chat_id=1591573930, text=f"{username} has {years} years and {days} days left in the vip channel✅")
def membershipstatus(update,context):
    query2="SELECT * from  group_members where chatid=%s"
    value=[update.effective_chat.id]
    cursor.execute(query2,value)
    rows = cursor.fetchall()
    if rows:
        for i in rows:
            expiry_date= datetime.strptime(i[3],'%Y-%m-%d')
            timeleft=expiry_date-datetime.now()
            timeleft=str(timeleft)
            daysleft=timeleft.split(",")
            time_days=daysleft[0].split("days")
            years = int(time_days[0]) //365
            days = int(time_days[0]) % 365
            if(years==0):
                bot.send_message(chat_id=update.effective_chat.id, text=f"you have {str(days)} days left in the the Vip channel ✅✅")
            else:
                bot.send_message(chat_id=update.effective_chat.id, text=f"you have {str(years)} years and {str(days)} days left in the the Vip channel ✅✅")
    else:
        bot.send_message(chat_id=update.effective_chat.id, text="You are not a member of the Vip Group. Click 👉👉👉 /start /start /start  👈👈👈 to join today")
def error(update,context):
    print(f"Update{update} caused error {context.error}")

def membercheck():
    while True:
        membershipwarning()
        remove_user_from_group()
        time.sleep(43200)
def finalfunc():
    updater=Updater(keys.API_KEY,use_context=True)
    dp=updater.dispatcher
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler("status",membershipstatus))
    dp.add_handler(CommandHandler("allcommands",all_commands))
    dp.add_handler(CommandHandler("startdb",dbconnect))
    dp.add_handler(CommandHandler('add_user', add_user_to_group))
    dp.add_handler(CommandHandler('checkallmembers',checkallmembers))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,New_Memeber))
    
    VipMembership.main(updater,dp)
    Broadcaster.Broadcastermain(updater,dp)
    updater.start_polling()

bot_thread = threading.Thread(target=finalfunc)
bot_thread.start()
membershipcheck=threading.Thread(target=membercheck)
membershipcheck.start()
dbreconnect=threading.Thread(target=dbconnectfinal)
dbreconnect.start
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

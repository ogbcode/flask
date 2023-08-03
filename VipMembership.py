import asyncio
from datetime import datetime
import smtplib
from email.message import EmailMessage
import ssl
import pymysql
import Constants as keys
import re
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
# Connect to MySQL database
mydb = pymysql.connect(
  host=keys.host,
  user=keys.user,
  port=keys.port,
  password=keys.dbpassword,
  database=keys.database
)
cursor = mydb.cursor()
def start_command(update,context):
    
    username = update.message.from_user.username
    firstname=update.message.chat.first_name
    if username:
        pass
    else:
        username=""
    chatid=update.effective_chat.id
    try:
        query=("INSERT INTO broadcast_table VALUES (%s,%s)")
        values=[str(firstname),str(chatid)]
        cursor.execute(query,values)
        mydb.commit()
    except:
        pass
    services= [[InlineKeyboardButton(f"VIP SIGNALS {keys.twoweekprice}/2 weeeks 🚨", callback_data=f'VIP {keys.twoweekprice} (2weeks)')],
                 [InlineKeyboardButton(f"VIP SIGNALS {keys.onemonthprice}/1 Month 🚨" , callback_data=f'VIP {keys.onemonthprice} (1month)')],
                 [InlineKeyboardButton(f"VIP SIGNALS {keys.lifetimeprice}/Lifetime 🚨", callback_data=f'VIP {keys.lifetimeprice} (lifetime)')],
                 [InlineKeyboardButton("PROPFIRM ACCOUNT PASSING 🚨", callback_data= "PASSAGE")]]
    reply_markup = InlineKeyboardMarkup(services)
    
    logging.info(f"{username} started the bot.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! " +firstname)
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Use This bot To get Acces to Pips Matrix Services✅✅")
    update.message.reply_text("""🚨PipsmatrixFx Signals
    
Your Benefits:
⚡️Detailed Chart analysis
⚡️2-4 Signals Daily
⚡️Swing trades
⚡️Day Trades
⚡️Fundamental Trades and Analysis
⚡️Live Trading and Q/A Session
""", reply_markup=reply_markup)

def Back_command(update,context):
    query = update.callback_query
    services= [[InlineKeyboardButton(f"VIP SIGNALS {keys.twoweekprice}/2 weeeks 🚨", callback_data=f'VIP {keys.twoweekprice} (2weeks)')],
                 [InlineKeyboardButton(f"VIP SIGNALS {keys.onemonthprice}/1 Month 🚨" , callback_data=f'VIP {keys.onemonthprice} (1month)')],
                 [InlineKeyboardButton(f"VIP SIGNALS {keys.lifetimeprice}/Lifetime 🚨", callback_data=f'VIP {keys.lifetimeprice} (lifetime)')],
                 [InlineKeyboardButton("PROPFIRM ACCOUNT PASSING 🚨", callback_data= "PASSAGE")]]
    reply_markup = InlineKeyboardMarkup(services)
    query.edit_message_text(text="""🚨PipsmatrixFx Signals
Your Benefits:
⚡️Detailed Chart analysis
⚡️2-4 Signals Daily
⚡️Swing trades
⚡️Day Trades
⚡️Fundamental Trades and Analysis
⚡️Live Trading and Q/A Session
""", reply_markup=reply_markup)
def service_callback(update,context):
    query = update.callback_query
    global planselected
    planselected = query.data   
    paymentmethods = [
        [InlineKeyboardButton("Bank Transfer🏦/Credit Card💳" , callback_data='Payment (Bank )')],
        [InlineKeyboardButton("⚡️BTC(Bitcoin)", callback_data='Payment(CryptoBTC)')],
         [InlineKeyboardButton("💲USDT(TRC20)", callback_data='Payment (CryptoUSDT)')],
         [InlineKeyboardButton("<<<Back ", callback_data='Back')],]
    payment_markup = InlineKeyboardMarkup(paymentmethods)
    trial=planselected.split()
    query.edit_message_text(text=f'📈PipsmatrixFx VIP Signals📈\n\nYour benefits:\n✅PipsmatrixFx VIP(Channel Access)\nPrice:{trial[1]}\nBilling period:{trial[2]}\nBilling mode:Non recurring ', reply_markup=payment_markup)
    # query.edit_message_text(text=f'You have selected {planselected}. Please select a payment method:', reply_markup=payment_markup)

def PropBack_command(update,context):
    query = update.callback_query
    global propfirm_account
    propfirm_account=query.data
    Account_size=[[InlineKeyboardButton("💲5000 Passing fee:$50", callback_data='PROPFIRM 50 $5000')],
                 [InlineKeyboardButton("💲10,000 Passing fee:$100" , callback_data='PROPFIRM 100 $10,000')],
                 [InlineKeyboardButton("💲20,000 Passing fee:$200", callback_data='PROPFIRM 200 $20,000')],
                [InlineKeyboardButton("💲50,000 Passing fee:$300", callback_data= 'PROPFIRM 300 $50,000')],
                [InlineKeyboardButton("💲100,000 Passing fee:$500", callback_data='PROPFIRM 500 $100,000')],
                [InlineKeyboardButton("💲200,000 Passing fee:$700", callback_data='PROPFIRM 700 $200,000')],
                [InlineKeyboardButton("💲300,000 Passing fee:$900", callback_data='PROPFIRM 900 $300,000')],
                [InlineKeyboardButton("💲<<<Back", callback_data='Back')]]
    Account_size_markup = InlineKeyboardMarkup(Account_size)
    
    query.edit_message_text(text='What Account Size would you like to pass:', reply_markup=Account_size_markup)

def Propfirm(update,context):
    query = update.callback_query
    propfirm_account=query.data
    Account_size= [[InlineKeyboardButton("💲5000 Passing fee:$50", callback_data='PROPFIRM 50 $5000')],
                [InlineKeyboardButton("💲10,000 Passing fee:$100" , callback_data='PROPFIRM 100 $10,000 ')],
                [InlineKeyboardButton("💲20,000 Passing fee:$200", callback_data='PROPFIRM 200 $20,000')],
                [InlineKeyboardButton("💲50,000 Passing fee:$300", callback_data='PROPFIRM 300  $50,000')],
                [InlineKeyboardButton("💲100,000 Passing fee:$500", callback_data='PROPFIRM 500 $100,000')],
                [InlineKeyboardButton("💲200,000 Passing fee:$700", callback_data='PROPFIRM 700 $200,000')],
                [InlineKeyboardButton("💲300,000 Passing fee:$900", callback_data='PROPFIRM 900 $300,000')],
                [InlineKeyboardButton("<<<Back", callback_data='Back')]]
    Account_size_markup = InlineKeyboardMarkup(Account_size)
    
    query.edit_message_text(text='What Account Size would you like to pass:', reply_markup=Account_size_markup)

def proppay_callback(update,context):
    query = update.callback_query
    global Prop_planselected
    Prop_planselected = query.dataS
    res = Prop_planselected.split()
    global payment_amount
    global propaccount_size
    payment_amount=res[1]   
    propaccount_size=res[2]
    paymentmethods = [
        [InlineKeyboardButton("Bank Transfer🏦" , callback_data='PrPay (Bank)')],
        [InlineKeyboardButton("⚡️BTC(Bitcoin)", callback_data='PrPay(CryptoBTC)')],
        [InlineKeyboardButton("💲USDT(TRC20)", callback_data='PrPay (CryptoUSDT)')],
        [InlineKeyboardButton("<<<Back ", callback_data='bacpr')],]
    payment_markup = InlineKeyboardMarkup(paymentmethods)
    query.edit_message_text(text=f'🏆PropFirm Account passing🏆\n\nPassing Fee:${payment_amount}\nAccount size:{propaccount_size}\n\nPlease select a Payment method:', reply_markup=payment_markup)

def propfirmpay_callback(update,context):
    query=update.callback_query
    query.answer()
    Prop_payment=query.data

    if (Prop_payment=='PrPay(CryptoBTC)'):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Send ${payment_amount} for the {propaccount_size} Account passing to this BTC(Bitcoin) wallet\n\n Send the Transaction Receipt✅ and Account login details to @Pipsmatrixcustomersupport")
        context.bot.send_message(chat_id=update.effective_chat.id,text=keys.btc_address)

    if (Prop_payment=='PrPay (CryptoUSDT)'):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Send ${payment_amount} for the {propaccount_size} Account passing to this USDT TRC20 wallet\n\n Send the Transaction Receipt✅ and Account login details to @Pipsmatrixcustomersupport")
        context.bot.send_message(chat_id=update.effective_chat.id,text=keys.usdt_trc20)

    if ( Prop_payment=='PrPay (Bank)'):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Contact @Pipsmatrixcustomersupport For Payment details")
   
def Payment_callback(update, context):
    query = update.callback_query
    query.answer()
    payment_method= query.data
    if (planselected==f'VIP {keys.twoweekprice} (2weeks)' and ( payment_method=='Payment (Bank )')):
        url=keys.twoweekssub
        username = update.effective_user.username
        button = InlineKeyboardButton(text="💳 Subscribe", url=url)
        subscribe_markup = InlineKeyboardMarkup([[button]])
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Your telegram id is:{update.effective_chat.id} You will need it at checkout!\n\nProceed with Payment.', reply_markup=subscribe_markup)
   
    if (planselected==f'VIP {keys.onemonthprice} (1month)' and ( payment_method=='Payment (Bank )')):
        url=keys.onemonthsub
        username = update.effective_user.username
        button = InlineKeyboardButton(text="💳 Subscribe", url=url)
        subscribe_markup = InlineKeyboardMarkup([[button]])
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Your telegram id is:{update.effective_chat.id} You will need it at checkout!\n\nProceed with Payment.', reply_markup=subscribe_markup)
   
    if(planselected==f'VIP {keys.lifetimeprice} (lifetime)'and (payment_method=='Payment (Bank )')):
        url=keys.lifetimesub
        username = update.effective_user.username
        button = InlineKeyboardButton(text="💳 Subscribe", url=url)
        subscribe_markup = InlineKeyboardMarkup([[button]])
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Your telegram id:{update.effective_chat.id} You will need it at checkout!\n\nProceed with Payment.', reply_markup=subscribe_markup)

    if (payment_method=='Payment(CryptoBTC)'):
        trial=planselected.split()
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Send {trial[1]} for the {trial[0]} {trial[2]} plan to this BTC(Bitcoin) wallet\n\n Send the Transaction Receipt✅ to @Pipsmatrixcustomersupport")
        context.bot.send_message(chat_id=update.effective_chat.id,text=keys.btc_address)

    if (payment_method=='Payment (CryptoUSDT)'):
        trial=planselected.split()
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Send {trial[1]} for the {trial[0]} {trial[2]} plan to this USDT TRC20 wallet\n\n Send the Transaction Receipt✅ to @Pipsmatrixcustomersupport")
        context.bot.send_message(chat_id=update.effective_chat.id,text=keys.usdt_trc20)


def help_command(update,context):
    update.message.reply_text("Please contact @Pipsmatrixcustomersupport For more payment options or any issues faced")


def main(updater,dp):
    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(CommandHandler("help",help_command))

    dp.add_handler(CallbackQueryHandler(Propfirm,pattern=re.compile(r'\b\w*PASSAGE\w*\b')))
    dp.add_handler(CallbackQueryHandler(Back_command,pattern=re.compile(r'\b\w*Back\w*\b')))
    dp.add_handler(CallbackQueryHandler(service_callback,pattern = re.compile(r'\b\w*VIP\w*\b')))
    dp.add_handler(CallbackQueryHandler(Payment_callback,pattern=re.compile(r'\b\w*Payment\w*\b')))
    dp.add_handler(CallbackQueryHandler(PropBack_command,pattern=re.compile(r'\b\w*bacpr\w*\b')))
    dp.add_handler(CallbackQueryHandler(proppay_callback,pattern=re.compile(r'\b\w*PROPFIRM\w*\b')))
    dp.add_handler(CallbackQueryHandler(propfirmpay_callback,pattern=re.compile(r'\b\w*PrPay\w*\b')))

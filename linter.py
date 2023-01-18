from telegram import Update , ReplyKeyboardMarkup ,MessageEntity
from telegram.ext import ApplicationBuilder, ConversationHandler , CommandHandler , MessageHandler , ContextTypes,filters
from openpyxl import load_workbook
import pandas as pd
from random import randint
from datetime import date , timedelta

menu = [['review','find word']]
markup = ReplyKeyboardMarkup(menu,one_time_keyboard=True)
path = '/Users/chartex/Downloads/linter.xlsx'
menu,findWord,addOrNot,addWord,isTrue = range(5)
sheet = pd.read_excel(path)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user['first_name']
    Entity = [{'offset':6,'length':len(name),'type':'bold'}]
    await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker='CAACAgQAAxkBAAEG_BhjpwzaE0_WGWvzgT9r-BK0Yy60GQACiwgAAmfHiVJJMa5s69pZ0iwE')
    await context.bot.send_message(chat_id= update.effective_chat.id, text=f'salam {name} joon khosh umadi\nomidvaram emruz kalamehaye khubi yad begirim',reply_markup=markup,entities=Entity)
    return menu

async def get_word(updat:Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=updat.effective_chat.id,text='lotfan kalameye mored nazar ro beman begu')
    return findWord

async def find_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global word
    word = update.message.text.lower()
    # sheet = load_workbook(path).active
    # mydict = {}
    # for x,y in sheet[f'A1:B{sheet.max_row}']:
    #     mydict[x.value] = y.value
    #     mydict[y.value] = x.value
    # if word in mydict.keys():
    if sheet[sheet.kalame == word].bool:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'in kalame hast\n{sheet[sheet.kalame == word].mani.item()}')
        return menu
    else:
        await context.bot.send_sticker(chat_id=update.effective_chat.id,sticker='CAACAgQAAxkBAAEG_BJjpwlt0zHspfumsnhjHC2mTjvOjQACBAoAAvZRiVL44lglOLvBKCwE')
        await context.bot.send_message(chat_id=update.effective_chat.id,text='in kalame tuye dictionary nist.\nmikhay ezafe konim?',reply_markup=ReplyKeyboardMarkup([['YES','NO']]))
        # answer = await update.message.text
        # if answer == 'YES':
        #     context.bot.send_message(chat_id=update.effective_chat.id,text='eyval')
        return addOrNot

async def Error(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text='dastor ya linki ke behem midi eshtebahe')
    return menu

async def start_review(update: Update,context: ContextTypes.DEFAULT_TYPE):
    global review_word
    def reviewWord():
        w = sheet[sheet.date <= date.today()].kalame.get(randint(1,sheet.last_valid_index()))
        return w
    while True:
        review_word = reviewWord()
        if review_word:
            await context.bot.send_message(chat_id=update.effective_chat.id,text=review_word)
            mani = sheet[sheet.kalame == review_word].mani.item()
            await context.bot.send_message(chat_id=update.effective_chat.id,text= mani ,entities=[{'offset':0,'length':len(mani),'type':'spoiler'}])
            await context.bot.send_message(chat_id=update.effective_chat.id,text='balad budi?',reply_markup=ReplyKeyboardMarkup([['yes','no']],one_time_keyboard=True))
            break    
    return isTrue

async def get_mean(updat: Update, context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=updat.effective_chat.id,text='hala ke mikhay ezafe koni lotfan mani kalame ro be man bede')
    return addWord

#TODO eslah beshe ba pandas
async def add_word(update: Update,context:ContextTypes.DEFAULT_TYPE):
    mean = update.message.text.lower()
    wb = load_workbook(path)
    sheet = wb.active
    max_row = sheet.max_row
    sheet[f'A{max_row}'] = word
    sheet[f'B{max_row}'] = mean    
    wb.save(path)
    await context.bot.send_message(chat_id=update.effective_chat.id,text='kalameye jadid save shod\nbargashtim menuye asli hala chikar konim?????',reply_markup=markup)
    return menu

async def return_menu(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text='bargashtim menuye asli hala chikar konim?????',reply_markup=markup)
    return menu

async def check_review(update:Update,context:ContextTypes.DEFAULT_TYPE):
    a = update.message.text
    if a == 'yes':
        status_list = [1,3,5,7,15,30]
        i = sheet.index[sheet.kalame == review_word].item()
        old_status = sheet[sheet.index == i].status.item()
        sheet.at[i,'date'] +=  timedelta(days= old_status)
        sheet.at[i,'status'] = status_list[status_list.index(old_status)+1]
    await context.bot.send_message(chat_id=update.effective_chat.id,text='mikhay edame bedi?',reply_markup=ReplyKeyboardMarkup([['yes','no']],one_time_keyboard=True))
    return menu

def main():
    application = ApplicationBuilder().token('5024895126:AAGbQ7OBTxoiMxtdPtwATDNSzgY6Qlvcj7o').build()
    conv_handler = ConversationHandler(
        entry_points= [CommandHandler('start',start)],
        states= {
            menu : [MessageHandler(filters.Regex('^review$'),start_review),
                    MessageHandler(filters.Regex('^find word$'),get_word)],
            findWord: [MessageHandler(filters.Regex('.*'),find_word)],
            addOrNot: [MessageHandler(filters.Regex('^YES$'),get_mean),
                       MessageHandler(filters.Regex('^NO$'),return_menu)],
            addWord: [MessageHandler(filters.Regex('.*'),add_word)],
            isTrue: [MessageHandler(filters.Regex('.*'),check_review)]
        },
        fallbacks= []
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
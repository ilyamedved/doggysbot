from PIL import Image, ImageDraw, ImageFont
#from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime 
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, CallbackQuery, InputFile 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state, State, StatesGroup

BOT_TOKEN = "399139355:AAGHxC5TD6N117PY4P_UFjtsb7G41CXCXOI"
class play(StatesGroup):
    choisedate = State()
    choisetime = State()
    choiseperson = State()
    choisepersondate = State()
    cancel = State()
    mode = State()
# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()

def Draw_timetable(file_path, dts, mr, ev, weeknum): #draws jpeg with timetable on the week number = weeknum.
    new_img = Image.open(file_path +"eek_matrix.jpg")
    font = ImageFont.truetype("arial.ttf", 14)
    pencil = ImageDraw.Draw(new_img)
    fname = file_path + "eek"+str(weeknum)+".jpg"
    for i in range(7):
        if mr[i].upper() == "СП":
            r = 153
            g = 204
            b = 255
            pencil.rectangle([40+i*32, 14+0*32, 65+i*32, 39+0*32],fill = (r, g, b, 0), outline = 'black', width = 1)
            pencil.text((40+3+i*32, 18),mr[i]  , font=font, fill='black')
        if ev[i].upper() == "СП":
            r = 153
            g = 204
            b = 255
            pencil.rectangle([40+i*32, 14+1*32, 65+i*32, 39+1*32],fill = (r, g, b, 0), outline = 'black', width = 1)
            pencil.text((40+3+i*32, 18+32*1),ev[i]  , font=font, fill='black')
        if mr[i].upper() == "ММ":
            r = 255
            g = 153
            b = 204
            pencil.rectangle([40+i*32, 14+0*32, 65+i*32, 39+0*32],fill = (r, g, b, 0), outline = 'black', width = 1)
            pencil.text((40+3+i*32, 18),mr[i]  , font=font, fill='black')
        if ev[i].upper() == "ММ":
            r = 255
            g = 153
            b = 204
            pencil.rectangle([40+i*32, 14+1*32, 65+i*32, 39+1*32],fill = (r, g, b, 0), outline = 'black', width = 1)
            pencil.text((40+3+i*32, 18+32*1),ev[i]  , font=font, fill='black')
        if mr[i].upper() == "КН":
            r = 255
            g = 153
            b = 51
            pencil.rectangle([40+i*32, 14+0*32, 65+i*32, 39+0*32],fill = (r, g, b, 0), outline = 'black', width = 1)
            pencil.text((40+3+i*32, 18),mr[i]  , font=font, fill='black')
        if ev[i].upper() == "КН":
            r = 255
            g = 153
            b = 51
            pencil.rectangle([40+i*32, 14+1*32, 65+i*32, 39+1*32],fill = (r, g, b, 0), outline = 'black', width = 1)
            pencil.text((40+3+i*32, 18+32*1),ev[i]  , font=font, fill='black')
        if mr[i].upper() == "КА":
            r = 191
            g = 191
            b = 191
            pencil.rectangle([40+i*32, 14+0*32, 65+i*32, 39+0*32],fill = (r, g, b, 0), outline = 'black', width = 1)
            pencil.text((40+3+i*32, 18),mr[i]  , font=font, fill='black')
        if ev[i].upper() == "КА":
            r = 191
            g = 191
            b = 191
            pencil.rectangle([40+i*32, 14+1*32, 65+i*32, 39+1*32],fill = (r, g, b, 0), outline = 'black', width = 1)
            pencil.text((40+3+i*32, 18+32*1),ev[i]  , font=font, fill='black')
    # Let's draw dates.
    font = ImageFont.truetype("arial.ttf", 9)

    for i in range(7):
        dt = dts[i].split("-")[2] + "." + dts[i].split("-")[1]
        pencil.rectangle([40+i*32, 1, 65+i*32, 12],fill = (255, 255, 255, 0), outline = 'white', width = 0)
        pencil.text((40+3+i*32, 1),dt, font=font, fill=(80, 80, 80, 0))
    #os.remove(fname)
    new_img.save(fname)

def get_stats(fname):
    fin = open(fname,"r", encoding="utf-8")
    stat = [[0,0,0,0],[0,0,0,0]]
    td = datetime.date.today()
    #stat[1] = [0,0,0,0] #number of evening doggy walks. СП, ММ, КА, КН.
    strng = fin.readline()
    while strng !="": #strng ="" <=> EOF is reached.
        print(strng)
        spl = strng.split() # w[0] is date, w[1] is morning, w[2] is evening.
        print(datetime.date(int(str(spl[0].split('-')[0])),int(str(spl[0].split('-')[1])),int(str(spl[0].split('-')[2]))))
        if datetime.date(int(str(spl[0].split('-')[0])),int(str(spl[0].split('-')[1])),int(str(spl[0].split('-')[2]))) <= td:
            if spl[1] == 'СП':
                stat[0][0] += 1
            if spl[1] == 'ММ':
                stat[0][1] += 1
            if spl[1] == 'КА':
                stat[0][2] += 1
            if spl[1] == 'КН':
                stat[0][3] += 1
            if spl[2] == 'СП':
                stat[1][0] += 1
            if spl[2] == 'ММ':
                stat[1][1] += 1
            if spl[2] == 'КА':
                stat[1][2] += 1
            if spl[2] == 'КН':
                stat[1][3] += 1
        strng = fin.readline()
    fin.close()
    return stat

def put_into(fname,dt,morning,person):
    #fname = имя файла где хранится,dt = дата что записать, morning =0 <=> утро, person = кто гуляет.
    fnameout = fname.rstrip(".txt") + "1.txt"
    fout = open(fnameout,"w", encoding="utf-8")
    fin = open(fname,"r", encoding="utf-8")
    strng = fin.readline()
    fl = False # True <=> date is found un the file.
    cerdt = datetime.date(int(str(dt).split('-')[0]),int(str(dt).split('-')[1]),int(str(dt).split('-')[2])) # это certain date - точно дата, независимо от того, подали str or date.
    print(cerdt)
    while strng !="": #strng ="" <=> EOF is reached.
        spl = strng.split() # w[0] is date, w[1] is morning, w[2] is evening.
        #print(spl[0].split('-')[0])
        if datetime.date(int(spl[0].split('-')[0]),int(spl[0].split('-')[1]),int(spl[0].split('-')[2])) == cerdt:   
            print("this is the line we searsching for")
            strng = spl[0] + " "
            if morning == 0:
                strng = strng + person.upper() + " " + spl[2] + "\n"
            else:
                #print("evening")
                strng = strng + spl[1] + " " + person.upper()+ "\n"
            fl = True
            print(strng)
        fout.write(strng)
        strng = fin.readline()
    print("flag =",fl)
    if not fl:
        # Have to enter a new line cause the date was not found in the file.        
        print("there is no such data in the file. Let's form and insert a new one.")
        strng = str(cerdt) + " "
        if morning == 0:
            strng = strng + person.upper() + " ПУ"
        else:
            strng = strng + "ПУ " + person.upper()  
        fout.write('\n' + strng)
    fin.close()
    fout.close()
    # Let's delete previous file and rename new.
    os.remove(fname)
    os.rename(fnameout, fname)

# -------------------------------------------- Инициализация -----------------------------------
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)
# Создание клавиатуры
def get_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐕Расписание"), KeyboardButton(text="🐾 Взять день")],
            [KeyboardButton(text="📊Статистика"), KeyboardButton(text="🚫Отменить выбор")] ],
        resize_keyboard=True,  # Подгоняет размер кнопок
        input_field_placeholder="Чего изволите?"  # Подсказка в поле ввода
    )
    return keyboard
def get_ref_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐕Расписание"), KeyboardButton(text="🐾Взять день"), KeyboardButton(text="🕵️‍♂️Попросить")],
            [KeyboardButton(text="📊Статистика"), KeyboardButton(text="🤖Освежить"), KeyboardButton(text="🚫Отменить выбор")] ],
        resize_keyboard=True,  # Подгоняет размер кнопок
        input_field_placeholder="Чего изволите?"  # Подсказка в поле ввода
    )
    return keyboard
def personkeyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="СП - суперпапаша"), KeyboardButton(text="КН - крутой Никита")],
            [KeyboardButton(text="КА - красавчик Андрей"),KeyboardButton(text="ММ - малышка мама")],
            [KeyboardButton(text="Назад")]  ],
        resize_keyboard=True,  # Подгоняет размер кнопок
        input_field_placeholder="Выбери кто погуляет..."  # Подсказка в поле ввода
    )
    return keyboard
def daykeyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Пн"), KeyboardButton(text="Вт"),KeyboardButton(text="Ср"), KeyboardButton(text="Чт")],
            [KeyboardButton(text="Пт"),KeyboardButton(text="Сб"),KeyboardButton(text="Вс"), KeyboardButton(text="Назад")] ],
        resize_keyboard=True,  # Подгоняет размер кнопок
        input_field_placeholder="Выбери день..."  # Подсказка в поле ввода
    )
    return keyboard
def timekb():
    inline_kb_list = [
        [InlineKeyboardButton(text="☀️утро", callback_data="morning"),
        InlineKeyboardButton(text="🌆вечер", callback_data="evening")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ]
    return InlineKeyboardMarkup(row_width=2, inline_keyboard=inline_kb_list)

def timetable_inlinekb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Эта неделя", callback_data="week0"),
        InlineKeyboardButton(text="Следующая", callback_data="week1")],
        [InlineKeyboardButton(text="Покажи легенду 📜", callback_data="legend")]
    ]
    return InlineKeyboardMarkup(row_width=2, inline_keyboard=inline_kb_list) 

# -------------------------------------- callback handler -----------------------------------------------------
@dp.callback_query(F.data == "back", StateFilter(play.choisetime))
async def morning_pressed(callback: types.CallbackQuery, state: FSMContext):
    #await callback.message.answer("Отличный выбор, "+user_data['name']+"!", reply_markup=get_keyboard())
    await state.set_state(play.choisedate)    
    await callback.answer()
    await callback.message.answer("Выбирай день⬇️", reply_markup=daykeyboard())
    
@dp.callback_query(F.data == "morning", StateFilter(play.choisetime))
async def morning_pressed(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Утречком отлично гуляется!")
    await state.update_data(tt = 0) # tt=0 <=> утро, 1 - вечер.
    user_data = await state.get_data()
    cdt = user_data['dt']
    #print("tt=",user_data['tt'])
    print(user_data['wdn'], user_data['wd'], user_data['week'])
    #print(user_data['morn_week0'])
    #print("проверяем ", user_data['morn_week0'][user_data['wdn']-1])
    if (user_data['week'] == 0):
        if user_data['tt'] == 0:
            if user_data['morn_week0'][user_data['wdn']-1] == "ПУ":
                 # the slot is empty.
                print("w0, the slot is empty")
                pict_path = user_data['pict_path'] +"eek"+str(user_data['week'])+".jpg"
                new_img = Image.open(pict_path)
                font = ImageFont.truetype("arial.ttf", 14)
                pencil = ImageDraw.Draw(new_img)
                wdn = int(user_data['wdn']) # weekday number from 1 to 7.
                r = user_data['red']
                g = user_data['green']
                b = user_data['blue']
                pencil.rectangle([40+(wdn-1)*32, 14+user_data['tt']*32, 65+(wdn-1)*32, 39+user_data['tt']*32],fill = (r, g, b, 0), outline = 'black', width = 1)
                pencil.text((40+3+(wdn-1)*32, 18),user_data['sname'], font=font, fill='black')
                new_img.save(pict_path)
                await callback.message.answer("Отличный выбор, "+user_data['name']+"!", reply_markup=get_ref_keyboard())
                await state.set_state(default_state)
                await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
                #---Let's update file wcalendar.txt
                put_into(user_data['pict_path']+"utf8calendar.txt",cdt,0,user_data['sname'])
                #Let's update the timetable loaded.
                ev = user_data['morn_week0']
                ev[user_data['wdn']-1] = user_data['sname']
                await state.update_data(morn_week0 = ev)
                await callback.answer()
            else:
                #print("smbd has already taken this timeslot")
                if user_data['morn_week0'][user_data['wdn']-1] == user_data['sname'].upper():
                    await state.set_state(play.choisedate)
                    await callback.message.answer("Это время уже и так твоё, "+user_data['name']+". Возьмёшь ещё?", reply_markup=daykeyboard())
                else:
                    #Time to negotiate.
                    await state.set_state(play.choisedate)
                    await callback.message.answer("Это время успел занять "+user_data['morn_week0'][user_data['wdn']-1]+". Выберешь другое?", reply_markup=daykeyboard())
        else:
            if user_data['even_week0'][user_data['wdn']-1] == "ПУ":
                # the slot is empty.
                print("the slot is empty")
                pict_path = user_data['pict_path'] +"eek"+str(user_data['week'])+".jpg"
                new_img = Image.open(pict_path)
                font = ImageFont.truetype("arial.ttf", 14)
                pencil = ImageDraw.Draw(new_img)
                wdn = int(user_data['wdn']) # weekday number from 1 to 7.
                r = user_data['red']
                g = user_data['green']
                b = user_data['blue']
                pencil.rectangle([40+(wdn-1)*32, 14+user_data['tt']*32, 65+(wdn-1)*32, 39+user_data['tt']*32],fill = (r, g, b, 0), outline = 'black', width = 1)
                pencil.text((40+3+(wdn-1)*32, 18+user_data['tt']*32),user_data['sname'], font=font, fill='black')
                new_img.save(pict_path)
                await callback.message.answer("Отличный выбор, "+user_data['name']+"!", reply_markup=get_ref_keyboard())
                await state.set_state(default_state)
                await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
                #---Let's update file wcalendar.txt
                put_into(user_data['pict_path']+"utf8calendar.txt",cdt,1,user_data['sname'])
                #Let's update the timetable loaded.
                ev = user_data['even_week0']
                ev[user_data['wdn']-1] = user_data['sname']
                await state.update_data(even_week0 = ev)
                await callback.answer()
            else:
                #print("smbd has already taken this timeslot")
                if user_data['even_week0'][user_data['wdn']-1] == user_data['sname'].upper():
                    await callback.message.answer("Это время уже и так твоё, "+user_data['name']+". Возьмёшь ещё?", reply_markup=daykeyboard())
                    await callback.answer()
                else:
                    #Time to negotiate.
                    await callback.message.answer("Это время успел занять "+user_data['even_week0'][user_data['wdn']-1]+". Выберешь другое?", reply_markup=daykeyboard())
    if (user_data['week'] == 1):
        if user_data['tt'] == 0:
            if user_data['morn_week1'][user_data['wdn']-1] == "ПУ":
                 # the slot is empty.
                print("w1, the slot is empty")
                pict_path = user_data['pict_path'] +"eek"+str(user_data['week'])+".jpg"
                new_img = Image.open(pict_path)
                font = ImageFont.truetype("arial.ttf", 14)
                pencil = ImageDraw.Draw(new_img)
                wdn = int(user_data['wdn']) # weekday number from 1 to 7.
                r = user_data['red']
                g = user_data['green']
                b = user_data['blue']
                pencil.rectangle([40+(wdn-1)*32, 14+user_data['tt']*32, 65+(wdn-1)*32, 39+user_data['tt']*32],fill = (r, g, b, 0), outline = 'black', width = 1)
                pencil.text((40+3+(wdn-1)*32, 18),user_data['sname'], font=font, fill='black')
                new_img.save(pict_path)
                await callback.message.answer("Отличный выбор, "+user_data['name']+"!", reply_markup=get_ref_keyboard())
                await state.set_state(default_state)
                await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
                #---Let's update file wcalendar.txt
                put_into(user_data['pict_path']+"utf8calendar.txt",cdt,0,user_data['sname'])
                #Let's update the timetable loaded.
                ev = user_data['morn_week1']
                ev[user_data['wdn']-1] = user_data['sname']
                await state.update_data(morn_week1 = ev)
                await callback.answer()
            else:
                #print("smbd has already taken this timeslot")
                if user_data['morn_week1'][user_data['wdn']-1] == user_data['sname'].upper():
                    await state.set_state(play.choisedate)
                    await callback.message.answer("Это время уже и так твоё, "+user_data['name']+". Возьмёшь ещё?", reply_markup=daykeyboard())
                else:
                    #Time to negotiate.
                    await state.set_state(play.choisedate)
                    await callback.message.answer("Это время успел занять "+user_data['morn_week1'][user_data['wdn']-1]+". Выберешь другое?", reply_markup=daykeyboard())
        else:
            if user_data['even_week1'][user_data['wdn']-1] == "ПУ":
                # the slot is empty.
                print("the slot is empty")
                pict_path = user_data['pict_path'] +"eek"+str(user_data['week'])+".jpg"
                new_img = Image.open(pict_path)
                font = ImageFont.truetype("arial.ttf", 14)
                pencil = ImageDraw.Draw(new_img)
                wdn = int(user_data['wdn']) # weekday number from 1 to 7.
                r = user_data['red']
                g = user_data['green']
                b = user_data['blue']
                pencil.rectangle([40+(wdn-1)*32, 14+user_data['tt']*32, 65+(wdn-1)*32, 39+user_data['tt']*32],fill = (r, g, b, 0), outline = 'black', width = 1)
                pencil.text((40+3+(wdn-1)*32, 18+user_data['tt']*32),user_data['sname'], font=font, fill='black')
                new_img.save(pict_path)
                await callback.message.answer("Отличный выбор, "+user_data['name']+"!", reply_markup=get_ref_keyboard())
                await state.set_state(default_state)
                await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
                #---Let's update file wcalendar.txt
                put_into(user_data['pict_path']+"utf8calendar.txt",cdt,1,user_data['sname'])
                #Let's update the timetable loaded.
                ev = user_data['even_week1']
                ev[user_data['wdn']-1] = user_data['sname']
                await state.update_data(even_week1 = ev)
                await callback.answer()
            else:
                #print("smbd has already taken this timeslot")
                if user_data['even_week1'][user_data['wdn']-1] == user_data['sname'].upper():
                    await callback.message.answer("Это время уже и так твоё, "+user_data['name']+". Возьмёшь ещё?", reply_markup=daykeyboard())
                    await callback.answer()
                else:
                    #Time to negotiate.
                    await callback.message.answer("Это время успел занять "+user_data['even_week1'][user_data['wdn']-1]+". Выберешь другое?", reply_markup=daykeyboard())  
    await callback.answer() # чтобы подтвердить ответ, техническая штука

@dp.callback_query(F.data == "evening", StateFilter(play.choisetime))
async def morning_pressed(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(tt = 1) # tt=0 <=> утро, 1 - вечер.
    user_data = await state.get_data()
    cdt = user_data['dt']
    print("dt=",user_data['dt'])
    #print(user_data['wdn'], user_data['wd'], user_data['week'])
    #print(user_data['even_week0'])
    #print("проверяем ", user_data['morn_week0'][user_data['wdn']-1])
    if (user_data['week'] == 0):
        if user_data['tt'] == 0:
            if user_data['morn_week0'][user_data['wdn']-1] == "ПУ":
                 # the slot is empty.
                print("the slot is empty")
                pict_path = user_data['pict_path'] +"eek"+str(user_data['week'])+".jpg"
                new_img = Image.open(pict_path)
                font = ImageFont.truetype("arial.ttf", 14)
                pencil = ImageDraw.Draw(new_img)
                wdn = int(user_data['wdn']) # weekday number from 1 to 7.
                r = user_data['red']
                g = user_data['green']
                b = user_data['blue']
                pencil.rectangle([40+(wdn-1)*32, 14+user_data['tt']*32, 65+(wdn-1)*32, 39+user_data['tt']*32],fill = (r, g, b, 0), outline = 'black', width = 1)
                pencil.text((40+3+(wdn-1)*32, 18),user_data['sname'], font=font, fill='black')
                new_img.save(pict_path)
                await callback.message.answer("Отличный выбор, "+user_data['name']+"!", reply_markup=get_ref_keyboard())
                await state.set_state(default_state)
                await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
                #---Let's update file wcalendar.txt
                put_into(user_data['pict_path']+"utf8calendar.txt",cdt,0,user_data['sname'])
                #Let's update the timetable loaded.
                ev = user_data['morn_week0']
                ev[user_data['wdn']-1] = user_data['sname']
                await state.update_data(morn_week0 = ev)
                await callback.answer()
            else:
                #print("smbd has already taken this timeslot")
                if user_data['morn_week0'][user_data['wdn']-1] == user_data['sname'].upper():
                    await callback.message.answer("Это время уже и так твоё, "+user_data['name']+". Возьмёшь ещё?", reply_markup=daykeyboard())
                    await state.set_state(play.choisedate)
                    await callback.answer()
                else:
                    #Time to negotiate.
                    await state.set_state(play.choisedate)
                    await callback.message.answer("Это время успел занять "+user_data['morn_week0'][user_data['wdn']-1]+". Выберешь другое?", reply_markup=daykeyboard())
                    await callback.answer()
        else:
            if user_data['even_week0'][user_data['wdn']-1] == "ПУ":
                # the slot is empty.
                print("the slot is empty")
                pict_path = user_data['pict_path'] +"eek"+str(user_data['week'])+".jpg"
                new_img = Image.open(pict_path)
                font = ImageFont.truetype("arial.ttf", 14)
                pencil = ImageDraw.Draw(new_img)
                wdn = int(user_data['wdn']) # weekday number from 1 to 7.
                r = user_data['red']
                g = user_data['green']
                b = user_data['blue']
                pencil.rectangle([40+(wdn-1)*32, 14+user_data['tt']*32, 65+(wdn-1)*32, 39+user_data['tt']*32],fill = (r, g, b, 0), outline = 'black', width = 1)
                pencil.text((40+3+(wdn-1)*32, 18+user_data['tt']*32),user_data['sname'], font=font, fill='black')
                new_img.save(pict_path)
                await callback.message.answer("Отличный выбор, "+user_data['name']+"!", reply_markup=get_ref_keyboard())
                #Let's update the timetable loaded.
                ev = user_data['even_week0']
                ev[user_data['wdn']-1] = user_data['sname']
                await state.update_data(even_week0 = ev)
                
                await state.set_state(default_state)
                await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))  #---Let's update file wcalendar.txt
                put_into(user_data['pict_path']+"utf8calendar.txt",cdt,1,user_data['sname'])
                await callback.answer() # чтобы подтвердить ответ, техническая штука
            else:
                #print("smbd has already taken this timeslot")
                if user_data['even_week0'][user_data['wdn']-1] == user_data['sname'].upper():
                    await callback.message.answer("Это время уже и так твоё, "+user_data['name']+". Возьмёшь ещё?", reply_markup=daykeyboard())
                    await state.set_state(play.choisedate)
                    await callback.answer() # чтобы подтвердить ответ, техническая штука
                else:
                    #Time to negotiate.
                    await callback.message.answer("Это время успел занять "+user_data['even_week0'][user_data['wdn']-1]+". Выберешь другое?", reply_markup=daykeyboard())
                    await state.set_state(play.choisedate)
                    await callback.answer() # чтобы подтвердить ответ, техническая штука
    if (user_data['week'] == 1):
        if user_data['tt'] == 0:
            if user_data['morn_week1'][user_data['wdn']-1] == "ПУ":
                 # the slot is empty.
                print("the slot is empty")
                pict_path = user_data['pict_path'] +"eek"+str(user_data['week'])+".jpg"
                new_img = Image.open(pict_path)
                font = ImageFont.truetype("arial.ttf", 14)
                pencil = ImageDraw.Draw(new_img)
                wdn = int(user_data['wdn']) # weekday number from 1 to 7.
                r = user_data['red']
                g = user_data['green']
                b = user_data['blue']
                pencil.rectangle([40+(wdn-1)*32, 14+user_data['tt']*32, 65+(wdn-1)*32, 39+user_data['tt']*32],fill = (r, g, b, 0), outline = 'black', width = 1)
                pencil.text((40+3+(wdn-1)*32, 18),user_data['sname'], font=font, fill='black')
                new_img.save(pict_path)
                await callback.message.answer("Отличный выбор, "+user_data['name']+"!", reply_markup=get_ref_keyboard())
                await state.set_state(default_state)
                await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
                #---Let's update file wcalendar.txt
                put_into(user_data['pict_path']+"utf8calendar.txt",cdt,0,user_data['sname'])
                #Let's update the timetable loaded.
                ev = user_data['morn_week1']
                ev[user_data['wdn']-1] = user_data['sname']
                await state.update_data(morn_week1 = ev)
                await callback.answer()
            else:
                #print("smbd has already taken this timeslot")
                if user_data['morn_week1'][user_data['wdn']-1] == user_data['sname'].upper():
                    await callback.message.answer("Это время уже и так твоё, "+user_data['name']+". Возьмёшь ещё?", reply_markup=daykeyboard())
                    await state.set_state(play.choisedate)
                    await callback.answer()
                else:
                    #Time to negotiate.
                    await state.set_state(play.choisedate)
                    await callback.message.answer("Это время успел занять "+user_data['morn_week1'][user_data['wdn']-1]+". Выберешь другое?", reply_markup=daykeyboard())
                    await callback.answer()
        else:
            if user_data['even_week1'][user_data['wdn']-1] == "ПУ":
                # the slot is empty.
                print("the slot is empty")
                pict_path = user_data['pict_path'] +"eek"+str(user_data['week'])+".jpg"
                new_img = Image.open(pict_path)
                font = ImageFont.truetype("arial.ttf", 14)
                pencil = ImageDraw.Draw(new_img)
                wdn = int(user_data['wdn']) # weekday number from 1 to 7.
                r = user_data['red']
                g = user_data['green']
                b = user_data['blue']
                pencil.rectangle([40+(wdn-1)*32, 14+user_data['tt']*32, 65+(wdn-1)*32, 39+user_data['tt']*32],fill = (r, g, b, 0), outline = 'black', width = 1)
                pencil.text((40+3+(wdn-1)*32, 18+user_data['tt']*32),user_data['sname'], font=font, fill='black')
                new_img.save(pict_path)
                await callback.message.answer("Отличный выбор, "+user_data['name']+"!", reply_markup=get_ref_keyboard())
                #Let's update the timetable loaded.
                ev = user_data['even_week1']
                ev[user_data['wdn']-1] = user_data['sname']
                await state.update_data(even_week1 = ev)
                
                await state.set_state(default_state)
                await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))  #---Let's update file wcalendar.txt
                put_into(user_data['pict_path']+"utf8calendar.txt",cdt,1,user_data['sname'])
                await callback.answer() # чтобы подтвердить ответ, техническая штука
            else:
                #print("smbd has already taken this timeslot")
                if user_data['even_week1'][user_data['wdn']-1] == user_data['sname'].upper():
                    await callback.message.answer("Это время уже и так твоё, "+user_data['name']+". Возьмёшь ещё?", reply_markup=daykeyboard())
                    await state.set_state(play.choisedate)
                    await callback.answer() # чтобы подтвердить ответ, техническая штука
                else:
                    #Time to negotiate.
                    await callback.message.answer("Это время успел занять "+user_data['even_week1'][user_data['wdn']-1]+". Выберешь другое?", reply_markup=daykeyboard())
                    await state.set_state(play.choisedate)
                    await callback.answer() # чтобы подтвердить ответ, техническая штука
    await callback.answer() # чтобы подтвердить ответ, техническая штука
@dp.callback_query(F.data == "legend")
async def morning_pressed(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    pict_path = user_data['pict_path']
    await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path+"egend_K.png"))
    await callback.answer() # чтобы подтвердить ответ, техническая штука

@dp.callback_query(F.data == "week0")
async def morning_pressed(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    pict_path = user_data['pict_path']
    await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path+"eek0.jpg"))
    await callback.answer() # чтобы подтвердить ответ, техническая штука
@dp.callback_query(F.data == "week1")
async def morning_pressed(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    pict_path = user_data['pict_path']
    await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path+"eek1.jpg"))
    await callback.answer() # чтобы подтвердить ответ, техническая штука
# ------------------------------------------------------------------------------------------------------------------------------------------
# Обработчик команды /send_alerts-----------------------------------------------------------------------------------------------------------
@dp.message(Command("send_alert"))
async def send_alerts(message: types.Message, state: FSMContext):
    td = datetime.date.today()
    wd = td.weekday() + 1 # день недели, пн = 1.
    fl = True
    user_data = await state.get_data()
    #cht_id = 120443225 # this is my chat.
    cht_id = user_data['famcht_id'] # this is our family chat.
    mr = user_data['morn_week0']
    ev = user_data['even_week0']
    ltr = ""
    if wd != 7:
        if mr[wd-1] == "ПУ":
            ltr = "Утром никто не погуляет с собаком?😳\nНе надо так. Погуляйте и запишитесь, пожалуйста😊\n"
        if mr[wd] == "ПУ":
            ltr = ltr + "Завтра утром никто не погуляет с собаком?😳\nНе надо так. Запишитесь, пожалуйста😊\n И, конечно, погуляйте!\n"
        if ev[wd-1] == "ПУ":
            ltr = ltr + "Вечером никто не погуляет с собаком?😳\nНе надо так. Погуляйте и запишитесь, пожалуйста😊\n"
    else:
        if user_data['even_week0'][6] == "ПУ":
            ltr = ltr + "Ой, вечером никто не погуляет с этим псом?😳\n Погуляйте и запишитесь, пожалуйста😊\n"
        # Let's check monday of the next week.
        if user_data['morn_week1'][0] == "ПУ":
            ltr = "Завтра утром никто не погуляет с собаком?😳\nНе надо так. Погуляйте и запишитесь, пожалуйста😊\n"
        if user_data['even_week1'][0] == "ПУ":
            ltr = ltr + "Завтра вечером никто не погуляет с собаком?😳\nНе надо так. Погуляйте и запишитесь, пожалуйста😊\n"
    print(cht_id, "\n"+ltr)
    #await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
    await bot.send_message(chat_id=cht_id, text=ltr)
    #print("send alerts")

@dp.message(Command("send_warning"))
async def send_warn(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    cht_id = 120443225 # this is my chat.
    if message.from_user.id == 120443225: # this is Ilya.
        cht_id = user_data['famcht_id'] # this is our family chat.
        #await bot.send_message(chat_id=cht_id, text="Раздел статистики готов. Пользуйстесь😊")
        #await bot.send_message(chat_id=cht_id, text="Я обновился!\nТеперь есть кнопка 'обновить' - можно нажимать её вместо команды 'start'. Пользуйстесь😊\nА ещё я буду уведомлять когда кто-нибудь освободит время прогулки.")
        #print("gg")
        #await bot.send_message(chat_id=cht_id, text="Я обновился!\nТеперь я могу попросить погулять с пёсом кого скажете! Пользуйтесь\nА ещё произошла масштабная миграция - я переехал в облако. Будет надёжнее и быстрее.\nА ещё появилась команда \help - описание основного функционала. Совершенству нет предела😊\nStay tuned!")
    else:
        cht_id = user_data['cht_id'] # this is this chat.
        await bot.send_message(chat_id=cht_id, text="Последняя обнова была такая⬇️ Все в курсе, не будем спамить.\nТеперь я могу попросить погулять с пёсом кого скажете! Пользуйтесь\nА ещё произошла масштабная миграция - я переехал в облако. Будет надёжнее и быстрее.\nА ещё появилась команда \help - описание основного функционала. Совершенству нет предела😊\nStay tuned!")
    #print("send alerts")

# Обработчик команды /start ----------------------------------------------------------------------------------------------------------------
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    uname = message.from_user.id
    print(message.chat.id)
    #await state.update_data(pict_path = r'C:\Users\ilya_\Desktop\doggysbot\w')
    await state.update_data(pict_path = r'w')
    await state.update_data(cht_id = message.chat.id)
    await state.update_data(famcht_id = "-1001541827100") 
    await state.update_data(dates_week0 = []) # даты текущей недели.
    await state.update_data(dates_week1 = []) # даты следующей недели.
    await state.update_data(morn_week0 = []) # утры текущей недели - кто гуляет.
    await state.update_data(morn_week1 = []) # утры следующей недели - кто гуляет.
    await state.update_data(even_week0 = []) # вечера текущей недели - кто гуляет.
    await state.update_data(even_week1 = []) # вечера следующей недели - кто гуляет.
    await state.update_data(days_week0 = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]) # дни текущей недели.
    await state.update_data(days_week1 = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]) # дни следующей недели.
    user_data = await state.get_data()
    dts = [] 
    mr = []
    ev = []
    td = datetime.date.today()
    wd = td.weekday() + 1 # день недели, пн = 1.
    monday = td - datetime.timedelta(days = wd - 1) # date of this week's monday.
    user_data = await state.get_data()
     # Let's fill the calendar from the file. 
    #fname = user_data['pict_path']+"calendar.txt"
    fname = user_data['pict_path']+"utf8calendar.txt"
    print(fname)
    #fin = open(fname,"r", encoding="ANSI")
    fin = open(fname,"r", encoding="utf-8")
    for k in range(7):
        fl = True
        cdt = monday + datetime.timedelta(days = k) # current date to look for in the file.
        print(cdt)
        while fl:
            strng = fin.readline()
            if strng != "":
                spl = strng.split() # w[0] is date, w[1] is morning, w[2] is evening.
                print(spl)
                if datetime.date(int(spl[0].split('-')[0]),int(spl[0].split('-')[1]),int(spl[0].split('-')[2])) == cdt:   
                    fl = False                
            else:
                fl = False #EOF is reached.
        if strng == "":
            # there is no searched date in the file :-(
            dts.append(str(cdt.year)+"-"+str(cdt.month)+"-"+str(cdt.day))
            mr.append("ПУ")
            ev.append("ПУ")
            print(dts)
        else:
            dts.append(spl[0])
            mr.append(spl[1])
            ev.append(spl[2])
            print(dts)
        fin.seek(0) # rewind the file.
    fin.close()
    await state.update_data(dates_week0 = dts)
    await state.update_data(morn_week0 = mr)
    await state.update_data(even_week0 = ev)
    
    print("week0 is done")
    print(dts)
    print(mr)
    print(ev)
    #Let's draw the timetable of week0.
    Draw_timetable(user_data['pict_path'], dts, mr, ev, 0)
    print("Going to fill week1")
    # Let's fill the next week = week1.
    tmpdate = datetime.date(int(dts[6].split('-')[0]),int(dts[6].split('-')[1]),int(dts[6].split('-')[2]))
    dts1 = [] 
    mr = []
    ev = [] 
    tmpdate = tmpdate + datetime.timedelta(days = 1)
    print("начало ",tmpdate)
    #dts.append(tmpdate.strftime("%Y-%m-%d"))
    dts1.append(tmpdate)
    mr.append("ПУ")
    ev.append("ПУ")
    print(dts1)
    for k in range(6):
        tmpdate = dts1[k] + datetime.timedelta(days = 1)
        dts1.append(tmpdate)
        mr.append("ПУ")
        ev.append("ПУ")
    print(dts1)
    fin = open(fname,"r", encoding="utf-8")
    fl = True
    while fl:
        #let's find dts[k] in the file.
        strng = fin.readline()
        if strng != "":
            spl = strng.split() # w[0] is date, w[1] is morning, w[2] is evening.
            #print(spl[0].split('-')[0])
            tmpdate = datetime.date(int(spl[0].split('-')[0]),int(spl[0].split('-')[1]),int(spl[0].split('-')[2]))
            print(tmpdate)
            for k in range(7):   
                if dts1[k] == tmpdate:
                    mr[k] = spl[1]
                    ev[k] = spl[2]                
        else:
            fl = False #EOF is reached. dts[k] is not found.
    fin.close()
    dts = []
    for k in range(7):
        dts.append(dts1[k].strftime("%Y-%m-%d"))
    
    await state.update_data(dates_week1 = dts)
    await state.update_data(morn_week1 = mr)
    await state.update_data(even_week1 = ev)
    #Let's draw the timetable of week1.
    #print(dts)
    #print(mr)
    #print(ev)
    Draw_timetable(user_data['pict_path'], dts, mr, ev, 1)

    user_data = await state.get_data()
    #print(uname)
    if message.from_user.id == 120443225:
        await state.update_data(sname = 'СП')
        await state.update_data(name = 'Илья')
        await state.update_data(red = 153)
        await state.update_data(green = 204)
        await state.update_data(blue = 255)
        #user_data = await state.get_data()
    if message.from_user.id == 109036609:
        await state.update_data(sname = 'ММ')
        await state.update_data(name = 'Оля')
        await state.update_data(red = 255)
        await state.update_data(green = 153)
        await state.update_data(blue = 204)
        #user_data = await state.get_data()
    if message.from_user.id == 5183551400: 
        await state.update_data(sname = 'КА')
        await state.update_data(name = 'Андрей')
        await state.update_data(red = 191)
        await state.update_data(green = 191)
        await state.update_data(blue = 191)
        #user_data = await state.get_data()
    if message.from_user.id == 894032901:
        await state.update_data(sname = 'КН')
        await state.update_data(name = 'Никита')
        await state.update_data(red = 255)
        await state.update_data(green = 153)
        await state.update_data(blue = 51)
        #user_data = await state.get_data()
    user_data = await state.get_data()
    await message.answer("Привет, "+user_data['name']+"!", reply_markup=get_ref_keyboard())
    await message.answer("Этот бот поможет нам организоваться для прогулки с собачеком. Не оставим пса негулянным!", reply_markup=get_ref_keyboard())

@dp.message(Command('help'))
async def help_command(message: Message): 
    #await message.reply("Команды бота:\n/start - Начать работу\n/help - Получить помощь")
    await message.answer("Что умеет этот бот? Он хранит информацию о том, кто и когда гуляет с собакой корги. Подробнее:\nРасписание - посмотреть кто и когда гуляет\nВзять день - записаться на прогулку\nПопросить - попросить кого-то погулять с псом\nСтатистика - посмотреть кто сколько гулял\nОсвежить - обновить информацию в боте\nОтменить выбор - отказаться от выбранной ранее прогулки")

# Обработчик текстовых сообщений
@dp.message(F.text =="🤖Освежить")
async def echo_message(message: types.Message, state: FSMContext):
    #await state.update_data(pict_path = r'C:\Users\ilya_\Desktop\doggysbot\w')
    await state.update_data(pict_path = r'w')
    await state.update_data(cht_id = message.chat.id)
    await state.update_data(famcht_id = "-1001541827100") 
    user_data = await state.get_data()
    await state.update_data(dates_week0 = []) # даты текущей недели.
    await state.update_data(dates_week1 = []) # даты следующей недели.
    await state.update_data(morn_week0 = []) # утры текущей недели - кто гуляет.
    await state.update_data(morn_week1 = []) # утры следующей недели - кто гуляет.
    await state.update_data(even_week0 = []) # вечера текущей недели - кто гуляет.
    await state.update_data(even_week1 = []) # вечера следующей недели - кто гуляет.
    await state.update_data(days_week0 = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]) # дни текущей недели.
    await state.update_data(days_week1 = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]) # дни следующей недели.
    
    dts = [] 
    mr = []
    ev = []
    td = datetime.date.today()
    wd = td.weekday() + 1 # день недели, пн = 1.
    monday = td - datetime.timedelta(days = wd - 1) # date of this week's monday.
    user_data = await state.get_data()
     # Let's fill the calendar from the file.
    fname = user_data['pict_path']+"utf8calendar.txt"
    fin = open(fname,"r", encoding="utf-8")
    for k in range(7):
        fl = True
        cdt = monday + datetime.timedelta(days = k) # current date to look for in the file.
        print(cdt)
        while fl:
            strng = fin.readline()
            if strng != "":
                spl = strng.split() # w[0] is date, w[1] is morning, w[2] is evening.
                print(spl)
                if datetime.date(int(spl[0].split('-')[0]),int(spl[0].split('-')[1]),int(spl[0].split('-')[2])) == cdt:   
                    fl = False                
            else:
                fl = False #EOF is reached.
        if strng == "":
            # there is no searched date in the file :-(
            dts.append(str(cdt.year)+"-"+str(cdt.month)+"-"+str(cdt.day))
            mr.append("ПУ")
            ev.append("ПУ")
            print(dts)
        else:
            dts.append(spl[0])
            mr.append(spl[1])
            ev.append(spl[2])
            print(dts)
        fin.seek(0) # rewind the file.
    fin.close()
    await state.update_data(dates_week0 = dts)
    await state.update_data(morn_week0 = mr)
    await state.update_data(even_week0 = ev)
    print("week0 refreshed")
    #print(dts)
    #print(mr)
    #print(ev)
    #Let's draw the timetable of week0.
    Draw_timetable(user_data['pict_path'], dts, mr, ev, 0)
    print("Going to refresh week1")
    # Let's fill the next week = week1.
    tmpdate = datetime.date(int(dts[6].split('-')[0]),int(dts[6].split('-')[1]),int(dts[6].split('-')[2]))
    dts1 = [] 
    mr = []
    ev = [] 
    tmpdate = tmpdate + datetime.timedelta(days = 1)
    #print("начало ",tmpdate)
    #dts.append(tmpdate.strftime("%Y-%m-%d"))
    dts1.append(tmpdate)
    mr.append("ПУ")
    ev.append("ПУ")
    print(dts1)
    for k in range(6):
        tmpdate = dts1[k] + datetime.timedelta(days = 1)
        dts1.append(tmpdate)
        mr.append("ПУ")
        ev.append("ПУ")
    print(dts1)
    fin = open(fname,"r", encoding="utf-8")
    fl = True
    while fl:
        #let's find dts[k] in the file.
        strng = fin.readline()
        if strng != "":
            spl = strng.split() # w[0] is date, w[1] is morning, w[2] is evening.
            #print(spl[0].split('-')[0])
            tmpdate = datetime.date(int(spl[0].split('-')[0]),int(spl[0].split('-')[1]),int(spl[0].split('-')[2]))
            print(tmpdate)
            for k in range(7):   
                if dts1[k] == tmpdate:
                    mr[k] = spl[1]
                    ev[k] = spl[2]                
        else:
            fl = False #EOF is reached. dts[k] is not found.
    fin.close()
    dts = []
    for k in range(7):
        dts.append(dts1[k].strftime("%Y-%m-%d"))
    await state.update_data(dates_week1 = dts)
    await state.update_data(morn_week1 = mr)
    await state.update_data(even_week1 = ev)
    #Let's draw the timetable of week1.
    Draw_timetable(user_data['pict_path'], dts, mr, ev, 1)
    # Let's pick the active user.
    if message.from_user.id == 120443225:
        await state.update_data(sname = 'СП')
        await state.update_data(name = 'Илья')
        await state.update_data(red = 153)
        await state.update_data(green = 204)
        await state.update_data(blue = 255)
    if message.from_user.id == 109036609:
        await state.update_data(sname = 'ММ')
        await state.update_data(name = 'Оля')
        await state.update_data(red = 255)
        await state.update_data(green = 153)
        await state.update_data(blue = 204)
    if message.from_user.id == 5183551400: 
        await state.update_data(sname = 'КА')
        await state.update_data(name = 'Андрей')
        await state.update_data(red = 191)
        await state.update_data(green = 191)
        await state.update_data(blue = 191)
    if message.from_user.id == 894032901:
        await state.update_data(sname = 'КН')
        await state.update_data(name = 'Никита')
        await state.update_data(red = 255)
        await state.update_data(green = 153)
        await state.update_data(blue = 51)
    pict_path = user_data['pict_path'] 
    await message.answer(f"Обновились! Что желаете?", reply_markup=get_ref_keyboard())

@dp.message(F.text =="🐕Расписание")
async def echo_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    pict_path = user_data['pict_path'] 
    await message.answer(f"Какое расписание показать?", reply_markup=timetable_inlinekb())
    #await bot.send_photo(chat_id=message.chat.id, photo=types.FSInputFile(pict_path+"eek0.jpg"))
    #await bot.send_photo(chat_id=message.chat.id, photo=types.FSInputFile(pict_path+"egend_K.png"))
    #await message.answer(f"Осталось выбрать время", reply_markup=timekb()) 

@dp.message(F.text =="🐾Взять день")
async def echo_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await state.set_state(play.choisedate)
    #print(await state.get_data())
    await message.answer(f"Отлично, выбирай любой день!\nВведи день недели. Я понимаю такое:\nпн, вт, ср, чт, пт, сб, вс", reply_markup=daykeyboard())
    #await bot.send_photo(chat_id=message.chat.id, photo=types.FSInputFile("matrix_rus.jpg"))

@dp.message(F.text =="🕵️‍♂️Попросить")
async def echo_message(message: types.Message, state: FSMContext):
    #user_data = await state.get_data()
    await state.set_state(play.choiseperson)
    #print(await state.get_data())
    await message.answer(f"Кого ты хочешь попросить погулять?", reply_markup=personkeyboard())
    #await bot.send_photo(chat_id=message.chat.id, photo=types.FSInputFile("matrix_rus.jpg"))

@dp.message(F.text =="📊Статистика")
async def echo_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    fname = user_data['pict_path'] +"utf8calendar.txt"
    stat = [[0,0,0,0],[0,0,0,0]] #number of doggy walks. СП, ММ, КА, КН.
    #stat[1] = [0,0,0,0] #number of evening doggy walks. СП, ММ, КА, КН.
    #print("Let's dive into get_stat")
    stat = get_stats(fname)
    #print("stat1=",stat)
    fname = user_data['pict_path'] + "stat.jpg"
    new_img = Image.open(fname)
    font = ImageFont.truetype("arial.ttf", 14)
    pencil = ImageDraw.Draw(new_img)
    #print("ready to draw, fname =",fname)   
    for i in range(4):
        #pencil.rectangle([40+i*32, 14+0*32, 65+i*32, 39+0*32],fill = (r, g, b, 0), outline = 'black', width = 1)
        k = stat[0][i]
        m = stat[1][i]
        print("k=",k," m=",m)
        pencil.rectangle([169, 25+i*32, 219, 45+i*32],fill = (255, 255, 255, 0), outline = 'white', width = 1)
        pencil.text(xy=(169+20, 30+i*32.5), text=str(k)  , font=font, fill='black')
        pencil.rectangle([223, 25+i*32, 273, 45+i*32],fill = (255, 255, 255, 0), outline = 'white', width = 1)
        pencil.text(xy=(223+20, 30+i*32.5), text=str(m)  , font=font, fill='black')
        pencil.rectangle([281, 25+i*32, 330, 45+i*32],fill = (255, 255, 255, 0), outline = 'white', width = 1)
        pencil.text(xy=(281+20, 30+i*32.5), text=str(k+m)  , font=font, fill='black')
    new_img.save(fname)
    #print('saved')
    await message.answer(f"статистика с 08.12.2025 по сегодня:")
    await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(fname))
    
@dp.message(F.text =="🚫Отменить выбор")
async def echo_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await state.set_state(play.cancel)
    await message.answer(
        f"😢 Какая прогулка не состоится?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Эта неделя"),   KeyboardButton(text="Следующая"),],
                [KeyboardButton(text="Назад")]
            ], resize_keyboard=True,
        ),
    )
@dp.message(F.text, StateFilter(play.cancel))
# идёт отмена выбранной даты погулять.
async def echo_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    pos_mor_canc = [] # possible morning cancelations.
    pos_eve_canc = [] # possible evening cancelations.
    td = datetime.date.today()
    #print("today is ",td)
    mrw0 = user_data['morn_week0']
    mrw1 = user_data['morn_week1']
    evw0 = user_data['even_week0']
    evw1 = user_data['even_week1']
    print(mrw1)
    print(evw1)
    #await state.update_data(dates_week0 = []) # даты текущей недели.
    #await state.update_data(dates_week1 = []) # даты следующей недели.
    #await state.update_data(morn_week0 = []) # утры текущей недели - кто гуляет.
    #await state.update_data(morn_week1 = []) # утры следующей недели - кто гуляет.
    #await state.update_data(even_week0 = []) # вечера текущей недели - кто гуляет.
    #await state.update_data(even_week1 = []) # вечера следующей недели - кто гуляет.
    if message.text.lower() == "назад":
        await state.set_state(default_state)
        await message.answer("Правильно, "+user_data['name']+", нечего отменять собачека!", reply_markup=get_ref_keyboard())
    if message.text.lower() == "эта неделя":
        tmpkeyb = []
        tmpkeyb.append([])
        tmpkeyb.append([])
        await state.update_data(wn = '0')
        for i in range(7):
            #print(user_data['dates_week0'][i])
            tmpdt = datetime.date(int(user_data['dates_week0'][i].split('-')[0]),int(user_data['dates_week0'][i].split('-')[1]),int(user_data['dates_week0'][i].split('-')[2]))
            #print(tmpdt)
            if mrw0[i] == user_data['sname'] and tmpdt >= td:
                pos_mor_canc.append(user_data['days_week0'][i])
            if evw0[i] == user_data['sname'] and tmpdt >= td:
                pos_eve_canc.append(user_data['days_week0'][i])
        #print("after cycle")
        if len(pos_mor_canc) == 0 and len(pos_eve_canc) == 0:
            await message.answer("На этой неделе тебе нечего отменять", reply_markup=get_ref_keyboard())
            await state.set_state(default_state)
        else:       
            if len(pos_mor_canc) != 0 and len(pos_eve_canc) != 0: 
                #print("morn & even")
                for t in pos_eve_canc:
                    tmpkeyb[1].append(KeyboardButton(text="Вечер_"+t))
                for t in pos_mor_canc:
                    tmpkeyb[0].append(KeyboardButton(text="Утро_"+t))
                tmpkeyb.append([])
                tmpkeyb[2].append(KeyboardButton(text="Назад"))
            if len(pos_mor_canc) == 0:
                # only evenings can be canceled.
                #print("only even")
                for t in pos_eve_canc:
                    tmpkeyb[0].append(KeyboardButton(text="Вечер_"+t))
                tmpkeyb[1].append(KeyboardButton(text="Назад"))
            if len(pos_eve_canc) == 0:
                #print("only morn")
                # only mornings can be canceled.
                for t in pos_mor_canc:
                    tmpkeyb[0].append(KeyboardButton(text="Утро_"+t))
                tmpkeyb[1].append(KeyboardButton(text="Назад"))
            print(tmpkeyb)
            await message.answer("На этой неделе ты можешь отменить\n", reply_markup=ReplyKeyboardMarkup(keyboard=tmpkeyb, resize_keyboard=True, input_field_placeholder="выбор что отменить"))
    if message.text.lower() == "следующая":
        #print("зашли")
        tmpkeyb = []
        tmpkeyb.append([])
        tmpkeyb.append([])
        await state.update_data(wn = '1')
        for i in range(7):
            #print(user_data['dates_week0'][i])
            tmpdt = datetime.date(int(user_data['dates_week1'][i].split('-')[0]),int(user_data['dates_week1'][i].split('-')[1]),int(user_data['dates_week1'][i].split('-')[2]))
            if mrw1[i] == user_data['sname']:
                pos_mor_canc.append(user_data['days_week1'][i])
            if evw1[i] == user_data['sname']:
                pos_eve_canc.append(user_data['days_week1'][i])
        #print(tmpdt)
        if len(pos_mor_canc) == 0 and len(pos_eve_canc) == 0:
            await message.answer("На следующей неделе тебе пока нечего отменять", reply_markup=get_ref_keyboard())
            await state.set_state(default_state)
        else:
            if len(pos_mor_canc) != 0 and len(pos_eve_canc) != 0: 
                #print("morn & even")
                for t in pos_eve_canc:
                    tmpkeyb[1].append(KeyboardButton(text="Вечер_"+t))
                for t in pos_mor_canc:
                    tmpkeyb[0].append(KeyboardButton(text="Утро_"+t))
                tmpkeyb.append([])
                tmpkeyb[2].append(KeyboardButton(text="Назад"))
            if len(pos_mor_canc) == 0:
                # only evenings can be canceled.
                #print("only even")
                for t in pos_eve_canc:
                    tmpkeyb[0].append(KeyboardButton(text="Вечер_"+t))
                tmpkeyb[1].append(KeyboardButton(text="Назад"))
            if len(pos_eve_canc) == 0:
                #print("only morn")
                # only mornings can be canceled.
                for t in pos_mor_canc:
                    tmpkeyb[0].append(KeyboardButton(text="Утро_"+t))
                tmpkeyb[1].append(KeyboardButton(text="Назад"))
            #print(tmpkeyb)
            await message.answer("На следующей неделе ты можешь отменить\n", reply_markup=ReplyKeyboardMarkup(keyboard=tmpkeyb, resize_keyboard=True, input_field_placeholder="выбор что отменить"))
    if message.text.lower() == "утро_пн":
        wn = user_data['wn'] # wn = 0 <=> this week
        pict_path = user_data['pict_path'] +"eek"+wn+".jpg"
        new_img = Image.open(pict_path)
        pencil = ImageDraw.Draw(new_img)
        wdn = 1
        pencil.rectangle([40+(wdn-1)*32, 14+0*32, 65+(wdn-1)*32, 39+0*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        #---Let's update file wcalendar.txt
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week'+wn][wdn-1],0,"ПУ") #print(fname,dt,morning,person)
        #Let's update the timetable loaded.
        if wn == '0':
            mrw0[wdn-1] = "ПУ"
            await state.update_data(morn_week0 = mrw0)
        else:
            if wn == '1':
                mrw1[wdn-1] = "ПУ"
                await state.update_data(morn_week1 = mrw1)
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила утро понедельника. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил утро понедельника. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())
    if message.text.lower() == "вечер_пн":
        # this week пн
        pict_path = user_data['pict_path'] +"eek0.jpg"
        new_img = Image.open(pict_path)
        pencil = ImageDraw.Draw(new_img)
        wdn = 1
        pencil.rectangle([40+(wdn-1)*32, 14+1*32, 65+(wdn-1)*32, 39+1*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        #---Let's update file wcalendar.txt
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week0'][wdn-1],1,"ПУ")
        #Let's update the timetable loaded.
        mrw0[wdn-1] = "ПУ"
        await state.update_data(morn_week0 = mrw0)
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила вечер понедельника. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил вечер понедельника. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())
    if message.text.lower() == "утро_вт":
        # this week вт
        pict_path = user_data['pict_path'] +"eek0.jpg"
        new_img = Image.open(pict_path)
        pencil = ImageDraw.Draw(new_img)
        wdn = 2
        pencil.rectangle([40+(wdn-1)*32, 14+0*32, 65+(wdn-1)*32, 39+0*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        #---Let's update file wcalendar.txt
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week0'][wdn-1],0,"ПУ")
        #Let's update the timetable loaded.
        mrw0[wdn-1] = "ПУ"
        await state.update_data(morn_week0 = mrw0)
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила утро вторника. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил утро вторника. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())
    if message.text.lower() == "вечер_вт":
        # this week вт
        pict_path = user_data['pict_path'] +"eek0.jpg"
        new_img = Image.open(pict_path)
        pencil = ImageDraw.Draw(new_img)
        wdn = 2
        pencil.rectangle([40+(wdn-1)*32, 14+1*32, 65+(wdn-1)*32, 39+1*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        #---Let's update file wcalendar.txt
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week0'][wdn-1],1,"ПУ")
        #Let's update the timetable loaded.
        mrw0[wdn-1] = "ПУ"
        await state.update_data(morn_week0 = mrw0)
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила вечер вторника. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил вечер вторника. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())
    if message.text.lower() == "утро_ср":
        # this week ср
        pict_path = user_data['pict_path'] +"eek0.jpg"
        new_img = Image.open(pict_path)
        pencil = ImageDraw.Draw(new_img)
        wdn = 3
        pencil.rectangle([40+(wdn-1)*32, 14+0*32, 65+(wdn-1)*32, 39+0*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        #---Let's update file wcalendar.txt
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week0'][wdn-1],0,"ПУ")
        print("wdn=",wdn)
        #Let's update the timetable loaded.
        mrw0[wdn-1] = "ПУ"
        await state.update_data(morn_week0 = mrw0)
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила утро среды. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил утро среды. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())
    if message.text.lower() == "вечер_ср":
        # this week ср
        pict_path = user_data['pict_path'] +"eek0.jpg"
        new_img = Image.open(pict_path)
        pencil = ImageDraw.Draw(new_img)
        wdn = 3
        pencil.rectangle([40+(wdn-1)*32, 14+1*32, 65+(wdn-1)*32, 39+1*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        #---Let's update file wcalendar.txt
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week0'][wdn-1],1,"ПУ")
        #Let's update the timetable loaded.
        mrw0[wdn-1] = "ПУ"
        await state.update_data(morn_week0 = mrw0)
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила вечер среды. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил вечер среды. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())
    if message.text.lower() == "утро_чт":
        # this week чт morning
        pict_path = user_data['pict_path'] +"eek0.jpg"
        new_img = Image.open(pict_path)
        print("pict opened")
        pencil = ImageDraw.Draw(new_img)
        wdn = 4
        pencil.rectangle([40+(wdn-1)*32, 14+0*32, 65+(wdn-1)*32, 39+0*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        print("pict saved, путь =",pict_path)
        print("pict saved, chat_id =",user_data['cht_id'])
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        print("pict sent")
        #---Let's update file wcalendar.txt
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week0'][wdn-1],0,"ПУ")
        #Let's update the timetable loaded.
        #print("file on the disk updated")
        mrw0[wdn-1] = "ПУ"
        await state.update_data(morn_week0 = mrw0)
        print(user_data['name'])
        print(user_data['morn_week0'])
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила утро четверга. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил утро четверга. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())
    if message.text.lower() == "вечер_чт":
        # this week чт
        pict_path = user_data['pict_path'] +"eek0.jpg"
        new_img = Image.open(pict_path)
        pencil = ImageDraw.Draw(new_img)
        wdn = 4
        pencil.rectangle([40+(wdn-1)*32, 14+1*32, 65+(wdn-1)*32, 39+1*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        #---Let's update file wcalendar.txt
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week0'][wdn-1],1,"ПУ")
        #Let's update the timetable loaded.
        mrw0[wdn-1] = "ПУ"
        await state.update_data(morn_week0 = mrw0)
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила вечер четверга. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил вечер четверга. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())
    if message.text.lower() == "утро_пт":
        # this week пт
        pict_path = user_data['pict_path'] +"eek0.jpg"
        new_img = Image.open(pict_path)
        pencil = ImageDraw.Draw(new_img)
        wdn = 5
        pencil.rectangle([40+(wdn-1)*32, 14+0*32, 65+(wdn-1)*32, 39+0*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        #---Let's update file wcalendar.txt
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week0'][wdn-1],0,"ПУ")
        #Let's update the timetable loaded.
        mrw0[wdn-1] = "ПУ"
        await state.update_data(morn_week0 = mrw0)
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила утро пятницы. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил утро пятницы. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())
    if message.text.lower() == "вечер_пт":
        # this week пт
        pict_path = user_data['pict_path'] +"eek0.jpg"
        new_img = Image.open(pict_path)
        pencil = ImageDraw.Draw(new_img)
        wdn = 5
        pencil.rectangle([40+(wdn-1)*32, 14+1*32, 65+(wdn-1)*32, 39+1*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        #---Let's update file wcalendar.txt
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week0'][wdn-1],1,"ПУ")
        #Let's update the timetable loaded.
        mrw0[wdn-1] = "ПУ"
        await state.update_data(morn_week0 = mrw0)
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила вечер пятницы. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил вечер пятницы. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())
    if message.text.lower() == "утро_сб":
        # this week сб
        pict_path = user_data['pict_path'] +"eek0.jpg"
        new_img = Image.open(pict_path)
        pencil = ImageDraw.Draw(new_img)
        wdn = 6
        pencil.rectangle([40+(wdn-1)*32, 14+0*32, 65+(wdn-1)*32, 39+0*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        #---Let's update file wcalendar.txt
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week0'][wdn-1],0,"ПУ")
        #Let's update the timetable loaded.
        mrw0[wdn-1] = "ПУ"
        await state.update_data(morn_week0 = mrw0)
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила утро субботы. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил утро субботы. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())
    if message.text.lower() == "вечер_сб":
        # this week сб
        pict_path = user_data['pict_path'] +"eek0.jpg"
        new_img = Image.open(pict_path)
        pencil = ImageDraw.Draw(new_img)
        wdn = 6
        pencil.rectangle([40+(wdn-1)*32, 14+1*32, 65+(wdn-1)*32, 39+1*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        #---Let's update file wcalendar.txt
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week0'][wdn-1],1,"ПУ")
        #Let's update the timetable loaded.
        mrw0[wdn-1] = "ПУ"
        await state.update_data(morn_week0 = mrw0)
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила вечер субботы. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил вечер субботы. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())
    
    if message.text.lower() == "утро_вс":
        # this week вс
        pict_path = user_data['pict_path'] +"eek0.jpg"
        new_img = Image.open(pict_path)
        pencil = ImageDraw.Draw(new_img)
        wdn = 7
        pencil.rectangle([40+(wdn-1)*32, 14+0*32, 65+(wdn-1)*32, 39+0*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        #---Let's update file wcalendar.txt
        print(user_data['dates_week0'][wdn-1])
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week0'][wdn-1],0,"ПУ")
        #Let's update the timetable loaded.
        mrw0[wdn-1] = "ПУ"
        await state.update_data(morn_week0 = mrw0)
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила утро воскресенья. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил утро воскресенья. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())
    if message.text.lower() == "вечер_вс":
        # this week вс
        pict_path = user_data['pict_path'] +"eek0.jpg"
        new_img = Image.open(pict_path)
        pencil = ImageDraw.Draw(new_img)
        wdn = 7
        pencil.rectangle([40+(wdn-1)*32, 14+1*32, 65+(wdn-1)*32, 39+1*32],fill = (255, 255, 255, 0), outline = 'gray', width = 1)
        new_img.save(pict_path)
        await state.set_state(default_state)
        await bot.send_photo(chat_id=user_data['cht_id'], photo=types.FSInputFile(pict_path))
        #---Let's update file wcalendar.txt
        put_into(user_data['pict_path']+"utf8calendar.txt",user_data['dates_week0'][wdn-1],1,"ПУ")
        #Let's update the timetable loaded.
        evw0[wdn-1] = "ПУ"
        await state.update_data(even_week0 = evw0)
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        if user_data['name'] == "ММ":
            await bot.send_message(chat_id=cht_id, text="Малышка мама освободила вечер воскресенья. Пользуйстесь возможностью погулять собачека😊")
        else:
            await bot.send_message(chat_id=cht_id, text=user_data['name']+" освободил вечер воскресенья. Пользуйстесь возможностью погулять собачека😊")
        await message.answer("Освободили...", reply_markup=get_ref_keyboard())

@dp.message(F.text, StateFilter(play.choisepersondate))
# идёт выбор времени человека погулять.
async def echo_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    td = datetime.date.today()
    twd = td.weekday() + 1 # день недели, пн = 1.
    wp = user_data['wanted_person'] # the person user wants to ask to walk the doggy dog.
    fl = True # fl = true <=> команда не распознана.
    dn = True # dn = true <=> команда не обработана, требуются дальнейшие действия.
    pos_can = [] # potintial days/times to ask for.
    if message.text.lower() == "назад":
        fl = False
        dn = False
        await message.answer("Вернулись", reply_markup=personkeyboard())
        await state.set_state(play.choiseperson)
    mw0 = user_data['morn_week0']
    ew0 = user_data['even_week0']
    mw1 = user_data['morn_week1']
    ew1 = user_data['even_week1']
    if message.text.lower() == "пн":
        pos_can = []
        fl = False
        if twd == 1:
            # it is monday so let's choise this week or the next one.
            if mw0[0] == "ПУ":
                pos_can.append("утро этого пн")
            if ew0[0] == "ПУ":
                pos_can.append("вечер этого пн")
            if mw1[0] == "ПУ":
                pos_can.append("утро след пн")
            if ew1[0] == "ПУ":
                pos_can.append("вечер след пн")
        else:
            # the only possible week is the next one.
            if mw1[0] == "ПУ":
                pos_can.append("утро_пн")
            if ew1[0] == "ПУ":
                pos_can.append("вечер_пн")
    if message.text.lower() == "вт":
        pos_can = []
        fl = False
        if twd <= 2:
            if mw0[1] == "ПУ":
                pos_can.append("утро этого вт")
            if ew0[1] == "ПУ":
                pos_can.append("вечер этого вт")
            if mw1[1] == "ПУ":
                pos_can.append("утро след вт")
            if ew1[1] == "ПУ":
                pos_can.append("вечер след вт")
        else:
            # the only possible week is the next one.
            if mw1[1] == "ПУ":
                pos_can.append("утро след вт")
            if ew1[1] == "ПУ":
                pos_can.append("вечер след вт")   
    if message.text.lower() == "ср":
        pos_can = []
        fl = False
        if twd <= 3:
            if mw0[2] == "ПУ":
                pos_can.append("утро этой ср")
            if ew0[2] == "ПУ":
                pos_can.append("вечер этой ср")
            if mw1[2] == "ПУ":
                pos_can.append("утро след ср")
            if ew1[2] == "ПУ":
                pos_can.append("вечер след ср")
        else:
            # the only possible week is the next one.
            if mw1[2] == "ПУ":
                pos_can.append("утро след ср")
            if ew1[2] == "ПУ":
                pos_can.append("вечер след ср")
    if message.text.lower() == "чт":
        pos_can = []
        fl = False
        if twd <= 4:
            if mw0[3] == "ПУ":
                pos_can.append("утро этого чт")
            if ew0[3] == "ПУ":
                pos_can.append("вечер этого чт")
            if mw1[3] == "ПУ":
                pos_can.append("утро след чт")
            if ew1[3] == "ПУ":
                pos_can.append("вечер след чт")
        else:
            # the only possible week is the next one.
            if mw1[3] == "ПУ":
                pos_can.append("утро след чт")
            if ew1[3] == "ПУ":
                pos_can.append("вечер след чт")
    if message.text.lower() == "пт":
        pos_can = []
        fl = False
        if twd <= 5:
            if mw0[4] == "ПУ":
                pos_can.append("утро этой пт")
            if ew0[4] == "ПУ":
                pos_can.append("вечер этой пт")
            if mw1[4] == "ПУ":
                pos_can.append("утро след пт")
            if ew1[4] == "ПУ":
                pos_can.append("вечер след пт")
        else:
            # the only possible week is the next one.
            if mw1[4] == "ПУ":
                pos_can.append("утро след пт")
            if ew1[4] == "ПУ":
                pos_can.append("вечер след пт")
    if message.text.lower() == "сб":
        pos_can = []
        fl = False
        if twd <= 6:
            if mw0[5] == "ПУ":
                pos_can.append("утро этой сб")
            if ew0[5] == "ПУ":
                pos_can.append("вечер этой сб")
            if mw1[5] == "ПУ":
                pos_can.append("утро след сб")
            if ew1[5] == "ПУ":
                pos_can.append("вечер след сб")
        else:
            # the only possible week is the next one.
            if mw1[5] == "ПУ":
                pos_can.append("утро след сб")
            if ew1[5] == "ПУ":
                pos_can.append("вечер след сб")
    if message.text.lower() == "вс":
        pos_can = []
        fl = False
        if mw0[6] == "ПУ":
            pos_can.append("утро этого вс")
        if ew0[6] == "ПУ":
            pos_can.append("вечер этого вс")
        if mw1[6] == "ПУ":
            pos_can.append("утро след вс")
        if ew1[6] == "ПУ":
            pos_can.append("вечер след вс")
    if message.text.lower() == "утро этого вс":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром ближайшего воскресенья.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер этого вс":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером ближайшего воскресенья.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "утро след вс":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром следующего воскресенья.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер след вс":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером следующего воскресенья.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    #-----
    if message.text.lower() == "утро этого пн":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром сегодня, в понедельник.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер этого пн":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером сегодня, в понедельник.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "утро след пн":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром следующего понедельника.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер след пн":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером следующего понедельника.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    #----------
    if message.text.lower() == "утро этого вт":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром этого вторника.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер этого вт":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером этого вторника.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "утро след вт":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром следующего вторника.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер след вт":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером следующего вторника.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    #----------
    if message.text.lower() == "утро этой ср":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром в эту среду.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер этой ср":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером в эту среду.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "утро след ср":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром следующей среды.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер след ср":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером следующей среды.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    #----------
    if message.text.lower() == "утро этого чт":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром в ближайший четверг.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер этого чт":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером в ближайший четверг.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "утро след чт":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром следующего четверга.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер след чт":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером следующего четверга.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    #----------
    if message.text.lower() == "утро этой пт":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром в эту пятницу.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер этой пт":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером в эту пятницу.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "утро след пт":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром пятницы на следующей неделе.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер след пт":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером пятницы на следующей неделе.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    #----------
    if message.text.lower() == "утро этой сб":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром в субботу на этой неделе.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер этой сб":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером в субботу на этой неделе.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "утро след сб":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса утром в субботу на следующей неделе.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    if message.text.lower() == "вечер след сб":
        fl = False
        dn = False
        msg = user_data['wanted_person']+", тебя просят прогулять пса вечером в субботу на следующей неделе.\nНе откажись - запишись😀 "+user_data['wanted_person_uname']
        #cht_id = 120443225 # this is my chat.
        cht_id = user_data['famcht_id'] # this is our family chat.
        await bot.send_message(chat_id=cht_id, text=msg)
        await message.answer("Попросили!", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    #----------
    if fl:
        await message.answer("Я такое не понимаю. Нажми на кнопку чтобы выбрать день", reply_markup=daykeyboard())
        #await state.set_state(play.choisepersondate)
    else:
        if dn:
            if len(pos_can) == 0:
                await message.answer("В этот день уже всё занято, не погулять.\nВначале надо отменить прогулку, потом занимать местечко", reply_markup=get_ref_keyboard())
                await state.set_state(default_state)
            else:
                print(pos_can)
                # Создание клавиатуры
                kb = [[],[]]
                for st in pos_can: 
                    kb[0].append(KeyboardButton(text=st))
                kb[1].append(KeyboardButton(text="Назад"))
                await message.answer("Вот возможные варианты:", reply_markup=ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,input_field_placeholder="Свободные возможности"))      

@dp.message(F.text, StateFilter(play.choiseperson))
# идёт выбор человека погулять.
async def echo_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    fl = True # fl = ture <=> команда не распознана.
    if message.text.lower() == "назад":
        fl = False
        await message.answer("Добро, никого не просим", reply_markup=get_ref_keyboard())
        await state.set_state(default_state)
    else:
        if message.text.lower() == "сп - суперпапаша":
            fl = False
            await message.answer("Когда просим его погулять?", reply_markup=daykeyboard())
            await state.set_state(play.choisepersondate)
            await state.update_data(wanted_person = 'Илья')
            await state.update_data(wanted_person_uname = '@ilya_medved')
            #cht_id = 120443225 # this is my chat.
            #cht_id = user_data['famcht_id'] # this is our family chat.
        if message.text.lower() == "мм - малышка мама":
            fl = False
            await message.answer("Когда просим её погулять?", reply_markup=daykeyboard())
            await state.set_state(play.choisepersondate)
            await state.update_data(wanted_person = 'Оля')
            await state.update_data(wanted_person_uname = '@seal_1307')
        if message.text.lower() == "ка - красавчик андрей":
            fl = False
            await message.answer("Когда просим его погулять?", reply_markup=daykeyboard())
            await state.set_state(play.choisepersondate)
            await state.update_data(wanted_person = 'Андрей')
            await state.update_data(wanted_person_uname = '@zeus_f1re')
        if message.text.lower() == "кн - крутой никита":
            fl = False
            await message.answer("Когда просим его погулять?", reply_markup=daykeyboard())
            await state.set_state(play.choisepersondate)
            await state.update_data(wanted_person_uname = '@Insp1red505')
            await state.update_data(wanted_person = 'Никита')
    if fl:
        await message.answer("Я такое не понимаю. Нажми на кнопку чтобы выбрать человека", reply_markup=personkeyboard())
        #await state.set_state(play.choisepersondate)

# Обработчик текстовых сообщений
@dp.message(F.text, StateFilter(play.choisedate))
# идёт выбор даты погулять.
async def echo_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    td = datetime.date.today()
    twd = td.weekday() + 1 # день недели, пн = 1.
    fl = False # fl = True <=> введена корректная дата / день.
    if message.text.lower() == "назад":
        await state.set_state(default_state)
        await message.answer("Да, "+user_data['name'], reply_markup=get_ref_keyboard())
    #else:
    #    await message.answer(f"Введи дату или день недели либо нажми Назад для возврата.\nФорматы такие:\nпн, вт, ср, чт, пт, сб, вс\nдд.мм, дд.мм.гг, дд.мм.гггг", reply_markup=daykeyboard())
    if message.text.lower() == "пн":
        fl = True
        await state.update_data(wd = message.text)
        await state.update_data(wdn = 1)
        if twd == 1:
            cdt = td # choosen date is today.
            await state.update_data(week = 0)
        else:
            cdt = td + datetime.timedelta(days =7 - (twd-1)) # choosen date is in the future.
            await state.update_data(week = 1)
    if message.text.lower() == "вт":
        fl = True
        await state.update_data(wdn = 2)
        await state.update_data(wd = message.text)
        if twd == 2:
            cdt = td # choosen date is today.
            await state.update_data(week = 0)
        if twd == 1:
            cdt = td + datetime.timedelta(days = 1)
            await state.update_data(week = 0)
        if twd > 2:
            cdt = td + datetime.timedelta(days =7 - (twd-2))
            await state.update_data(week = 1)
    if message.text.lower() == "ср":
        fl = True
        await state.update_data(wdn = 3)
        await state.update_data(wd = message.text)
        if twd <= 3:
            cdt = td + datetime.timedelta(days =3-twd) #choosen day is on this week.
            await state.update_data(week = 0)
        if twd > 3:
            cdt = td + datetime.timedelta(days =7 - (twd-3)) # choosen day is on the next week.
            await state.update_data(week = 1)
    if message.text.lower() == "чт":
        fl = True
        await state.update_data(wdn = 4)
        await state.update_data(wd = message.text)
        if twd <= 4:
            cdt = td + datetime.timedelta(days = 4-twd) #choosen day is on this week.
            await state.update_data(week = 0)
        if twd > 4:
            cdt = td + datetime.timedelta(days = 7 - (twd-4)) # choosen day is on the next week.
            await state.update_data(week = 1)
    if message.text.lower() == "пт":
        fl = True
        await state.update_data(wdn = 5)
        await state.update_data(wd = message.text)
        if twd <= 5:
            cdt = td + datetime.timedelta(days = 5-twd) #choosen day is on this week.
            await state.update_data(week = 0)
        if twd > 5:
            cdt = td + datetime.timedelta(days = 7 - (twd-5)) # choosen day is on the next week.
            await state.update_data(week = 1)
    if message.text.lower() == "сб":
        fl = True
        await state.update_data(wdn = 6)
        await state.update_data(wd = message.text)
        if twd <= 6:
            cdt = td + datetime.timedelta(days =6-twd) #choosen day is on this week.
            await state.update_data(week = 0)
        if twd > 6:
            cdt = td + datetime.timedelta(days =7 - (twd-6)) # choosen day is on the next week.
            await state.update_data(week = 1)
    if message.text.lower() == "вс":
        fl = True
        await state.update_data(wdn = 7)
        await state.update_data(wd = message.text)
        cdt = td + datetime.timedelta(days = 7-twd) # choosen day is on the this week - it is sunday.
        await state.update_data(week = 0)
    # ------------- dates -----------------
    # not ready yet
    if fl:
        #await state.update_data(week = 0) # just in debugging purposes. delete afterwards.
        await state.update_data(dt = cdt)
        await state.set_state(play.choisetime)
        await message.answer(f"Осталось выбрать время", reply_markup=timekb())   
        #await message.answer(f"Отлично, выбирай любой день!\nВведи дату или день недели. Я понимаю такое:\nпн, вт, ср, чт, пт, сб, вс\nдд.мм, дд.мм.гг, дд.мм.гггг", reply_markup=daykeyboard())
        #print(user_data['dates_week0'])
        #print(user_data['morn_week0'])
        #print(user_data['even_week0'])
    else:
        current_state = await state.get_state()
        #print(current_state)
        if current_state == play.choisedate:
            await message.answer("Я такого не понимаю. Попробуй ещё разок", reply_markup=daykeyboard())

# Запуск бота
async def main():
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
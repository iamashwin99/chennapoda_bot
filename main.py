import os
import telebot
import pandas as pd
from datetime import datetime
import pytz
import json
import random
import requests as re


API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)
IST = pytz.timezone('Asia/Kolkata')
uri = "https://api.susi.ai/susi/chat.json?timezoneOffset=+530&q=" 

listOfFoods=["IDK do something",
"What didi what",
"Make something tasty",
"What Bhaiya What",
"monaco chat",
"milkshake",
"idk anything",
"khichdi",
"tomato rice",
"oats",
"Make samosa",
"Neerdosa it is",
"photo-synthesis is the best thing",
"Yum Yum Cup-cakes",
"Veg Shawarma",
"Pizza",
"Lets partyyy",
"Sprouts is healthy",
""

]

listOfGames=["we can play scribbl",
"We can play chess",
"Badminton",
"Badminton",
"Badminton",
"lets party at MedC",
"Lets go out",
"Lets do matlab",
"Machine learning is fun"
]

listOfAlive=["Yes",
"Yes",
"No \n JK Im alive",
"Im dead from the inside",
"Am i really alive",
"IDK you tell me",
"Im dexter",
"IG",
"yes but im going to get chopped soon :)"
]
def callSusi(query):
  ans = json.loads(re.get(uri+query).content)
  return ans['answers'][0]['actions'][0]['expression']


def getMealNow():
  meal = ""
  datetime_ist = datetime.now(IST)
  hour = datetime_ist.strftime('%H')
  day = datetime_ist.strftime('%a')

  if(int(hour)>=11 and int(hour)< 15 ):
    meal = "Lunch"
  elif(int(hour)>=15 and int(hour)< 18 ):
    meal = "Snacks"
  elif(int(hour)>=18 and int(hour)< 22 ):
    meal = "Dinner"
  else:
    meal = "Breakfast"
  return [day,meal]


def getMessy(meal):
  returnString = ""
  url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSpgPFjsVbVak8MuXxOYEV8ezmsXC38Ki13xHcGwVt3YbFRoRSKwiRemMk9lCGOKRsDCrlYtD2ePg7V/pub?output=csv"
  df = pd.read_csv(url)
  if(meal not in ['Breakfast','Lunch','Snacks','Dinner']):
    [day,meal] = getMealNow()
  for i in range(len(df)):
    returnString += f"{meal} at {df.Hostel[i]} is {df[meal][i]} last updated at {df.Timestamp[i]} \n ##### \n"

  return returnString

def extract_arg(arg):
    return arg.split()[1:]



@bot.message_handler(commands=['howmessycanitget'])
def mess(message):
  bot.reply_to(message, getMessy("none"))


@bot.message_handler(commands=['whatshouldweeat'])
def whattoeat(message):
  a = random.randint(0,len(listOfFoods)-1)
  
  bot.reply_to(message, listOfFoods[a])

@bot.message_handler(commands=['whatshouldwedo'])
def whattodo(message):
  a = random.randint(0,len(listOfGames)-1)
  bot.reply_to(message, listOfGames[a])

@bot.message_handler(commands=['areyoualive'])
def alive(message):
  a = random.randint(0,len(listOfAlive)-1)
  bot.reply_to(message, listOfAlive[a])



@bot.message_handler(commands=['hello'])
def hello(message):
  bot.send_message(message.chat.id, "Hello!")

@bot.message_handler(commands=['chat'])
def chat(message):
  try:
        bot.reply_to(message, callSusi(message.text.replace('/chat','')))
  except:
    pass

@bot.message_handler(func=lambda m: True)
def echo_all(message):
  Q = message.text.replace("@chennapoda_bot","")
  if (Q!=message.text):
    if(Q.replace('/','')==Q):
      try:
        bot.reply_to(message, callSusi(Q))
      except:
        pass
  #status = extract_arg(message.text)
  #print(status)

  #bot.reply_to(message, message.text)


bot.polling()

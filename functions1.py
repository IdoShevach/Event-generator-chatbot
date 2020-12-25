from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
import datetime
from datetime import date, timedelta
import io
import csv

def find_num(num):
    message = " my name is Roberta, I'm here to help you find the best date for your event." + "\n" + "1)For a daily event enter '1'." + "\n" + "2)For an event of two days or more enter '2'." + "\n" + "If you want to finish click done"
    with open("phoneNumber.txt") as f1:
        phone_numbers = csv.reader(f1, delimiter=",")
        for phone in phone_numbers:
            if str(num)==phone[0]:
                return "Hey Ido!"+message
            if str(num)==phone[1]:
                return "Hey Jonathan!"+message
            if str(num)==phone[2]:
                return "Hey Sahar!" + message
            if str(num)==phone[3]:
                return "Hey Guy!" + message
            if str(num)==phone[4]:
                return "Hey Yuval!" + message
            if str(num)==phone[5]:
                return "Hey Omri!" + message
            if str(num) == phone[6]:
                return "Hey Amos!" + message
            if str(num) == phone[7]:
                return "Hey Idan!" + message
            if str(num) == phone[8]:
                return "Hey Shahaf!" + message
            if str(num) == phone[9]:
                return "Hey Mamul!" + message
            if str(num) == phone[10]:
                return "Hey Ben!" + message
            else:
                return "Hey!" + message





def get_userName1(num):
    with open("phoneNumber.txt") as f1:
        phone_numbers = csv.reader(f1, delimiter=",")
        for phone in phone_numbers:
            if str(num)==phone[0]:
                return "Ido"
            if str(num)==phone[1]:
                return "Jonathan"
            if str(num)==phone[2]:
                return "Sahar"
            if str(num)==phone[3]:
                return "Guy"
            if str(num)==phone[4]:
                return "Yuval"
            if str(num)==phone[5]:
                return "Omri"
            if str(num) == phone[6]:
                return "Amos"
            if str(num) == phone[7]:
                return "Idan"
            if str(num) == phone[8]:
                return "Shahaf"
            if str(num) == phone[9]:
                return "Mamul"
            if str(num) == phone[10]:
                return "Ben"
            else:
                return str(num)




def check_dates(date):
    if len(date[date.rfind("/"):]) != 5:
        return False
    if date.count("/")!=2:
        print("False")
        return False
    day, month, year = date.split('/')
    isValidDate = True
    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False

    if (isValidDate) and datetime.datetime.strptime(date, "%d/%m/%Y")>datetime.datetime.today():
        # print("Input date is valid ..")
         return True
    else:
        return False



def check_twoDates1(dates):
    if "-" not in dates:
        return False
    else:
      x=dates.find("-")
      start_date=dates[0:x]
      end_date=dates[x+1:]
      if check_dates(start_date)==False or check_dates(end_date)==False:
          return False
      start= datetime.datetime.strptime(start_date, "%d/%m/%Y")
      end= datetime.datetime.strptime(end_date, "%d/%m/%Y")
      if start<end:
         return True
      else:
        return False




def make_final_date(date):
    x = date.find("/")
    y = date.rfind("/")
    days = str(int(date[0:x]))
    month = str(int(date[x + 1:y]))
    year = str(int(date[y + 1:]))
    new_date = days + "/" + month + "/" + year
    return new_date


def check_choice(msg):
    options=["Done","done","1","2"]
    if str(msg) in options:
        return True
    else:
        return False



def enter_datesTocsv(start,end,num):
    name = get_userName1(str(num))
    start_date = datetime.datetime.strptime(start, "%d/%m/%Y")
    end_date = datetime.datetime.strptime(end, "%d/%m/%Y")
    delta = end_date - start_date
    with io.open("bigEvent.csv", "a", encoding="utf-8")as f1:
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            DAY = datetime.datetime.strftime(day, "%d/%m/%Y")
            f1.write(str(DAY) + "," + str(name) + "\n")





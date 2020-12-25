import csv
from pymongo import MongoClient
from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import urllib
from urllib.parse import urlparse
import io
from functions1 import *
from functions2 import *

#this part is to open the data-base
with open("cred.txt.txt") as f1:
    datarow=csv.reader(f1,delimiter=",")
    for row in datarow:
        id=row[0]
        pwd=row[1]

client=MongoClient("mongodb+srv://"+id+":"+urllib.parse.quote(pwd)+"@cluster0.jozda.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client["whatsapp_db"]
collection = db["whatsapp_collection"]

#end data-base parts

apbot=Flask(__name__)
@apbot.route("/sms",methods=["get","post"])
def reply():
    num=request.form.get("From")
    num=num.replace("whatsapp:","")    #num= user phone number
    msg_text=request.form.get("Body")
    x=collection.find_one({"NUMBER":num})
    msg=MessagingResponse()
    try:
        status=x["status"]
    except:
        pass
    if (bool(x)==False):                   #user coming for the first time(no status in the data)
        collection.insert_one({"NUMBER":num,"status":"first"})
        resp=msg.message(find_num(num))  #send menu message
        return(str(msg))

    if collection.find_one({"NUMBER": num,"finish":"done"}):
        respone=msg.message("You are currently blocked and can not add dates."+"\n"+"For more information you are welcome to contact my manager")
        return (str(msg))

    if(status=="first"):
           if check_choice(msg_text)==False:
               respone=msg.message("You entered an incorrect option,try again")
               return str(msg)
           else:
              if str(msg_text).lower()=="done":
                 respone=msg.message("Thank you")
                 collection.insert_one({"NUMBER": num, "finish": "done"})
                 return (str(msg))
              if str(msg_text)=="2":    #if the event is for 2 days or more
                 collection.delete_one({"NUMBER":num,"status":"first"})
                 collection.insert_one({"NUMBER":num,"status":"second"})
                 respone=msg.message("You have selected a two-days or more event. Please enter your start date and end date in the format: 'dd/mm/yyyy-dd/mm/yyyy'."+"\n"+"For example:'5/5/2021-10/5/2021'"+"\n"+"To watch the best results until now press '0'")
                 return (str(msg))
              if str(msg_text)=="1":    #if the event is for one day
                  collection.delete_one({"NUMBER":num,"status":"first"})
                  collection.insert_one({"NUMBER": num, "status":"one"})
                  respone=msg.message("You chose one day event,please enter your date in the format dd/mm/yyyy."+"\n"+"To watch the best results until now press '0'")
                  return str(msg)
    if(status=="second"):                        ####Two days event
        if str(msg_text).lower() == "done":
            respone = msg.message("Thank you")  # need to finish this part
            collection.insert_one({"NUMBER": num, "finish": "done"})
            return (str(msg))
        if str(msg_text)=="0":
            respone=msg.message(str(findDate_ForBigEvent("bigEvent.csv")))
            respone1=msg.message("You can add another start date and end date for the event in the same format: 'dd/mm/yyyy-dd/mm/yyyy'"+"\n"+"-> To finish enter 'done'")
            return (str(msg))
        else:
            if check_twoDates1(str(msg_text))==True:
                date=str(msg_text)
                z = date.find("-")
                start_date =make_final_date(date[0:z])
                end_date =make_final_date(date[z+1:])
                if collection.find_one({"NUMBER": num, "status": "second","start_date": start_date,"end_date":end_date}):
                    respone = msg.message("You have already entered the date " + start_date +"-"+end_date+ " please try again in the format 'dd/mm/yyyy'-'dd/mm/yyyy'."+"\n"+"For example:'5/5/2021-10/5/2021.")
                    return (str(msg))
                else:
                    collection.insert_one({"NUMBER":num,"status":"second","start_date": start_date,"end_date":end_date})
                    enter_datesTocsv(str(start_date),str(end_date),str(num))
                    respone = msg.message("Thank you. If you want you can add alternative date in the same format."+"\n"+"To watch the best results until now press '0'"+"\n"+"If you are done enter: 'Done'")
                    return (str(msg))
            else:
                respone = msg.message("The date you have entered is incorrect." + "\n" + "Please enter your start date and end date in the format dd/mm/yyyy-dd/mm/yyyy."+"\n"+"For example:'5/5/2021-10/5/2021")
                return (str(msg))

    if (status == "one"):                      #One day event
        if str(msg_text).lower() == "done":
            respone = msg.message("Thank you")  # need to finish this part
            collection.insert_one({"NUMBER":num,"finish":"done"})
            return (str(msg))
        if str(msg_text)=="0":
            respone = msg.message(str(find_mostCommon("respone.csv")))
            respone1 = msg.message("You can add another date for the event in the same format: 'dd/mm/yyyy'" + "\n" + "-> To finish enter 'done'.")
            return (str(msg))
        else:
         with io.open("respone.csv", "a", encoding="utf-8")as f1:
            x=str(msg_text)
            if check_dates(x)==True:
                final_date=make_final_date(x)
                if collection.find_one({"NUMBER":num,"status":"one","Date:":final_date}):
                    respone = msg.message("You have already entered the date "+final_date+" please try again in the format dd/mm/yyyy")
                    return (str(msg))
                else:
                    collection.insert_one({"NUMBER":num,"status":"one","Date:":final_date})
                    date=final_date
                    name=get_userName1(str(num))
                    f1.write(date+","+name+"\n")
                    respone=msg.message("Thank you, if you want you can add another date in the same format."+"\n"+"To watch the best results until now press '0'."+"\n"+"If you want to finish, enter: 'done'.")
                    return (str(msg))
            else:
              respone=msg.message("The date you entered is incorrect."+"\n"+"please try again in the format dd/mm/yyyy")
              return (str(msg))





if (__name__=="__main__"):
    apbot.run()


import csv
import datetime
from datetime import date, timedelta
import matplotlib.pyplot as plt

NUM_DAYS=3


def get_dictDateAndName(file):
    with open(file, newline='') as csvfile:
        read = csv.reader(csvfile)
        d1=dict()
        for row in read:
            if row[0] not in d1:
                d1[row[0]] = {row[1]}
            else:
                d1[row[0]].add(row[1])
    return d1

def date_diff(date0,date1):
    d0=datetime.datetime.strptime(date0, "%d/%m/%Y")
    d1=datetime.datetime.strptime(date1, "%d/%m/%Y")
    delta = d1 - d0
    return delta.days




def find_mostCommon(file):
    with open(file, newline='') as csvfile:
        read = csv.reader(csvfile)
        date_list=[]
        date_dict={}
        for row in read:
            date=row[0]
            date_list.append(date)
    d1=get_dictDateAndName("respone.csv")
    for date in date_list:
        date_dict[date]=date_list.count(date)
    sort_topDates = dict(sorted(date_dict.items(), key=lambda x: x[1], reverse=True)[:10])
    dictDate_nName=dict()
    for date in sort_topDates:
        for key,value in d1.items():
            if date==key:
                dictDate_nName[date]=value
    print(dictDate_nName)
    result = ""
    for key, value in sort_topDates.items():
        result += "*Date: " + key + ", Votes: " + str(value) + "\n"
    # result+="\n"+str(dictDate_nName)
    return result



def get_startDates(file):
    with open(file, newline='') as csvfile:
        read = csv.reader(csvfile)
        all_dates=[]
        for row in read:
            all_dates.append(row[0])
    all_dates_asDate=[datetime.datetime.strptime(date, "%d/%m/%Y") for date in all_dates]
    set1=set()
    for date in all_dates_asDate:
        counter=0
        for i in range(NUM_DAYS):
            if date+timedelta(days=i) in all_dates_asDate:
                counter=counter+1
            if counter==NUM_DAYS:
                set1.add(date)
    return set1






def findDate_ForBigEvent(file):
    with open(file, newline='') as csvfile:
        read = csv.reader(csvfile)
        d = dict()  # dictionary of names and dates.
        for row in read:
            if row[1] not in d:
                d[row[1]] = {row[0]}
            else:
                d[row[1]].add(row[0])

    all_dates = []  # all allthe dates without names.
    for num in d.values():
        for date in num:
            all_dates.append(date)

    d_dates1 = dict()  # dictionary of dates with count as datetime.
    set_Dates = set(all_dates)  # all dates one time.

    for date in set_Dates:
        d_dates1[datetime.datetime.strptime(date, "%d/%m/%Y")] = all_dates.count(date)

    start_dateSet = get_startDates("bigEvent.csv")
    datesFor_evevt = []
    for date in start_dateSet:
        counter = 0
        for i in range(NUM_DAYS):
            counter += d_dates1[date + timedelta(days=i)]
        start_date = date
        end_date = date + timedelta(days=NUM_DAYS - 1)
        datesFor_evevt.append((start_date, end_date, counter))
    finalDate_dict = {}
    for i in datesFor_evevt:
        finalDate_dict[
            datetime.datetime.strftime(i[0], "%d/%m/%Y") + "-" + datetime.datetime.strftime(i[1], "%d/%m/%Y")] = i[2]
    # plt.bar(*zip(*finalDate_dict.items()))
    # plt.show()

    sort_topDates = dict(sorted(finalDate_dict.items(), key=lambda x: x[1], reverse=True)[:10])
    result = ""
    for key, value in sort_topDates.items():
        result += "*Date: " + key + ", Votes: " + str(value) + "\n"
    print(result)
    sort_datesFor_event = sorted(datesFor_evevt, key=lambda x: x[2], reverse=True)
    new_dateSet = set()
    for date in sort_datesFor_event:
        start = date[0]
        end = date[1]
        delta = end - start
        for i in range(delta.days + 1):
            day = start + timedelta(days=i)
            new_dateSet.add(day)
    topDates_list = list(new_dateSet)
    sort_topDates_list = sorted(topDates_list, key=lambda x: x)
    str_topDates_list = [datetime.datetime.strftime(date, "%d/%m/%Y") for date in sort_topDates_list]
    print(str_topDates_list)
    d1 = get_dictDateAndName("bigEvent.csv")
    dic_namesWithDates = dict()
    print(d1)
    for date in str_topDates_list:
        for key, value in d1.items():
            if date == key:
                dic_namesWithDates[key] = value
    print(dic_namesWithDates)
    # for key,value in dic_namesWithDates.items():
    #     result+=""+key+":"+str(value)+", "
    return result




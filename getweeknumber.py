# -*- coding: utf-8 -*-
"""
calculate the week number of each volunteer
"""

from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def getWeekNumber(endDateStr, renewTimes = 0):
    enddate = datetime.strptime(endDateStr, '%m/%d/%Y')
    startdate = enddate - relativedelta(months = (renewTimes+1) * 3)
    
    startdate = startdate.date();
    today = date.today();
    print(startdate)
    days_til_now = (today - startdate).days
    weeks_num = int(days_til_now/7)
    return weeks_num

print(getWeekNumber("7/24/2023",2))
    
    
    
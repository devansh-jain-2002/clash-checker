import pandas as pd
from datetime import datetime
df = pd.read_excel("Courses.xls")
def time_table(s):
    l = s.split(" ,")
    tt = {}
    for x in l:
        days, times = x.split()
        st,en = times.split("-")
        start = datetime.strptime(st,"%H:%M")
        end = datetime.strptime(en,"%H:%M")
        time = [start,end]
        if('M' in days):
            tt['M'] = time
        if('T' in days):
            if('Th' in days):
                tt['Th'] = time
                if('TWTh' in days or 'TTh' in days):
                    tt['T'] = time
            else:
                tt['T'] = time
        if('W' in days):
            tt['W'] = time
        if('F' in days):
            tt['F'] = time
    return tt
def is_clashing(tt1,tt2):
    days_arr = ['M','T','W','Th','F']
    for day in days_arr:
        if(day in tt1 and day in tt2):
            if(not (tt1[day][0] >= tt2[day][1] or tt2[day][0] >= tt1[day][1])):
                return True
    return False
def get_time_string(course):
    row =  df[df["Course Name/Group Name"].str.contains(course)]
    time_string = []
    if(type(row["Time"].item())==str):
        time_string.append(row["Time"].item())
    if(type(row["Time.1"].item())==str):
        time_string.append(row["Time.1"].item())
    return " ,".join(time_string)
    
def is_not_clashing_with_template(time_str,template):
    if type(time_str)!= str :
        return True
    for courses in template:
        if(is_clashing(time_table(get_time_string(courses)),time_table(time_str))):
            return False
    return True
template = ['MTH204A','MTH301A','MSO201','TA202','PHI147']
df1 = df[df["Time"].apply(is_not_clashing_with_template,args=(template,))].to_excel("ROUNAK.xlsx")

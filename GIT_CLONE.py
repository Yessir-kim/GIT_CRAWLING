import requests
import json
from time import sleep
import datetime
import timeit

"""
    You have to install 'requests' library. Command is as follows.
    --> 'pip install requests' 
"""

def url_make(name, para_set, que_set, date_set):
    idx = -1
    
    for emt in que_set:
        if name in emt:
            idx = que_set.index(emt)
            break
        
    if len(para_set) == 2:
        if idx == -1:
            que_set.append(name + ":" + str(para_set[1]))
        else:
            que_set[idx] = name + ":" + str(para_set[1])
            
        if name == "pushed": # 날짜 기준만 재설정
            if idx == -1:
                date_set[0] = str(len(que_set) - 1)
            else:
                date_set[0] = str(idx)
            if para_set[1][0] == '>':
                date_set[1] = str(para_set[1][1:])
                date_set[2] = str(datetime.date.today())
            else: 
                date_set[2] = str(para_set[1][1:])           
    else:
        if idx == -1:
            que_set.append(name + ":" + str(para_set[1]) + ".." + str(para_set[2])) 
        else:
            que_set[idx] = name + ":" + str(para_set[1]) + ".." + str(para_set[2])
            
        if name == "pushed": # 날짜 기준만 재설정
            if idx == -1:
                date_set[0] = str(len(que_set) - 1)
            else:
                date_set[0] = str(idx)
      
            date_set[1] = str(para_set[1])
            date_set[2] = str(para_set[2])


username = "yeongbin123"
token = "d302d70de2034265895446a2510663d38bd8d97c"

gh_session = requests.Session()
gh_session.auth = (username, token)

# command line

url = "https://api.github.com/search/repositories?q=" # Basic form

print("1. Language\t2. Created\t3. Pushed\t4. Forks\n5. Stars\t6. Sizes\t7. Followers\t8. Topics")

com = input("Input your command that you want to search(Search : 0) : ")
print("")


stand_date = "2008-01-01"
limit_date = str(datetime.date.today())
date_set = ["-1", stand_date, limit_date]
que_set = []

while not com[0] == "0":
    if com[0] == "1": # 이부분 바꿔야함 
        try:
            list_com = com.split(" ")
            url += "language:" + str(list_com[1])
        except:
            print("Check command form")
    elif com[0] == "2":
        try:
            list_com = com.split(" ")
            url_make("created", list_com, que_set, date_set)
        except Exception as es:
            print("Check command form", es)
    elif com[0] == "3":
        try:
            list_com = com.split(" ")
            url_make("pushed", list_com, que_set, date_set)
        except:
            print("Check command form")
    elif com[0] == "4":
        try:
            list_com = com.split(" ")
            url_make("forks", list_com, que_set, date_set)
        except:
            print("Check command form")

    elif com[0] == "5":
        try:
            list_com = com.split(" ")
            url_make("stars", list_com, que_set, date_set)
        except:
            print("Check command form")
    elif com[0] == "6":
        try:
            list_com = com.split(" ")
            url_make("size", list_com, que_set, date_set)
        except:
            print("Check command form")
    elif com[0] == "7":
        try:
            list_com = com.split(" ")
            url_make("followers", list_com, que_set, date_set)
        except:
            print("Check command form")
    elif com[0] == "8":
        try:
            list_com = com.split(" ")
            url_make("topics", list_com, que_set, date_set)
        except:
            print("Check command form")

    print("1. Language\t2. Created\t3. Pushed\t4. Forks\n5. Stars\t6. Sizes\t7. Followers\t8. Topics")

    com = input("Input your command that you want to search(Search : 0) : ")
    print("")
    
page = 1

idx_n = 101

total = 0

flag = 1

page_che = 0 

if date_set[0] == "-1":
    url_make("created", date_set, que_set, date_set)

org_url = url # Org url store

stand_date = date_set[1]

limit_date = date_set[2]

# print(stand_date, limit_date)

start = timeit.default_timer()

while stand_date <= limit_date: # Stand date -> Limit date
    url = org_url 
    
    che = 0 # Count check
    
    for ss in que_set:
        if che != int(date_set[0]): # date_set[0] == Created query
            url += "+" + str(ss)
            
        che += 1 
        
    url += "+" + str(que_set[int(date_set[0])]) + "&per_page=100&page=" # Url create
       
    while idx_n == 101: # Data show 
        set_url = url + str(page) # Pagination
        # print(set_url)
        if page_che % 20 == 0 and page_che != 0: # Limit 30 
            sleep(60)
            page_che = 0 
        
        request = json.loads(gh_session.get(set_url).text) # Use json type to parse
        page_che += 1
        """
        if flag: # Total count check
            print("<Total_count is " + str(request['total_count']) + ">")
            
            flag = 0
        """ 
        idx_n = 1
        # print(stand_date, limit_date)
        
        try:
            for repo in request['items']:
                    print(str(total+idx_n)+" "+repo['html_url'])
     
                    idx_n += 1
        except:
            break
        
        page += 1
        
        total = total + idx_n - 1

    page = 1 # Reset

    idx_n = 101

    flag = 1
    
    bef_date = datetime.datetime.strptime(stand_date, "%Y-%m-%d").date()
    
    aft_date = bef_date + datetime.timedelta(days=1)
            
    que_set[int(date_set[0])] = "created" + ":" + str(bef_date) + "T00:00.." + str(aft_date) + "T00:00"

    stand_date = str(aft_date)

stop = timeit.default_timer()
print("Total_time : " + str((stop - start) / 60))

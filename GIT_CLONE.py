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
            
        if name == "pushed":
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
            
        if name == "pushed":
            if idx == -1:
                date_set[0] = str(len(que_set) - 1)
            else:
                date_set[0] = str(idx)
      
            date_set[1] = str(para_set[1])
            date_set[2] = str(para_set[2])


username = "yeongbin123" # input("Your name here : ")
token = "dfd2fe71b58f73ee77137c659096a89589b27378" # input("Your token here : ")

gh_session = requests.Session()
gh_session.auth = (username, token)

# command line

url = "https://api.github.com/search/repositories?q="

print("1. Language\t2. Created\t3. Pushed\t4. Forks\n5. Stars\t6. Sizes\t7. Followers\t8. Topics")

com = input("Input your command that you want to search(Search : 0) : ")
print("")


stand_date = "2007-01-01"
limit_date = str(datetime.date.today())
date_set = ["-1", stand_date, limit_date]
que_set = []

while not com[0] == "0":
    if com[0] == "1":
        try:
            list_com = com.split(" ")
            url_make("language", list_com, que_set, date_set)
        except:
            print("Check command form")
    elif com[0] == "2":
        try:
            list_com = com.split(" ")
            url_make("created", list_com, que_set, date_set)
        except:
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
    url_make("pushed", date_set, que_set, date_set)

org_url = url # Org url store

stand_date = date_set[1]

limit_date = date_set[2]

start = timeit.default_timer()

total_che = 1

set_date = limit_date

repos_list = []

repos_list = set()

try:
  f = open("output.txt",'w')
except IOError as e:
  print("IOError: {0}".format(e))

while int(total_che) != 0:
    url = org_url 
    
    che = 0 # Count check
    
    for ss in que_set:
        if che != int(date_set[0]): # date_set[0] == pushed query
            url += "+" + str(ss)
            
        che += 1 
        
    url += "+" + str(que_set[int(date_set[0])]) + "&sort=updated&order=desc&per_page=100&page=" # Url create
       
    while idx_n == 101 and page != 11: # Data show 
        set_url = url + str(page) # Pagination
        print(set_url)
        if page_che % 30 == 0 and page_che != 0: # Limit 30 
            sleep(60)
            page_che = 0 
        
        request = json.loads(gh_session.get(set_url).text) # Use json type to parse

        total_che = int(request['total_count'])

        page_che += 1

        idx_n = 1
        
        try:
            for repo in request['items']:
                    rem = len(repos_list)
                    repos_list.add(repo['html_url'])
                    if rem != len(repos_list):
                        f.write(repo['html_url'] + '\n')
                    set_date = repo['pushed_at']
                    idx_n += 1
        except Exception as ee:
            print(ee)
            break
        
        page += 1

    page = 1 # Reset

    idx_n = 101

    flag = 1

    if str(set_date) == limit_date:
        break
    
    if que_set[int(date_set[0])][7] == '<' or que_set[int(date_set[0])][7] == '>':
        que_set[int(date_set[0])] = que_set[int(date_set[0])][:8] + str(set_date)
    else:
        que_set[int(date_set[0])] = que_set[int(date_set[0])][:7] + stand_date + ".." + str(set_date)

    limit_date = str(set_date)

stop = timeit.default_timer()

print("Total_time : " + str((stop - start) / 60))

print("Total_repos_count : " + str(len(repos_list)))

f.close()

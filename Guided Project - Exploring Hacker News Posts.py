#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
f = open("HN_posts_year_to_Sep_26_2016.csv")
hn = list(csv.reader(f))
#print (hn[:5])


# In[2]:


headers = hn[:1]
hn = hn[1:]
#print (headers)
#print (hn[:5])


# In[3]:


ask_posts = []
show_posts = []
other_posts = []

for row in hn:
    title = row[1]
    if title.lower().startswith('ask hn'):
        ask_posts.append(row)
    elif title.lower().startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)

#print(len(ask_posts), len(show_posts), len(other_posts))
#print(len(show_posts))
#print(len(other_posts))


# In[4]:


total_ask_comments = 0
for row in ask_posts:
    total_ask_comments += int(row[4])
avg_ask_comments = total_ask_comments / len(ask_posts)
print (avg_ask_comments)

total_show_comments = 0
for row in show_posts:
    total_show_comments += int(row[4])
avg_show_comments = total_show_comments / len(show_posts)
print (avg_show_comments)


# As we can see, ask posts receive an average of 10.39 comments, while show posts receive 4.89. Therefore, on average, ask posts are more likely to receive comments than show posts. 

# In[5]:


import datetime as dt


# In[6]:


result_list = []

for row in ask_posts:
    result_list.append([row[6], int(row[4])])

counts_by_hour = {}
comments_by_hour = {}

for row in result_list:
    date_dt = dt.datetime.strptime(row[0], "%m/%d/%Y %H:%M")
    date_dt_hour = date_dt.strftime("%H")
    if date_dt_hour not in counts_by_hour:
        counts_by_hour[date_dt_hour] = 1
        comments_by_hour[date_dt_hour] = row[1]
    else:
        counts_by_hour[date_dt_hour] += 1
        comments_by_hour[date_dt_hour] += row[1]

#print (counts_by_hour)
#print (comments_by_hour)


# In[7]:


avg_by_hour = []

for hour in comments_by_hour:
    avg_comm = comments_by_hour[hour] / counts_by_hour[hour]
    avg_by_hour.append([hour,avg_comm ])
    
#print (avg_by_hour)


# In[19]:


from operator import itemgetter
swap_avg_by_hour = []

for row in avg_by_hour:
    swap_avg_by_hour.append([row[1], row[0]])
#print (swap_avg_by_hour)

sorted_swap = sorted(swap_avg_by_hour, key = itemgetter(0), reverse = True)

print (sorted_swap[:5])


# As we can see from the list, the time that is most likely to get a comment is 15, 13, 12 pm, 2, 10 am.

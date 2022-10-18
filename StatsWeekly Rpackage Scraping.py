
#Get proper imports
import time
import requests
from bs4 import BeautifulSoup
import urllib.request
from pprint import pprint
from html_table_parser.parser import HTMLTableParser
from datetime import datetime
#import pandas as pd

#Step 1: Set time and any excluded packages

userdate = input("Enter Cutoff Date, don't want this day or earlier (YEAR-MONTH-DAY):")
print("Cutoff Date: " + userdate)

enddate=datetime.strptime(userdate, '%Y-%m-%d') #date before day you want to run it

userlist = input("Enter Package Exclusions (pack1,pack2,pack3...):")
print("Excluded Packages: " +userlist)
exclude_list=userlist.split(',')

time.sleep(3)
print("Let's GO! \n")
#=========================================================================================================================


#Step 2: Generate list of packages within date timeline

print('Generate list of packages within date timeline \n')
    #Define function
def url_get_contents(url):
    req=urllib.request.Request(url=url)
    f =urllib.request.urlopen(req)
    return f.read()

    #Get contents of CRAN page
xhtml = url_get_contents('https://cran.r-project.org/web/packages/available_packages_by_date.html').decode('utf-8')

    #Define the HTMLTableParser object
p = HTMLTableParser()

    #Feed the html contents in the HTMLTableParser object
p.feed(xhtml)

    #Now finally obtaining the data of the table required
#pprint(p.tables[0][0][0:3])

    #Get only the dates greater than the end date
i_list =range(1,len(p.tables[0]))

pack_list=[]
for i in i_list:
    date=p.tables[0][i][0]
    data=date.replace('\n', ' ')
    package=p.tables[0][i][1]
    package=package.replace('\n', ' ')
    title=p.tables[0][i][2]
    title=title.replace('\n', ' ')
    linedate=datetime.strptime(date, '%Y-%m-%d')
    line =str(date) +'$$$'+ str(package) +'$$$'+ str(title)
    if linedate > enddate:
        pack_list.append(line)
    else:
        break
#=========================================================================================================================


#Step 2: Get links that go with those packages

print('Get links that go with those packages \n')

link_list=[]
main_url="https://cran.r-project.org/"

    #Send request and get links
rm = requests.get('https://cran.r-project.org/web/packages/available_packages_by_date.html')
soupm = BeautifulSoup(rm.content, 'html.parser')
links = soupm.findAll('a')

for i in range(1,len(pack_list)+1):
    n=i-1
    add_url=str(links[n].get('href')).strip("../../")
    full_url= main_url + add_url
    link_list.append(full_url)
#=========================================================================================================================


#Step 3: Combine the lists

print('Combine the lists \n')

full_list=[]

for i in range(0,len(pack_list)):
    date,package,title=pack_list[i].split('$$$')
    link=link_list[i]
    full_list.append([package,date,title,link])
#=========================================================================================================================


#Step 4: Go through each item in the list and open the link to scrape

print('Go through each item in the list and open the link to scrape \n')
    
new_list=[]
old_list=[]
count=0

for item in full_list:
    count+=1
    new=True
    package=item[0]
    date=item[1]
    title=item[2]
    link=item[3]
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    intlink_list=[] #internal links within that page
    for i in soup.find_all('a'):
        intlink_list.append(i.get('href'))
    for j in intlink_list:
        if "/Archive/" in j:
            new=False
    if new:
        new_list.append(date +'\t'+ package +'\t'+ title +'\t'+ link)
    else:
        old_list.append(date +'\t'+ package +'\t'+ title +'\t'+ link)
    if count%10==0:
        print('\t' + str(count) +'/'+ str(len(full_list)) + ' done')
#Step 5: Print out packages by list

print('Print out packages by \n \n \n')

exclude_list2=[]

print("Updated Packages")
print('============================================================================================')
for i in old_list:
    print(i)
print('============================================================================================')
print('\n \n')


print("New Packages")
print('============================================================================================')
for i in new_list:
    package=i.split('\t')[0]
    if package not in exclude_list:
        print(i)
    else:
        exclude_list2.append(i)
print('============================================================================================')
print('\n \n')

print("Overlapped Packages")
print('============================================================================================')
for i in exclude_list2:
    print(i)


        
        
            



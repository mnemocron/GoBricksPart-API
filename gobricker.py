# -*- coding: utf-8 -*-
# open this file in SPYDER
import csv

# part numbers and categories from 
# https://rebrickable.com/downloads
# 38635 total parts
# -> remove unwanted parts that are not bricks (e.g. minifigures, stickers, motors)
# -> remove sub-parts (part number must be numeric e.g. 4070 instead of 4070a)
# 3272 remaining parts

# category_filter = [1,3,5,6,7,8,9,11,12,14,15,16,18,19,20,21,22,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,44,45,46,47,49,51,52,53,54,55,56,59,60,61,65,67]
category_filter = [3,5,6,7,8,9,11,12,14,15,16,18,19,20,21,22,23,25,27,28,29,30,32,37,40,46,47,49,51,52,53,54,55,67]

with open('parts.csv', mode='r', encoding="utf8") as infile:
    reader = csv.reader(infile)
    # [0] = part number / [2] = category
    mydict = [[rows[0],rows[2]] for rows in reader]
    # mylist = [row[0] for row in mydict[1:] if int(row[1]) in category_filter and row[0].isnumeric()]
    mylist = [row[0] for row in mydict[1:] if int(row[1]) in category_filter ]


# create payload for gobricks.cn API
partlist = []
for number in mylist:
    part = {}
    part['color_type'] = 'ldr'
    part['colorid'] = '0'   # color 0 = black
    part['designid'] = number
    part['quantity'] = 1
    partlist.append(part)

payload = {}
payload['testList'] = partlist

#%%
import requests					# requesting webpages
import json

headers = {
    'Host':'gobricks.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Accept':'application/json',
    'Accept-Language':'en-US,en;q=0.5',
    'Accept-Encoding':'gzip, deflate, br',
    'Content-Type':'application/json;charset=utf-8',
#    'Content-Length':'242615',
    'Origin':'https://gobricks.cn',
    'DNT':'1',
    'Connection':'keep-alive',
    'Referer':'https://gobricks.cn/'
}

# API URL
# POST request using JSON as payload data
url = 'https://gobricks.cn/frontend/v1/community/lego2ItemList'
response = requests.post(url, headers=headers, json=payload)
print(response.status_code)  # must return 200
partlist = json.loads(response.text)

#%%
# some parts are available "itemList"
# some parts are not in stock "inventoryDeficiency"
# some parts do not exist in the requested color "colorDeficiency"
# some parts do not exist at all "missList"
# some parts are on a no sell list ?? "noSellList"
hitlist = partlist['colorDeficiency'][:]
hitlist.extend(partlist['inventoryDeficiency'][:])
hitlist.extend(partlist['itemList'][:])
# 973 parts total on hitlist

# find the LEGO ID and GoBrick ID
for item in hitlist:
    ldd = item['designid']
    # gob = item['info']['id'][0:-4] # remove color info GDS-1232-080  ==> GDS-1232
    gob = '-'.join( item['info']['id'].split('-')[0:2] ) # GDS-612-080-DE01
    # print(ldd, ' ', gob)


#%% OUTPUT THE FULL CONVERSION TABLE
with open('gobrick_conversion_table.csv', newline='', mode='w') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    for item in hitlist:
        ldd = item['designid']
        gob = item['info']['id'][0:-4]   
        gob = '-'.join( item['info']['id'].split('-')[0:2] ) # GDS-612-080-DE01
        writer.writerow([ldd, gob])

#%% OUTPUT THE RAW JSON FILE
with open('api_request_raw.json', 'w') as outfile:
    json.dump(partlist, outfile, sort_keys=True, indent=4)




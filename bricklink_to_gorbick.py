# -*- coding: utf-8 -*-

import csv

# https://swooshable.com/parts/colors
# https://customizeminifiguresintelligence.wordpress.com/2020/07/27/gobricks-the-foxconn-of-china-clone-bricks/
colors = {}
with open('color_table.csv', mode='r', encoding="utf8") as infile:
    reader = csv.reader(infile)
    next(reader, None)  # skip the headers
    for row in reader:
        colors[row[1]] = row[2]
        
parts = {}
with open('gobrick_conversion_table.csv', mode='r', encoding="utf8") as infile:
    reader = csv.reader(infile)
    next(reader, None)  # skip the headers
    for row in reader:
        parts[row[0]] = row[1]

#%%
with open('bom.csv', mode='r', encoding="utf8") as infile, open('bom_gobricks.csv', mode='w', newline='', encoding='utf8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    # writer.writerow(['\u96f6\u4ef6\u7f16\u53f7', '\u989c\u8272\u7f16\u53f7', '\u6570\u91cf'])
    next(reader, None)  # skip the headers
    for row in reader:
        part = row[1]
        color = row[2]
        if(part in parts) and (color in colors):
            part = parts[part]
            color = colors[color]
            # print(part, color)
        elif(part in parts):
            part = parts[part]
#            print(part, color)
#        else:
#            print(part, color)
        if(len(row[2]) > 0):
            writer.writerow([ part+ '\t'+color.zfill(3) + '\t'+ row[2] ])
        else:
            print(part)
    





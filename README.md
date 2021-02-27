# GoBricksPart-API
API and conversion table of Gobricks vs. LEGO® part ID numbers using gobricks backend API

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/cc-0.svg)](https://forthebadge.com)

---

This iPython Script uses the brick database from [rebrickable.com](https://rebrickable.com/downloads/) to determine real LEGO® ID part numbers (ca. 30'000 items).
The part numbers are filtered by category (e.g. no sticker sheets, Duplo® etc.).
The filtered parts (ca. 11'000 items) are then sent to the [gobricks.cn](https://gobricks.cn) backend API to get a result **if** gobricks offers a compatible clone part and what Gobricks item number is.

---

### Part Lists

- [./gobrick_conversion_table.csv](./gobrick_conversion_table.csv)

---

### Convert Bricklink to BOM

- pick a set
- export set inventory to new Wanted List
    + click "part out"
    + create new Wanted List
- download the Wanted List as `.xml` file
- open the `.xml` file with Microsoft Excel
- save the table as `bom.csv`
- run the `bricklink_to_gobrick.py`
- open the `bom_gobricks.csv` with a text editor
- select all + copy
- open the template `gds-list.xml` from gobricks in Microsoft Excel
- paste the csv values in the table, save
- upload to gobricks.cn toolkit

---

### Gobricks API Documentation

(inofficial / reverse engineered)

See the `./raw` directory for the raw JSON output from the API.

```python
import requests
import json

partlist = ['10884', '2417']
for number in mylist:
    part = {}
    part['color_type'] = 'ldr'
    part['colorid'] = '0'   # color 0 = black
    part['designid'] = number
    part['quantity'] = 1
    partlist.append(part)

payload = {}
payload['testList'] = partlist

headers = {
    'Host':'gobricks.cn',
# fill in full request headers
    'Referer':'https://gobricks.cn/'
}

url = 'https://gobricks.cn/frontend/v1/community/lego2ItemList'
response = requests.post(url, headers=headers, json=payload)
print(response.status_code)  # must return 200
partlist = json.loads(response.text)
```












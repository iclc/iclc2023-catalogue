import csv
import unicodedata
from io import StringIO
from slugify import slugify
import yaml
import os
import re

"""
Video: prog_note
Paper: abstract
Workshop: abstract, prog_note
Performace: abastract, prog_note
"""

EXPORT_MAIL = True

BASIC_TYPES = {
    "Performance": "performance",
    "Paper-Long": "paper",
    "Paper-Short": "paper",
    "Community-Written": "paper",
    "Workshop": "workshop",
    "Community-Video": "video",
    "Video-Long": "video",
    "Video-Short": "video"
}

FOLDERS = ["performance", "person", "workshop", "video", "paper", "secret"]

def make_slug(input):
    return slugify(input, True, True, True, 64, True)

def clean_cell(cell):
    if cell.strip() == "NULL": cell = ""
    return unicodedata.normalize("NFC", cell.strip()).replace("\r", "")

def clean_text(cell):
    return re.sub(' +', ' ', cell)

def read_as_clean_dict(data):
    ret = []
    csvRows = csv.reader(StringIO(data))

    # clean up cell content
    csvRows = list(map(lambda row : list(map(clean_cell, row)), csvRows))

    keys = csvRows[0]

    csvRows = csvRows[1:]

    # build a dictionary out of it
    for row in csvRows:

        if row[0] == "": continue # if slug is empty then skip row
        
        entry = {}
        for i in range(len(keys)):
            entry[keys[i]] = row[i]

        ret.append(entry)
    
    return ret

with open('authors.csv', 'r') as file:
    authors_string = file.read()

with open('items.csv', 'r') as file:
    items_string = file.read()

authors = read_as_clean_dict(authors_string)
items = read_as_clean_dict(items_string)

for author in authors:
    # re-slugify slugs to make sure all is consistent
    author["slug"] = make_slug(author["slug"])

    # cleanup and split affilations
    if author["organizations"] == "NULL": author["organizations"] = ""

    if author["organizations"] == "":
        author["affiliations"] = []
    else:
        author["affiliations"] = list(map(clean_cell, author["organizations"].split(";")))

# build a dict to lookup authors
author_by_slug = {}
for author in authors:
    author_by_slug[author["slug"]] = author

for item in items:
    item["slug"] = make_slug(item["title"])
    if item["slug"] == "": item["slug"] = "___" # special case for [_ _ _]

    # make a list of authors
    author_list = [item["author_1_slug"], item["author_2_slug"], item["author_3_slug"],
                   item["author_4_slug"], item["author_5_slug"], item["author_6_slug"],
                   item["author_7_slug"], item["author_8_slug"], item["author_9_slug"],
                   item["author_10_slug"], item["author_11_slug"]]
    author_list = map(make_slug, author_list)

    item["authors"] = list(filter(lambda x: x != "", author_list))

    item["type"] = BASIC_TYPES[item["committee"]]

    # let's check if all authors in items can be mapped to authors
    for author in item["authors"]:
        if not author in author_by_slug:
            print("Author not found: " + author)
        else:
            author_by_slug[author]["has_item"] = True

# let's also check if we have an author without item
for author in authors:
    if not "has_item" in author:
        print("Author has no item:" + author["slug"])

# create folders
for folder in FOLDERS:
    path = 'output/' + folder
    if not os.path.exists(path):
        os.makedirs(path)

emails = {}

# let's render authors/persons
for author in authors:
    data = {
        "slug": author["slug"],
        "type": "person",
        "last_name": author["last_name"],
        "first_name": author["first_name"],
        "alias": None,
        "affiliations": author["affiliations"]
    }

    if EXPORT_MAIL:
        emails[author["slug"]] = author["email"]
   
    data_yaml = yaml.dump(data, allow_unicode=True, sort_keys=False)

    body = clean_text(author["bio"])
    
    out_string = "---\n" + data_yaml + "---\n\n" + body
    
    with open("output/person/" + author["slug"] + ".md", "w", encoding="utf-8") as f:
        f.write(out_string)

# let's render items
for item in items:
    data = {
        "slug": item["slug"],
        "title": item["title"],
        "type": item["type"],
        "submission_type": item["committee"],
        "contributors": list(map(lambda x: {"person": "$" + x}, item["authors"])),
    }
    
    data_yaml = yaml.dump(data, allow_unicode=True, sort_keys=False)

    item["abstract"] = clean_text(item["abstract"])
    item["prog_note"] = clean_text(item["prog_note"])

    if item["prog_note"] == "": item["prog_note"] = "(...)"
    if item["abstract"] == "": item["abstract"] = "(...)"

    if item["type"] == "video":
        body = "# $PROGRAM_NOTE\n\n" + item["prog_note"]
    elif item["type"] == "paper":
        body = "# $ABSTRACT\n\n" + item["abstract"]
    else:
        body = "# $PROGRAM_NOTE\n\n" + item["prog_note"] + "\n\n# $ABSTRACT\n\n" + item["abstract"]

    out_string = "---\n" + data_yaml + "---\n\n" + body

    with open("output/" + item["type"] + "/" +item["submission_id"] + "_" + item["slug"] + ".md", "w", encoding="utf-8") as f:
        f.write(out_string)

if EXPORT_MAIL:
    emails_yaml = yaml.dump(emails, allow_unicode=True, sort_keys=False)

    with open("output/secret/emails.yaml", "w", encoding="utf-8") as f:
        f.write(emails_yaml)
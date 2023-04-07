import csv
import unicodedata
from io import StringIO
import yaml
import os

EXPORT_MAIL = False

store = {}
emails = {}

if EXPORT_MAIL:
    with open("data/secret/emails.yaml", 'r') as file:
        emails = yaml.safe_load(file.read())


def sanitize_time(time):
    if time.startswith("t"):
        return time[1:]
    else:
        return time

def render_name(person, use_alias=True):
    ret = person["first_name"] + " " + person["last_name"]
    if use_alias and person.get("alias", None):
        ret = f"{ret} ({person['alias']})"
    
    if EXPORT_MAIL:
        email = emails.get(person['slug'])
        if email:
            ret = f"{ret}&nbsp;&lt;{email}&gt;"
    
    return ret.replace(" ", "&nbsp;")

def load_md(path):
    with open(path, 'r') as file:
        data = file.read()
    yaml_data = data.split("---")[1]
    body = "---".join(data.split("---")[2:])
    obj = yaml.safe_load(yaml_data)
    obj["body"] = body


    if obj["type"] == "event":
        for item in obj["schedule"]:
            item["time"] = sanitize_time(item["time"])

    store[obj["slug"]] = obj

# load all data
for root, dirs, files in os.walk("data"):
    for file in files:
        if file.endswith('.md'):
            load_md(root + "/" + file)


def master_schedule_event(slug):
    print("Master Schedule - processing: " + slug)
    event = store[slug]
    c = ""

    venue = ""
    if event['venue']:
        venue = f", <em>{event['venue']}</em>"

    c = c + f"<tr><td colspan='3'><h3>{event['title']}</h3>\n{event['date_time']}{venue}</td></tr>"
    for item in event["schedule"]:
        title = item['item']
        authors = ""
    
        item_venue = ""

        if title.startswith("$"):
            obj = store[title[1:]]
            
            if item.get("venue", None):
                item_venue = f"<br><br><span style='position:relative;top:-10px;'>Venue: <em>{item['venue']}</em></span>"
            
            title = f"<em>{obj['title']}</em>"

            if obj["type"] == "video":
                item_venue = "<br><br><span style='position:relative;top:-10px;'>(Video Screening)</span>"

            for contributor in obj["contributors"]:
                if authors != "":
                    authors += "<br>"
                
                if contributor["person"].startswith("$"):
                    author = store[contributor["person"][1:]]
                    authors += render_name(author)
                else:
                    authors += contributor["person"]
        else:
            title = f"{title}"
        
        c = c + f"<tr><td>{item['time']}</td><td><strong>{title}</strong>{item_venue}</td><td>{authors}</td></tr>\n"

        if item.get("visuals", None):
            vis = store[item["visuals"][1:]]
            vis_cont = vis["contributors"][0]["person"][1:]
            vis_person = store[vis_cont]
            vis_auth = render_name(vis_person)

            c = c + f"<tr style='position:relative;top:-12px;'><td></td><td>Visuals: <strong><em>{vis['title']}</em></strong>{item_venue}</td><td>{vis_auth}</td></tr>\n"


    c = c + "<tr><td style='padding-bottom: 50px;'></td></tr>\n"
    return c

def render_master_schedule():
    c = ""

    for item in store["__master"]["schedule"]:
        if type(item) == str:
            if not item.startswith("$"):
                c = c + f"<tr><td colspan='3'><h2>{item}</h2></td></tr>"
            else:
                c = c + master_schedule_event(item[1:])
        else:
            venue = item.get('venue')

            if venue == None:
                venue = ""
            else:
                venue = "<br><br><span style='position:relative;top:-10px;'>Venue: <em>" + venue + "</em></span>"

            c = c + f"<tr><td style='padding-bottom: 50px;'>{sanitize_time(item['time'])}</td><td colspan='2'><strong>{item['title']}</strong>{venue}</td></tr>"
    
    with open("templates/master.html", "r") as file:
        master_template = file.read()

    with open("output/master-schedule.html", "w") as file:
        file.write(master_template.replace("<!--CONTENT-->", c))

render_master_schedule()
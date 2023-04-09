from io import StringIO
import yaml
import os
import random
from datetime import datetime
import markdown


EXPORT_MAIL = False
MASTER_SCHEDULE_DO_HIDE = True
CAT_OUT_PATH = 'output/2023/catalogue/'

TYPES = {
    "keynote": "Keynote",
    "event": "Event",
    "person": "Person",
    "Performance": "Performance",
    "Paper-Long": "Paper",
    "Paper-Short": "Paper",
    "Community-Written": "Community Report (Paper)",
    "Workshop": "Workshop",
    "Community-Video": "Community Report (Video)",
    "Video-Long": "Video",
    "Video-Short": "Video"
}

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

def link_item(item, to, what):
    if not to.get(what): to[what] = []
    to[what].append(item)

# link entries (person -> contribution, etc.)
for slug in store.keys():
    item = store[slug]
    if item.get("contributors"):
        for contributor in item["contributors"]:
            person = contributor["person"]
            if person.startswith("$"):
                link_item(item, store[person[1:]], "contributions")

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
        time = item['time']

        if item.get('hide_time'):
            time = ""
    
        item_venue = ""

        if item.get('hidden') and MASTER_SCHEDULE_DO_HIDE:
            continue

        if title.startswith("$"):
            obj = store[title[1:]]
            
            if item.get("venue", None) and MASTER_SCHEDULE_DO_HIDE:
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

        
        c = c + f"<tr><td>{time}</td><td><strong>{title}</strong>{item_venue}</td><td>{authors}</td></tr>\n"

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
            if item.get('hidden') and MASTER_SCHEDULE_DO_HIDE:
                continue

            venue = item.get('venue')

            if venue == None:
                venue = ""
            else:
                venue = "<br><br><span style='position:relative;top:-10px;'>Venue: <em>" + venue + "</em></span>"

            c = c + f"<tr><td style='padding-bottom: 50px;'>{sanitize_time(item['time'])}</td><td colspan='2'><strong>{item['title']}</strong>{venue}</td></tr>"
    
    with open("templates/master.html", "r") as file:
        master_template = file.read()

    master_content = master_template.replace("$CONTENT", c)
    now = datetime.now()
    master_content = master_content.replace("$VERSION", now.strftime('%d.%m.%Y'))

    with open("output/master-schedule.html", "w") as file:
        file.write(master_content)

render_master_schedule()


# ---
# *** CATALOUGE
# ---


if not os.path.exists(CAT_OUT_PATH): os.makedirs(CAT_OUT_PATH)

with open("templates/catalogue.html", "r") as file:
    cat_template = file.read()

cat_template = cat_template.replace("$CACHEBUST", str(random.randint(10000, 99999)))

# prepare folders for output
for folder in ["performance", "person", "workshop", "video", "paper", "keynote", "event"]:
    path = CAT_OUT_PATH + folder + "/"
    if not os.path.exists(path):
        os.makedirs(path)

def write_cat_html(path, title, content):
    html = cat_template
    html = html.replace("$TITLE", title)
    html = html.replace("$MAINCONTENT", content)
    with open(path, "w") as file:
        file.write(html)
    print("Wrote: " + path)

def url_for_item(item):
    return item["type"] + "/" + item["slug"] + ".html"

def path_for_item(item):
    return CAT_OUT_PATH + url_for_item(item)

def title_for_item(item, include_type=False):
    ret = ""
    pre = ""
    if include_type:
        pre = type_description_for_item(item) + ": "
    
    if item["type"] == "person": ret = render_name(item)
    else: ret = item["title"]

    return pre + ret

def link_to_item(text, item):
    return f"<a href='{url_for_item(item)}'>{text}</a>"

def transform_body(md):
    return markdown.markdown(md)

def content_for_person(item):
    affiliations = ""
    num_affiliations = len(item["affiliations"])
    if num_affiliations == 1:
        affiliations = f"<p>Affiliation: <strong>{item['affiliations'][0]}</strong></p>"
    if num_affiliations > 1:
        affiliations = "<p style='margin-bottom: 5px'>Affiliations:</p><ul>"
        for affiliation in item["affiliations"]:
            affiliations += f"<li><strong>{affiliation}</strong></li>"
        affiliations += "</ul>"

    contributions = "<p style='margin-bottom: 5px'>Contributions:</p><ul>"
    for contribution in item["contributions"]:
        contributions += "<li><strong>" + link_to_item(title_for_item(contribution, True), contribution) + "</strong></li>"
    contributions += "</ul>"

    return f"""
        {affiliations}
        {contributions}
        <h4 style="margin-top: 35px;">Biography</h4>
        {transform_body(item["body"])}
    """

def type_description_for_item(item):
    t = item.get("submission_type")
    if not t: t = item.get("type")
    return TYPES[t]

def content_for_item(item):
    if item["type"] == "person": return content_for_person(item)
    return "<h2>No Content</h2>"

def render_item(item):
    if not item["type"] == "master":
        write_cat_html(path_for_item(item), title_for_item(item), content_for_item(item))

for slug in store.keys():
    render_item(store[slug])
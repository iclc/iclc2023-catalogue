from io import StringIO
import yaml
import os
import random
from datetime import datetime
import markdown
import unicodedata


EXPORT_MAIL = False
MASTER_SCHEDULE_DO_HIDE = True
CAL_FOLDER = "catalogue/"
CAT_OUT_PATH = 'output/2023/' + CAL_FOLDER
PROOF_INCLUDE_ABSTRACTS = True

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

now = datetime.now()


# prepare folders for output
for folder in ["performance", "person", "workshop", "video", "paper", "keynote", "event"]:
    path = CAT_OUT_PATH + folder + "/"
    if not os.path.exists(path):
        os.makedirs(path)


if EXPORT_MAIL:
    with open("data/secret/emails.yaml", 'r') as file:
        emails = yaml.safe_load(file.read())


def clean_cell(cell):
    if cell.strip() == "NULL": cell = ""
    return unicodedata.normalize("NFC", cell.strip()).replace("\r", "")


def sanitize_time(time):
    if time.startswith("t"):
        return time[1:]
    else:
        return time

def url_for_item(item):
    return CAL_FOLDER + item["type"] + "/" + item["slug"] + ".html"

def path_for_item(item):
    return CAT_OUT_PATH + item["type"] + "/" + item["slug"] + ".html"

def render_name(person, use_alias=True, reverse=False, alias_only=False):
    ret = person["first_name"] + " " + person["last_name"]

    if reverse:
        ret = "<strong>" + person["last_name"] + "</strong>, " + person["first_name"]

    if use_alias and person.get("alias", None):
        ret = f"{ret} ({person['alias']})"

    if alias_only:
        ret = person['alias']
    
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
        if file.endswith('.md') and not "__unused" in root:
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
    
    if item.get("schedule"):
        for schedule_item in item["schedule"]:
            if type(schedule_item) == str: continue
            if schedule_item.get('item'):
                if schedule_item['item'].startswith("$"):
                    store[schedule_item['item'][1:]]["event"] = item
                if schedule_item.get('visuals'):
                    store[schedule_item['visuals'][1:]]["event"] = item

def render_schedule(event, do_hide=True, do_link=True):
    c = ""

    for item in event["schedule"]:
        title = item['item']
        authors = ""
        time = item['time']

        if item.get('hide_time'):
            time = ""
    
        item_venue = ""

        if item.get('hidden') and do_hide:
            continue

        if title.startswith("$"):
            obj = store[title[1:]]
            
            if item.get("venue", None) and do_hide:
                item_venue = f"<br><br><span style='position:relative;top:-10px;'>Venue: <em>{item['venue']}</em></span>"
            
            title = f"<em>{obj['title']}</em>"

            if do_link:
                title = link_to_item(title, obj)

            if obj["type"] == "video":
                item_venue = "<br><br><span style='position:relative;top:-10px;'>(Video Screening)</span>"

            for contributor in obj["contributors"]:
                if authors != "":
                    authors += "<br>"
                
                if contributor["person"].startswith("$"):
                    author = store[contributor["person"][1:]]

                    author_text = render_name(author, True, False, item.get("alias_only"))

                    if do_link:
                        author_text = link_to_item(author_text, author)

                    authors += author_text
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

            vis_title = vis['title']

            if do_link:
                vis_title = link_to_item(vis_title, vis)
                vis_auth = link_to_item(vis_auth, vis_person)

            c = c + f"<tr style='position:relative;top:-12px;'><td></td><td>Visuals: <strong><em>{vis_title}</em></strong>{item_venue}</td><td>{vis_auth}</td></tr>\n"
        
    return c

def master_schedule_event(slug):
    print("Master Schedule - processing: " + slug)
    event = store[slug]
    c = ""

    venue = ""
    if event['venue']:
        venue = f", <em>{event['venue']}</em>"

    c = c + f"<tr><td colspan='3'><h3>{event['title']}</h3>\n{event['date_time']}{venue}</td></tr>"

    c = c + render_schedule(event, MASTER_SCHEDULE_DO_HIDE, False)

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
    master_content = master_content.replace("$VERSION", now.strftime('%d.%m.%Y'))

    with open("output/master-schedule.html", "w") as file:
        file.write(master_content)

render_master_schedule()


# ---
# *** Render Status OVerview
# ---

with open("templates/status.html", "r") as file:
    status_template = file.read()

def render_status_overview():
    c = ""
    entries = []
    for slug in store.keys():
        entry = store[slug]
        if entry["type"] != "master":
            title = ""
            if entry["type"] == "person":
                title = render_name(entry)
            else:
                title = entry["title"]

            entries.append([entry["type"], slug, title, entry.get("status", "n/a"), entry])
    
    entries.sort(key=lambda x: (x[0] + x[1]).lower())


    for entry in entries:
        color = "#ff80ff"
        if entry[3] == "n/a": color = "white"
        if entry[3] == "proof": color = "#FFD580"
        if entry[3] == "ready": color = "#7CFC00"

        url = url_for_item(entry[4])

        c += f"<tr style='background-color: {color};'><td>{entry[0]}</td><td>{entry[1]}</td><td><a href='../{url}'>{entry[2]}</a></td><td><strong>{entry[3]}</strong></tr>\n"

    with open("output/2023/catalogue/status-overview.html", "w") as file:
        file.write(status_template.replace("$CONTENT", c).replace("$VERSION", now.strftime('%d.%m.%Y')))

render_status_overview()    

# ---
# *** CATALOUGE
# ---


if not os.path.exists(CAT_OUT_PATH): os.makedirs(CAT_OUT_PATH)

with open("templates/catalogue.html", "r") as file:
    cat_template = file.read()

cat_template = cat_template.replace("$CACHEBUST", str(random.randint(10000, 99999)))

def write_cat_html(path, title, content):
    html = cat_template
    html = html.replace("$TITLE", title)
    html = html.replace("$MAINCONTENT", content)
    html = html.replace("$PATH", path.replace(CAT_OUT_PATH, ""))

    with open(path, "w") as file:
        file.write(html)
    print("Wrote: " + path)

def title_for_item(item, include_type=False):
    ret = ""
    post = ""
    if include_type:
        post = " (" + type_description_for_item(item) + ")"
    
    if item["type"] == "person": ret = render_name(item)
    else: ret = item["title"]

    return ret + post

def link_to_item(text, item):
    return f"<a href='{url_for_item(item)}'>{text}</a>"

def transform_body(md):
    return markdown.markdown(md, extensions=['footnotes'])

def get_body_chunk(body, chunk):
    tokens = body.split(chunk)
    if len(tokens) == 1: return body
    token = tokens[1]
    return clean_cell(token.split("# $")[0])


def content_for_person(item):
    affiliations = ""
    num_affiliations = len(item["affiliations"])
    if num_affiliations == 1:
        affiliations = f"<p>Affiliation: <strong>{item['affiliations'][0]}</strong></p>"
    if num_affiliations > 1:
        affiliations = "<p class='list-header'>Affiliations:</p><ul>"
        for affiliation in item["affiliations"]:
            affiliations += f"<li><strong>{affiliation}</strong></li>"
        affiliations += "</ul>"

    contributions = "<p class='list-header'>Contributions:</p><ul>"
    for contribution in item["contributions"]:
        contributions += "<li><strong>" + link_to_item(title_for_item(contribution, True), contribution) + "</strong></li>"
    contributions += "</ul>"

    return f"""
        {affiliations}
        {contributions}
        <h4>Biography</h4>
        {transform_body(item["body"])}
    """

def build_contributors_list(item, seperator=", "):
    contributors = ""
    for contributor in item["contributors"]:
        if contributors != "": contributors += ", "
        person = contributor["person"]
        if person.startswith("$"):
            person = store[person[1:]]
            contributors += link_to_item(render_name(person), person)
        else:
            contributors += person
    
    return contributors

def render_event_info(event, display_venue=True):
    venue = ", <em>" + event['venue'] + "</em>"
    if not display_venue: venue = ""

    event_text = f"""
        <strong>{event['title']}</strong><br>
        {event['date_time']}{venue}
    """
    return link_to_item(event_text, event)

def render_associated_event(item):
    if not item.get("event"): return ""
    event = item["event"]
    return render_event_info(event)

proof_abstract_disclaimer = "<p><em><br>The abstract is displayed here for proof-reading and will only be part of the published proceedings, not of the final version of this web catalogue.</em></p>"

def content_for_performance(item):
    body = get_body_chunk(item["body"], "$PROGRAM_NOTE")

    proof_abstract = ""
    if PROOF_INCLUDE_ABSTRACTS:
        proof_abstract += "<h4>Abstract</h4>"
        proof_abstract += proof_abstract_disclaimer
        proof_abstract += transform_body(get_body_chunk(item["body"], "$ABSTRACT"))

    return f"""
        <p><strong>{build_contributors_list(item, ", ")}</strong></p>
        <p class="list-header">Will be performed at:</p>
        <ul>
            <li>{render_associated_event(item)}</li>
        </ul>
        <h4>Program Notes</h4>
        {transform_body(body)}
        {proof_abstract}
    """

def content_for_paper(item):
    body = get_body_chunk(item["body"], "$ABSTRACT")

    return f"""
        <p><strong>{build_contributors_list(item, ", ")}</strong></p>
        <p class="list-header">Will be presented at:</p>
        <ul>
            <li>{render_associated_event(item)}</li>
        </ul>
        <h4>Abstract</h4>
        {transform_body(body)}
    """

def content_for_keynote(item):
    body = item["body"]

    return f"""
        <p><strong>{build_contributors_list(item, ", ")}</strong></p>
        <p><em>Put time/place here</em></p>
        {transform_body(body)}
    """

def content_for_workshop(item):
    body = get_body_chunk(item["body"], "$PROGRAM_NOTE")

    proof_abstract = ""
    if PROOF_INCLUDE_ABSTRACTS:
        proof_abstract += "<h4>Abstract</h4>"
        proof_abstract += proof_abstract_disclaimer
        proof_abstract += transform_body(get_body_chunk(item["body"], "$ABSTRACT"))

    return f"""
        <p><strong>{build_contributors_list(item, ", ")}</strong></p>
        <p><em>Put time/place here</em></p>
        {transform_body(body)}
        <p><em>Put requirements here (???)</em></p>
        {proof_abstract}
    """

def content_for_video(item):
    body = get_body_chunk(item["body"], "$PROGRAM_NOTE")

    return f"""
        <p><strong>{build_contributors_list(item, ", ")}</strong></p>
        <p><em>Still put video-related info here + the video of course ...</em></p>
        <h4>Description</h4>
        {transform_body(body)}
    """

def content_for_event(item):
    body = item["body"]

    schedule = render_schedule(item, True, True)
    schedule = f"<table>{schedule}</table>"

    schedule_title = "Schedule"
    if item["event_type"] == "Concert": schedule_title = "Line-Up"

    return f"""
        <p><strong>{item["date_time"]}<br>
        Venue: <em>{item["venue"]}</em></strong></p>
        {transform_body(body)}
        <h4>{schedule_title}</h4>
        {schedule}
    """

def type_description_for_item(item):
    t = item.get("submission_type")
    if not t: t = item.get("type")
    return TYPES[t]

def content_for_item(item):
    if item["type"] == "person": return content_for_person(item)
    if item["type"] == "performance": return content_for_performance(item)
    if item["type"] == "paper": return content_for_paper(item)
    if item["type"] == "keynote": return content_for_keynote(item)
    if item["type"] == "workshop": return content_for_workshop(item)
    if item["type"] == "event": return content_for_event(item)
    if item["type"] == "video": return content_for_video(item)


    return "<h2>No Content</h2>"

def render_item(item):
    if not item["type"] == "master":
        write_cat_html(path_for_item(item), title_for_item(item), content_for_item(item))

for slug in store.keys():
    render_item(store[slug])


# CATALOGUE INDEX

with open("templates/catalogue-index.html", "r") as file:
    cat_index_template = file.read()

def render_event_list(title, list):
    ret = ""
    ret += "<h4>" + title + "</h4>\n"
    ret += "<ul>\n"
    for slug in list:
        ret += "<li>"
        ret += render_event_info(store[slug], False)
        ret += "</li>"
    ret += "</ul>\n"
    return ret

def render_catalogue_index():
    c = ""

    c += "<p>Todo: Add Keynotes, Workshops and finally also videos. Also do a more sensible overview of papers and community reports.</p>"

    c += render_event_list("Paper Presentations", ["paper-session-1", "paper-session-2", "paper-session-3", "paper-session-4", "paper-session-5"])

    c += render_event_list("Community Reports", ["community-session-1", "community-session-2"])

    c += render_event_list("Concerts", ["choreographic-coding", "lunch-concert-1", "alternative-algorithms", "lunch-concert-2", "immersed-in-code", "algorave", "hybrid-acoustics"])

    c += "<br><br><h3>Contributor Overview</h3>\n"

    persons = []
    for slug in store.keys():
        if store[slug]["type"] == "person":
            persons.append([render_name(store[slug], True, True), slug])
    
    persons.sort(key=lambda x: x[0].lower())

    c += "<ul>"
    for person in persons:
        c += "<li>" + link_to_item(person[0], store[person[1]]) + "</li>"
    c += "</ul>"

    with open(CAT_OUT_PATH + "index.html", "w") as file:
        file.write(cat_index_template.replace("$MAINCONTENT", c))


render_catalogue_index()
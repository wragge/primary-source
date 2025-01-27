import os
import requests
from pyzotero import zotero
from dotenv import load_dotenv

load_dotenv()

discourse_api_key = os.getenv("discourse_api_key")
discourse_user = os.getenv("discourse_user")
zotero_api_key = os.getenv("zotero_api_key")

categories = [
    {
        "label": "collection news",
        "discourse_id": 6,
        "zotero_id": "2IGITA58"
    },
    {
        "label": "useful resources",
        "discourse_id": 11,
        "zotero_id": "NNDNJBQM"
    },
    {
        "label": "research updates",
        "discourse_id": 9,
        "zotero_id": "ZZCJ7MCG"
    }
]

headers = {
    "Api-Key": discourse_api_key,
    "Api-Username": discourse_user
}

zot = zotero.Zotero(5835691, "group", zotero_api_key)

def find_notes(items, item_id):
    notes = []
    for item in items:
        data = item["data"]
        parent_id = data.get("parentItem")
        if parent_id == item_id and data["itemType"] == "note":
            notes.append(data["note"])
    return notes

for category in categories:
    items = zot.collection_items(category["zotero_id"], tag="-added")
    for item in [i for i in items if i["data"]["itemType"] != "note"]:
        zot_data = item["data"]
        notes = find_notes(items, item["key"])
        note_str = "\n\n".join(notes)
        dis_data = {
            "title": zot_data["title"],
            "raw": f"{zot_data['url']}\n\n{note_str}",
            "category": category["discourse_id"],
            "tags": [t["tag"] for t in zot_data["tags"]]
        }
        response = requests.post("https://ozglam.chat/posts.json", json=dis_data, headers=headers)
        if response.ok:
            zot_data["tags"].append({"tag": "added"})
            zot.update_item(zot_data)
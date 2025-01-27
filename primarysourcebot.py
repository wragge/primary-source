import os
from pathlib import Path
import requests
import redis
from dotenv import load_dotenv
from mastodon import Mastodon, AttribAccessDict

load_dotenv()

#   Set up Mastodon
mastodon = Mastodon(
    access_token = os.getenv("TOKEN_SECRET"),
    api_base_url = 'https://wraggebots.net/',
    version_check_mode = "none"
)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

categories = {
    6: "Collection News" ,
    9: "Research Updates",
    11: "Useful Resources"
}

def convert_case(tag):
    parts = tag.split("-")
    upper = [p.title() for p in parts[1:]]
    return f"{parts[0]}{''.join(upper)}"

def create_message(topic):
    message = f"New topic! \"{topic['title']}\" was added to the {categories[topic['category_id']]} category by {topic['last_poster_username']}. https://ozglam.chat/t/{topic['id']}"
    tags = " #".join([convert_case(t) for t in topic["tags"]])
    if tags:
        message += f" #{tags}"
    return message

def save_image(topic):
    media = []
    if topic["image_url"]:
        img_response = requests.get(topic["image_url"])
        img_file = os.path.basename(topic["image_url"])
        img_path = Path(img_file)
        img_path.write_bytes(img_response.content)
        media = mastodon.media_post(img_file, description="Image illustrating the Primary Source topic.")
        img_path.unlink()
    return media

last_id = int(redis_client.get("primary_source_last_id"))
response = requests.get("https://ozglam.chat/latest.json")
data = response.json()
topics =  data["topic_list"]["topics"]
for topic in [t for t in topics if t["id"] > last_id][::-1]:
    message = create_message(topic)
    media = save_image(topic)
    mastodon.status_post(message, media_ids=media, visibility="public")
    if topic["id"] > last_id:
        redis_client.set("primary_source_last_id", topic["id"])
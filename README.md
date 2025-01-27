# Primary Source bots

This repository contains bots used in the management of [The Primary Source](https://ozglam.chat/).

- `zotero_to_discourse.py` – Looks for additions to The Primary Source Zotero group library and creates a post for them at The Primary Source. It uses the Zotero and Discourse APIs, and the [Pyzotero](https://github.com/urschrei/pyzotero) library.
- `primarysourcebot.py` – Looks for new posts at The Primary Source and shares them through the [@primarysourcebot@wraggebots.net](https://wraggebots.net/@primarysourcebot) account on Mastodon. It uses the Mastodon API and the [Mastodon.py](https://github.com/halcy/Mastodon.py) library.
"""

Basic testing script for libgen-api-refhub.
Runs through a number of searches using different parameters, outputs results to terminal.

Run -
python3 test.py

"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from libgen_api_refhub  import LibgenSearch
import json

title = "C sharp in a Nutshell"

libgen_domains = [
    "https://libgen.bz",
    "https://libgen.li",
    "https://libgen.la",
    "https://libgen.vg",
    "https://libgen.gs",
    "https://libgen.gl",
]
# test title filtering
# should print a result for the book specified at the top of the file,
# conforming to the title_filters below.
tf = LibgenSearch()
try:
    fastest_domain = tf.find_fastest_domain(libgen_domains)
    print(f"\nUsing fastest domain: {fastest_domain}")
except Exception as e:
    print(f"\nError finding fastest domain: {e}")
    exit(1)    
title_filters = {"Extension": "PDF", "Language": "English"}
print(
    "\n>>>\tSearching for title: "
    + title
    + " with filters --- "
    + ", ".join([":".join(i) for i in title_filters.items()])
)

titles = tf.search_title_filtered(title, title_filters, exact_match=False)
# resolve_download_links = tf.resolve_download_links(titles[0]) if titles else {}
print(titles[0])
resolve_image = tf.resolve_image(titles[0]) if titles else {}
# for item in titles:
#     print(item)
# print("Download links: ", resolve_download_links)
print("Image URL: ", resolve_image)


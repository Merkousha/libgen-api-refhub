import requests
from bs4 import BeautifulSoup

# WHY
# The SearchRequest module contains all the internal logic for the library.
#
# This encapsulates the logic,
# ensuring users can work at a higher level of abstraction.

# USAGE
# req = search_request.SearchRequest("[QUERY]", search_type="[title]")


class SearchRequest:
    # Default domain, can be changed from outside the class
    domain = "https://libgen.li"

    col_names = [
        "Title",
        "Author",
        "Publisher",
        "Year",
        "Language",
        "Pages",
        "Size",
        "Extension",
        "Mirror_1",
        "Mirror_2",
        "Mirror_3",
        "Mirror_4",
        "Mirror_5",
        "Edit",
    ]

    def __init__(self, query, search_type="title"):
        self.query = query
        self.search_type = search_type

        if len(self.query) < 3:
            raise Exception("Query is too short")

    def strip_i_tag_from_soup(self, soup):
        subheadings = soup.find_all("i")
        for subheading in subheadings:
            subheading.decompose()

    def get_search_page(self):
        # تنظیم هدرها برای شبیه‌سازی یک مرورگر معمولی
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        
        query_parsed = "%20".join(self.query.split(" "))
        if self.search_type.lower() == "title":
            search_url = (
                f"{self.__class__.domain}/index.php?req={query_parsed}&column=title&res=100"
            )
        elif self.search_type.lower() == "author":
            search_url = (
                f"{self.__class__.domain}/index.php?req={query_parsed}&column=author&res=100"
            )
        search_page = requests.get(search_url, headers=headers, allow_redirects=True)
        print(search_url + " - " + str(search_page.status_code))
        return search_page

    def aggregate_request_data(self):
        search_page = self.get_search_page()
        soup = BeautifulSoup(search_page.text, "lxml")
        self.strip_i_tag_from_soup(soup)

        # Libgen results contain 3 tables
        # Table2: Table of data to scrape.
        information_table = soup.find("table", id="tablelibgen")

        # Determines whether the link url (for the mirror)
        # or link text (for the title) should be preserved.
        # Both the book title and mirror links have a "title" attribute,
        # but only the mirror links have it filled.(title vs title="libgen.io")
        raw_data = [
            [
                (
                 td.find("b").get_text(strip=True)
                 if td.find("b") and td.find("b").get_text(strip=True)
                 else next((s for s in td.stripped_strings if s.strip()), "")
                ) if i == 0 else
                td.a["href"]
                if td.find("a")
                and td.find("a").has_attr("title")
                and td.find("a")["title"] != ""
                else "".join(td.stripped_strings)
                for i, td in enumerate(row.find_all("td"))
            ]
            for row in information_table.find_all("tr")[1:]  # Skip row 0 as it is the headings row
        ]

        output_data = [dict(zip(self.col_names, row)) for row in raw_data]
        return output_data

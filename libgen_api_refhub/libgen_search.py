from .search_request import SearchRequest
import requests
from bs4 import BeautifulSoup

MIRROR_SOURCES = ["GET", "Cloudflare", "IPFS.io", "Infura"]


class LibgenSearch:
    @staticmethod
    def set_domain(new_domain):
        """Set the domain for all future requests"""
        SearchRequest.domain = new_domain

    def find_fastest_domain(self, domains):
        """Find the fastest responding domain from a list of domains"""
        import concurrent.futures
        import time

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

        def check_domain(domain):
            try:
                start_time = time.time()
                response = requests.get(
                    f"{domain}/", 
                    headers=headers,
                    timeout=15,
                    allow_redirects=True
                )
                end_time = time.time()
                if response.status_code == 200:
                    return (domain, end_time - start_time)
                return (domain, float('inf'))
            except Exception as e:
                print(f"Error checking {domain}: {str(e)}")
                return (domain, float('inf'))

        # Test all domains concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(domains)) as executor:
            results = list(executor.map(check_domain, domains))

        # Filter working domains and sort by response time
        working_domains = [(domain, time) for domain, time in results if time != float('inf')]
        if not working_domains:
            raise Exception("No working domain found")

        # Return the fastest domain
        fastest_domain = min(working_domains, key=lambda x: x[1])[0]
        self.set_domain(fastest_domain)
        return fastest_domain

    def search_title(self, query):
        search_request = SearchRequest(query, search_type="title")
        return search_request.aggregate_request_data()

    def search_author(self, query):
        search_request = SearchRequest(query, search_type="author")
        return search_request.aggregate_request_data()

    def search_title_filtered(self, query, filters, exact_match=True):
        search_request = SearchRequest(query, search_type="title")
        results = search_request.aggregate_request_data()
        filtered_results = filter_results(
            results=results, filters=filters, exact_match=exact_match
        )
        return filtered_results

    def search_author_filtered(self, query, filters, exact_match=True):
        search_request = SearchRequest(query, search_type="author")
        results = search_request.aggregate_request_data()
        filtered_results = filter_results(
            results=results, filters=filters, exact_match=exact_match
        )
        return filtered_results

    def resolve_download_links(self, item):
        mirror_1 = item["Mirror_1"]
        domain_prefix = SearchRequest.domain + "/"
        page = requests.get(domain_prefix+mirror_1)
        soup = BeautifulSoup(page.text, "html.parser")
        links = soup.find_all("a", string=MIRROR_SOURCES)
        download_links = {link.string: domain_prefix+link["href"] for link in links}
        return download_links
    
    def resolve_image(self, item):
        bookpage = item["Mirror_1"]
        domain_prefix = SearchRequest.domain + "/"
        page = requests.get(domain_prefix+bookpage)
        soup = BeautifulSoup(page.text, "html.parser")
        img = soup.find("img", src=lambda x: x and x.startswith('/covers'))
        imgsrcurl = domain_prefix+img["src"] if img else ""
        return imgsrcurl



def filter_results(results, filters, exact_match):
    """
    Returns a list of results that match the given filter criteria.
    When exact_match = true, we only include results that exactly match
    the filters (ie. the filters are an exact subset of the result).

    When exact-match = false,
    we run a case-insensitive check between each filter field and each result.

    exact_match defaults to TRUE -
    this is to maintain consistency with older versions of this library.
    """

    filtered_list = []
    if exact_match:
        for result in results:
            # check whether a candidate result matches the given filters
            if filters.items() <= result.items():
                filtered_list.append(result)

    else:
        filter_matches_result = False
        for result in results:
            for field, query in filters.items():
                if query.casefold() in result[field].casefold():
                    filter_matches_result = True
                else:
                    filter_matches_result = False
                    break
            if filter_matches_result:
                filtered_list.append(result)
    return filtered_list

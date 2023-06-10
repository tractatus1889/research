import requests
from bs4 import BeautifulSoup
import re

def wiki_search(search_term):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": search_term,
    }
    response = requests.get(url, params=params)
    data = response.json()

    results = []
    if "query" in data and "search" in data["query"]:
        search_results = data["query"]["search"]

        for result in search_results:
            title = result["title"]
            snippet = result["snippet"]
            clean = re.compile('<.*?>')
            clean_snippet = re.sub(clean, '', snippet)
            result = f"Page title: {title}\nPage snippet: {clean_snippet}"
            results.append(result)

    return "\n".join(results)


def extract_main_text(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Find the main content element
        content_div = soup.find("div", id="mw-content-text")

        if content_div:
            paragraphs = content_div.find_all("p")
            main_text = [p.get_text() for p in paragraphs]
            return main_text
        else:
            print("Main content not found.")
            return None
    else:
        print("Error: ", response.status_code)
        return None


def extract_tables(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table")
        extracted_tables = []
        for table in tables:
            table_data = []
            # Find all table rows
            rows = table.find_all("tr")
            for row in rows:
                row_data = []
                # Find all table cells in the row
                cells = row.find_all(["th", "td"])
                for cell in cells:
                    cell_text = cell.get_text(strip=True)
                    row_data.append(cell_text)
                table_data.append(row_data)
            extracted_tables.append(table_data)
        return extracted_tables
    else:
        print("Error: ", response.status_code)
        return None


def extract_all(url):
    main_text = extract_main_text(url)
    tables = extract_tables(url)
    output_lines = []

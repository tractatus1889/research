from researcher import Researcher
import requests
from bs4 import BeautifulSoup
import re
import api
import tiktoken
import research_pb2
import validation


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


def remove_citations(text):
  pattern = r"\[\d+\]"
  clean_text = re.sub(pattern, "", text)
  return clean_text


# TODO: Implement RECURSIVE_GET_PAGE_TITLES_PROMPT.
# It'll be something like:
# QUESTION: What events happened on the release date of Haruki Murakami's latest
# novel?
# KNOWN INFORMATION: Haruki Murakami's latest novel was released on yyyy/mm/dd.
# NEXT WIKIPEDIA PAGE TITLE TO RESEARCH: yyyy/mm/dd

GET_PAGE_TITLES_PROMPT = """
I am a researcher, seeking to find the answers to some questions. For each question, I want to gather all the relevant information for the question on Wikipedia. 

For each question, I want you to suggest relevant Wikipedia page titles which might have relevant information for answering the question. Give me at most 3 suggestions. Order them in a list. Don't explain your suggestions.

QUESTION: Where was the director of Pulp Fiction born?
WIKIPEDIA PAGE TITLES TO RESEARCH:
1. Pulp Fiction (film)
2. Quentin Tarantino

QUESTION: {question}
WIKIPEDIA PAGE TITLES TO RESEARCH:
"""


def get_page_titles(question):
  response_json = api.get_response(
      GET_PAGE_TITLES_PROMPT.format(question=question))
  response = response_json["content"]

  def validate_response(response):
    page_titles = response.split("\n")
    if len(page_titles) > 3:
      return False
    for ix in range(len(page_titles)):
      if not page_titles[ix][0:3].startswith(f"{ix+1}. "):
        return False
    return True

  print("Researching Wikipedia pages:")
  print(response)
  print()
  assert validate_response(response)

  page_titles = response.split("\n")
  for ix in range(len(page_titles)):
    begin = page_titles[ix].index(". ")
    page_titles[ix] = page_titles[ix][begin + 2:].strip()
  return page_titles


WIKIPEDIA_RESEARCH_PROMPT = """
I am a researcher, seeking to find the answers to some questions. For each question, I have provided some text and I want to extract relevant snippets from that text. I want you to extract the most relevant snippets from the provided text. The extracted snippet must be an EXACT substring of the original provided text with no modifications. The snippet can be 1 or 2 sentences. Please extract the snippet verbatim, do not abbreviate, do not summarize, do not paraphrase. If there is no relevant snippet, output <NONE>.

QUESTION: Where was the director of Pulp Fiction born?
PROVIDED TEXT: Pulp Fiction is a 1994 American crime film written and directed by Quentin Tarantino from a story he conceived with Roger Avary. It tells four intertwining tales of crime and violence in Los Angeles, California. The film stars John Travolta, Samuel L. Jackson, Bruce Willis, Tim Roth, Ving Rhames, and Uma Thurman. The title refers to the pulp magazines and hardboiled crime novels popular during the mid-20th century, known for their graphic violence and punchy dialogue.

Tarantino wrote Pulp Fiction in 1992 and 1993, incorporating scenes that Avary originally wrote for True Romance (1993). Its plot occurs out of chronological order. The film is also self-referential from its opening moments, beginning with a title card that gives two dictionary definitions of "pulp." Considerable screen time is devoted to monologues and casual conversations with eclectic dialogue revealing each character's perspectives on several subjects, and the film features an ironic combination of humor and strong violence. TriStar Pictures reportedly turned down the script as "too demented." Miramax co-chairman Harvey Weinstein was enthralled, however, and the film became the first that Miramax fully financed.
EXTRACTED SNIPPET: Pulp Fiction is a 1994 American crime film written and directed by Quentin Tarantino from a story he conceived with Roger Avary.

QUESTION: Where was the director of Pulp Fiction born?
PROVIDED TEXT: The first U.S. review of the film was published on May 23 in industry trade magazine Variety. Todd McCarthy called Pulp Fiction a "spectacularly entertaining piece of pop culture ... a startling, massive success." From Cannes forward, Tarantino was on the road continuously, promoting the film. Over the next few months it played in smaller festivals around Europe, building buzz: Nottingham, Munich, Taormina, Locarno, Norway, and San Sebastián. Tarantino later said, "One thing that's cool is that by breaking up the linear structure, when I watch the film with an audience, it does break [the audience's] alpha state. It's like, all of a sudden, 'I gotta watch this ... I gotta pay attention.' You can almost feel everybody moving in their seats. It's actually fun to watch an audience in some ways chase after a movie." In late September, it opened the New York Film Festival. The New York Times published its review the day of the opening. Janet Maslin called the film a "triumphant, cleverly disorienting journey through a demimonde that springs entirely from Mr. Tarantino's ripe imagination, a landscape of danger, shock, hilarity and vibrant local color ... [He] has come up with a work of such depth, wit and blazing originality that it places him in the front ranks of American film makers."
EXTRACTED SNIPPET: <NONE>

QUESTION: What's the population of Honolulu?
PROVIDED TEXT: New York, often called New York City[a] or NYC, is the most populous city in the United States. With a 2020 population of 8,804,190 distributed over 300.46 square miles (778.2 km2), New York City is the most densely populated major city in the United States and more than twice as populous as Los Angeles, the nation's second-largest city. The city also has a population that is larger than that of 38 individual U.S. states. New York City is located at the southern tip of New York State. The city constitutes the geographical and demographic center of both the Northeast megalopolis and the New York metropolitan area, the largest metropolitan area in the U.S. by both population and urban area. With over 20.1 million people in its metropolitan statistical area and 23.5 million in its combined statistical area as of 2020, New York is one of the world's most populous megacities, and over 58 million people live within 250 mi (400 km) of the city. New York City is a global cultural, financial, high-tech, entertainment, glamor, and media center with a significant influence on commerce, health care and life sciences, research, technology, education, politics, tourism, dining, art, fashion, and sports. Home to the headquarters of the United Nations, New York is an important center for international diplomacy, and is sometimes described as the capital of the world.
EXTRACTED SNIPPET: <NONE>

QUESTION: {question}
PROVIDED TEXT: {provided_text}
EXTRACTED SNIPPET: (Reminder that the extracted snippet must either be an exact substring of the provided text or <NONE>. Do not abbreviate, do not paraphrase, only output the exact snippet.) """


class WikipediaResearcher(Researcher):
  def __init__(self, num_paragraphs=8, model=api.GPT3P5):
    self.num_paragraphs = num_paragraphs
    self.model = model
    self.validate = True

  def do_research(self, question, query):
    url = f"https://en.wikipedia.org/wiki/{query}"
    # TODO: For now we only looking at the main text, but we should also extract
    # tables using extract_tables().
    paragraphs = extract_main_text(url)
    if paragraphs is None:
      return None

    research = research_pb2.Research()
    research.query = query
    research.source = "wikipedia"

    # Skip the first paragraph, which is just the URL.
    paragraphs = paragraphs[1:]
    p_ix = 0
    while p_ix < len(paragraphs):
      # TODO: This isn't a good way to do it. There's no guarantee that the
      # num_paragraphs is below the max number of tokens.
      text = "\n".join(paragraphs[p_ix: p_ix + self.num_paragraphs])
      text = remove_citations(text)
      prompt = WIKIPEDIA_RESEARCH_PROMPT.format(
          question=question, provided_text=text)
      enc = tiktoken.encoding_for_model(self.model)
      tokens = enc.encode(prompt)
      print(f"Reading {len(tokens)} tokens")

      response_json = api.get_response(prompt)
      response = response_json["content"]

      p_ix += self.num_paragraphs
      if "NONE" in response:
        continue

      if self.validate:
        if validation.validate_extraction(response, text):
          research.facts.append(response)
          print(f"Extracted and validated: {response}")
        else:
          print(f"Invalid extraction: {response}")
      else:
        research.facts.append(response)
        print(f"Extracted: {response}")

    return research

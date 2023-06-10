"""Class representing questions."""
from wikipedia_researcher import WikipediaResearcher

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

  print(", ".join(response))
  assert validate_response(response)

  page_titles = response.split("\n")
  for ix in range(len(page_titles)):
    begin = page_titles[ix].index(". ")
    page_titles[ix] = page_titles[ix][begin + 2:].strip()
  return page_titles


ANSWER_PROMPT = """
I am a researcher, seeking to find the answers to some questions. For each question, I have provided some possibly relevant sentences from Wikipedia articles. I want you to use those sentences and those sentences only to answer the question. Every claim you make in your answer must be justified by at least one provided sentence from a Wikipedia article.

Do not use any other information other than the provided sentences to answer the question. For example, if the question is "Who was the 1st US President?" and none of the provided sentences state that George Washington was the 1st US President, then you must not give George Washington as the answer.

You MUST provide a list of citations after your answer. Please quote verbatim the extracted sentences that you used to answer the question. You must include which Wikipedia article the quote comes from. If there is not enough information to answer the question, then return <NO ANSWER>.

QUESTION: Who is the top scorer in NBA history?
WIKIPEDIA PAGE TITLE: List of National Basketball Association career scoring leaders
POSSIBLY RELEVANT SENTENCE: LeBron James is the leading scorer in NBA history.
WIKIPEDIA PAGE TITLE: Kareem Abdul-Jabbar
POSSIBLY RELEVANT SENTENCE: Ferdinand Lewis Alcindor Jr. was born in Harlem, New York City, the only child of Cora Lillian, a department store price checker, and Ferdinand Lewis Alcindor Sr., a transit police officer and jazz musician.
WIKIPEDIA PAGE TITLE: Kareem Abdul-Jabbar
POSSIBLY RELEVANT SENTENCE: At the time of his retirement, Abdul-Jabbar held the record for most career games played in the NBA.
WIKIPEDIA PAGE TITLE: Kareem Abdul-Jabbar
POSSIBLY RELEVANT SENTENCE: His 38,387 career points remained the NBA's career scoring record until February 7, 2023, when he was surpassed by LeBron James of the Lakers in Los Angeles.
ANSWER: LeBron James is the top scorer in NBA history.
CITATIONS:
- "LeBron James is the leading scorer in NBA history." from the Wikipedia page List of National Basketball Association career scoring leaders.
- "His 38,387 career points remained the NBA's career scoring record until February 7, 2023, when he was surpassed by LeBron James of the Lakers in Los Angeles." from the Wikipedia page Kareem Abdul-Jabbar.

QUESTION: %s
%s
ANSWER: (Please remember to include your CITATIONS at the end of your answer.) """


class Question:
  def __init__(self, question, researchers):
    self.question = question
    self.researchers = researchers
    self.research_so_far = []

    self.queries = get_page_titles(self.question)
    self.curr_query_ix = 0

    # TODO: Implement the recursive case.
    self.recursive = False

  def research_is_finished():
    # TODO: Implement a smarter (GPT) version of this.
    return curr_query_ix >= len(queries)

  def do_next_research():
    query = self.queries[self.curr_query_ix]
    self.curr_query_ix += 1
    research_so_far.append(researchers[0].do_research(self.question, query))
    return

  def answer():
    while not research_is_finished():
      do_next_research()

    lines = []
    for research in research_so_far:
      page_title = research.query
      for fact in research.facts:
        lines.append(f"WIKIPEDIA PAGE TITLE: {page_title}")
        lines.append(f"POSSIBLY RELEVANT SENTENCE: {fact}")

    prompt = ANSWER_PROMPT % (question, "\n".join(lines))
    print(prompt)
    response_json = api.get_response(prompt)
    response = response_json["content"]
    return reponse


q = Question("What was the first book that Barack Obama published?", WikipediaResearcher())
print(q.answer())
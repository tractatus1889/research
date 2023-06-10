"""Class representing questions.

Example usage:
python question.py "What bands has Conor Oberst played in?"

Example questions:
"""
from wikipedia_researcher import WikipediaResearcher, get_page_titles
import api
import sys

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

QUESTION: {question}
{extracted_sentences}
ANSWER: (Please remember to include your CITATIONS at the end of your answer.) """


class Question:
  def __init__(self, question, researchers):
    self.question = question
    self.researchers = researchers
    self.research_so_far = []

    print(f"Question: '{self.question}'")
    self.queries = get_page_titles(self.question)
    self.curr_query_ix = 0

    # TODO: Implement the recursive case.
    self.recursive = False

  def research_is_finished(self):
    # TODO: Implement a smarter (GPT) version of this for the recursive search.
    # It'll be something like:
    # QUESTION:
    # COLLECTED RESEARCH:
    # IS THIS ENOUGH INFORMATION TO ANSWER THE QUESTION?: YES/NO
    return self.curr_query_ix >= len(self.queries)

  def do_next_research(self):
    query = self.queries[self.curr_query_ix]
    self.curr_query_ix += 1
    # TODO: Don't assume a single Researcher.
    print(f"Researching Wikipedia page: {query}")
    research = self.researchers[0].do_research(self.question, query)
    if research is not None:
      self.research_so_far.append(research)
    print()
    return

  def answer(self):
    while not self.research_is_finished():
      self.do_next_research()

    lines = []
    for research in self.research_so_far:
      page_title = research.query
      for fact in research.facts:
        lines.append(f"WIKIPEDIA PAGE TITLE: {page_title}")
        lines.append(f"POSSIBLY RELEVANT SENTENCE: {fact}")
    extracted_sentences = "\n".join(lines)

    prompt = ANSWER_PROMPT.format(
        question=self.question, extracted_sentences=extracted_sentences)
    response_json = api.get_response(prompt)
    response = response_json["content"]
    return response


if __name__ == '__main__':
  arguments = sys.argv
  question = arguments[1]

  # TODO: Stop doing all this print() garbage and do it properly.
  q = Question(question,
               [WikipediaResearcher()])
  print(f"ANSWER: {q.answer()}")

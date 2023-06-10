import api
import wiki
import tiktoken
import re
from collections import defaultdict
import validation

QUERY = "Who is the top scorer in NBA history?"
QUERY = "What was the first book that Barack Obama published?"
QUERY = "Who was the first man in space?"
QUERY = "How many home runs has Barack Obama hit in his baseball career?"
QUERY = "What bands has Jimmy Page played in?"
QUERY = "What bands has Conor Oberst played in?"
QUERY = "What software has Linus Torvalds worked on?"
QUERY = "What is Bill Gates' net worth as of now?"
QUERY = "Can you give me a summary of Bill Gates' philanthropy and how much money he's spent on philanthropy?" # GOOD ANSWER
QUERY = "How did the dinosaurs go extinct?" # GOOD ANSWER
QUERY = "What was the first book that Barack Obama published?" # GOOD ANSWER
QUERY = "What is Haruki Murakami's most recent novel?" # GOOD ANSWER
QUERY = "Where does Warren Buffett's wealth come from?"
QUERY = "What bands has Mark Kozelek played in?" # GOOD ANSWER
QUERY = "What bands has Phoebe Bridgers played in?" # GOOD ANSWER
QUERY = "What software has John Carmack worked on?" # GOOD ANSWER
QUERY = "What are the canonical dishes in Mexican cuisine?" # GOOD ANSWER
QUERY = "What are the best sights to see as a tourist in Mexico City?"
QUERY = "What book did Michael Jordan write in 1999?"
QUERY = "What book did Michael Jordan write in 2015?"
QUERY = "What bands has Mark Kozelek played in?" # GOOD ANSWER
QUERY = "How many chapters are in The Haj by Leon Uris?"
QUERY = "Can you write a sonnet that is also a haiku?"  # NO ANSWER. I think with some work we could make this work.
QUERY = "Is NYSE open on Saturday?"
QUERY = "What are the top graduate level books on arithmetic geometry in characteristic p?"
QUERY = "Who invented videogames?"  # GOOD ANSWER
# https://arstechnica.com/information-technology/2023/04/clash-of-the-ai-titans-chatgpt-vs-bard-in-a-showdown-of-wits-and-wisdom/
QUERY = "How many people get autism from vaccines every year?"  # NO ANSWER -- GOOD.
QUERY = "Who wrote Beethoven's 10th Symphony?"  # GOOD https://cs.stanford.edu/~knuth/chatGPT20.txt
QUERY = "What did Winston Churchill think of Alan Turing?"
QUERY = "Why did Jacqueline prevented Picasso's children Claude and Paloma from attending the funeral?" # GOOD -- https://twitter.com/nntaleb/status/1666298335509053440

def clean_text(text):
    pattern = r"\[\d+\]"
    clean_text = re.sub(pattern, "", text)
    return clean_text


def get_page_titles(query):
    find_page_titles = f"""
I am a researcher, seeking to find the answers to some questions. For each question, I want to gather all the relevant information for the question on Wikipedia. 

For each question, I want you to suggest relevant Wikipedia page titles which might have relevant information for answering the question. Give me at most 3 suggestions. Order them in a list. Don't explain your suggestions.

QUESTION: Where was the director of Pulp Fiction born?
WIKIPEDIA PAGE TITLES TO RESEARCH:
1. Pulp Fiction (film)
2. Quentin Tarantino

QUESTION: {query}
WIKIPEDIA PAGE TITLES TO RESEARCH:
"""

    print(
        f"""
Getting search queries using:
{find_page_titles}
==========
"""
    )

    response = api.get_response(find_page_titles)

    def validate_response(response):
        page_titles = response.split("\n")
        if len(page_titles) > 3:
            return False
        for ix in range(len(page_titles)):
            if not page_titles[ix][0:3].startswith(f"{ix+1}. "):
                return False
        return True

    print(response)
    assert validate_response(response)

    page_titles = response.split("\n")
    for ix in range(len(page_titles)):
        begin = page_titles[ix].index(". ")
        page_titles[ix] = page_titles[ix][begin + 2 :].strip()
    return page_titles


print(
    f"""Trying to answer:
{QUERY}
==========
"""
)

PAGE_TITLES = get_page_titles(QUERY)
print("Page titles:", PAGE_TITLES)

#######


def extract_relevant_text(query, page_titles):
    extract_text_prompt = f"""
I am a researcher, seeking to find the answers to some questions. For each question, I have provided some text and I want to extract relevant snippets from that text. I want you to extract the most relevant snippets from the provided text. The extracted snippet must be an EXACT substring of the original provided text with no modifications. The snippet can be 1 or 2 sentences. Extract the snippet verbatim, do not abbreviate, do not summarize, do not paraphrase. If there is no relevant snippet, output <NONE>.

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

QUESTION: %s
PROVIDED TEXT: %s
EXTRACTED SNIPPET: (Reminder that the extracted snippet must be an exact substring of the provided text. Do not abbreviate, do not paraphrase, only output the exact snippet.) """
    relevant_text = defaultdict(list)
    for page_title in page_titles:
        url = f"https://en.wikipedia.org/wiki/{page_title}"
        print(page_title)
        paragraphs = wiki.extract_main_text(url)
        if paragraphs is None:
            continue
        paragraphs = paragraphs[1:]
        ix = 0
        num_paragraphs = 8
        while ix < len(paragraphs):
            text = "\n".join(paragraphs[ix: ix+num_paragraphs])
            text = clean_text(text)

            prompt = extract_text_prompt % (query, text)
            enc = tiktoken.encoding_for_model(api.GPT3P5)
            tokens = enc.encode(prompt)
            print("prompt token length:", len(tokens))
            response = api.get_response(prompt)

            if "NONE" not in response and response not in text:
                print("response is not verbatim substring.")
                if not validation.valid_extraction(response, text):
                    print("response has hallucination.")
                    print(response)
                    response = "<NONE>"

            if "NONE" not in response:
                relevant_text[page_title].append(response)
                print(response)
            ix += num_paragraphs
        print(relevant_text[page_title])
    return relevant_text

RELEVANT_TEXT = extract_relevant_text(QUERY, PAGE_TITLES)
print(RELEVANT_TEXT)

######

def synthesize(query, relevant_text):
    synthesize_prompt = """
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
    lines = []
    for page_title, sentences in relevant_text.items():
        for sentence in sentences:
            lines.append(f"WIKIPEDIA PAGE TITLE: {page_title}")
            lines.append(f"POSSIBLY RELEVANT SENTENCE: {sentence}")
    prompt = synthesize_prompt % (query, "\n".join(lines))
    print(prompt)
    response = api.get_response(prompt)

    return response

SYNTHESIZED = synthesize(QUERY, RELEVANT_TEXT)
print(SYNTHESIZED)

# GPT research bot

by K.L. // June 7, 2023

## Instructions

1. You need an OpenAI account with API access.

2. Create a file `auth.py` with the contents:

```
ORGANIZATION = "your-org"
API_KEY = "your-openai-api-key"
```

- Your organization can be accessed at
  [https://platform.openai.com/account/org-settings](https://platform.openai.com/account/org-settings).
- Your API key can be accessed at
  [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

3. Run:

```
python question.py "your-question-here"
```

## MVP: General knowledge research

The first problem that I want to tackle is the problem of LLM hallucination. I
believe that it is incorrect to view LLMs as repositories of factual knowledge.
If you ask a plausible-sounding question, then you will get a plausible-sounding
answer. But a plausible-sounding answer does not make a correct or true answer.

I believe that instead it is better to use LLMs as a "glue layer" on top of
factual databases. Instead of thinking of LLMs as agents that know _everything_,
I think it is better to think of them as agents that know _nothing_, but that
have ordinary common sense.

Humans who know no facts about a domain can still utilize factual databases to
research and answer questions about that domain, using their common sense. So
the solution to the problem of hallucination is to engineer a setup wherein the
LLM is forced to research all of its answers, and to give citations for every
claim that it makes. An important point to make here is that the system must be
allowed to give negative answers, or non-answers, when there isn't enough
information to give a definitive response.

Furthermore, this research can be done in an iterative fashion, querying the
factual databases recursively as needed. For example, for the query "What other
events happened on the day that Haruki Murakami's latest novel was published?"
requires that you first look up the publication date of his latest novel, and
then secondly look up events on that date, once that date is known. Each step of
this process is just basic common sense and can clearly be executed by an LLM.

## Examples

Some example output is in the directory `examples/`.

Noteworthy:

- `examples/turing.txt` contains the question "What did Winston Churchill think
  of Alan Turing" which our model answers agnostically with NO ANSWER after
  researching Wikipedia. Indeed,
  [according to Donald Knuth](https://cs.stanford.edu/~knuth/chatGPT20.txt),
  there is no evidence that Churchill had any specific opinion or memory of
  Turing. The point of this example is to demonstrate producing a non-answer
  when there is no data for an answer, and avoiding hallucination.

- `examples/picasso.txt` contains the question "Why did Jacqueline prevented
  Picasso's children Claude and Paloma from attending the funeral?" which
  [Nassim Taleb asked ChatGPT and got a hallucinated answer](https://twitter.com/nntaleb/status/1666298335509053440).
  Our system instead gives a non-answer, avoiding hallucination.

## Ultimate application: Coding assistance

This idea can be extended further to any database of any kind. Specifically, I
am most interested in large codebases. One should be able to use an LLM to debug
errors by reading the code and then recursively tracing the functions throughout
different files (either by using a code search engine or by traversing the AST),
gathering all of the relevant information, and then finally synthesizing it to
provide coding assistance.

For large codebases at large corporations, the abstractions can get quite
complex and it can be quite difficult and time consuming for engineers to
decipher how things work. To understand one class can often require tracing
through several parent classes. Sometimes one doesn't need to understand all of
those classes completely, one just needs to identify e.g. the relevant parts of
the relevant ancestor methods. Instead of manually reading all of that code, an
LLM can read it for you, and extract the relevant parts, and make useful
suggestions.

## Related work and differences

This is basically the same as ChatGPT Browse, ChatGPT Plug-ins, or Bing Search,
which force the LLM to cite its answers from the web. ChatGPT Browse is also
already able to research questions in a recursive fashion:
[example](https://chat.openai.com/share/1c2a4082-d566-4e0f-9477-a44e9865b2c6).
One difference here is that I want to extend the idea so that it can use any
API, not just the single API of Bing Search. Although the web contains nearly
"all" possible information, there are still plenty of databases that are not
indexed by web search engines, for example legal databases or medical databases,
or internal corporate documentation. Furthermore, information on the web may not
be trustworthy and we may want to limit our LLM's knowledge base to a smaller
set of trustworthy sources. One can also imagine that eventually websites
themselves will contain prompt injection attacks, so we may not want to use the
entire web for security reasons.

Another related project is the Berkeley
[Gorilla](https://gorilla.cs.berkeley.edu/) project, which implements an LLM
with the ability to call over 1500 different APIs. But Gorilla is built with the
assumption that each query will only call one API. Our aim here is to be
maximally general and allow for multiple API calls per query if needed.

## Technical implementation

The Question object consists of:

- A string question
- A list of Researchers, such as WikipediaResearcher, GoogleResearcher,
  WeatherResearcher, RapGeniusResearcher, NYTimesResearcher, etc.
- A list of Research objects.
  - Each Research object consists of a query, a list of facts corresponding to
    the query, and a source (which Researcher produced this Research).

The main method is do_research() which does the following in a loop:

- If research_is_finished(), stop researching.
- Otherwise, call plan_next_research() which produces a query and selects a
  Researcher to conduct research on that query, given all the research collected
  so far.
- Given this Researcher and query, call researcher.do_research(question, query)
  and add its output Research into the list of Research done so far.
  - For example, in the case of WikipediaResearcher, the query can be the name
    of the Wikipedia article that we want to research, and do_research() can
    extract all sentences that are relevant to the question from the article.

Now we have produced all the research needed for the question. We finally call
answer() on the Question to produce a answer from the research.

Note that research_is_finished() and plan_next_research() will be implemented
with a GPT call. The Researcher method do_research() will be implemented with an
external API call (e.g. reading from a Wikipedia page) combined with a GPT call
(e.g. asking GPT to read the Wikipedia page and extract all relevant sentences).

## TODOs

- Implement more Researchers. Currently I have only implemented
  WikipediaResearcher.
  - To do so, we need do_next_research() to select between Researchers.
    Implement a prompt for that.
  - Each Researcher should have a description. The selector prompt should make
    use of the descriptions.
- Implement recursive research. I have only implemented research that queries
  wikipedia 3 times, rather than recursively.
  - Implement RECURSIVE_GET_PAGE_TITLES_PROMPT.
  - Implement research_is_finished.
  - In Question, call the API with the RECURSIVE_GET_PAGE_TITLES_PROMPT for each
    do_next_research() call.
- Implement quality tracking for each prompt model. Track all inputs and
  outputs, and a way to evaluate output quality.
- WikipediaResearcher currently reads 8 paragraphs at a time. Probably there's a
  smarter way to do this, it requires a lot of API calls which is both expensive
  and slow. Perhaps we should take embeddings of chunks of text and find
  relevant text using embeddings.

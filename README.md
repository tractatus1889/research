# GPT research bot

by K.L. // June 7, 2023

## Concept

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
claim that it makes.

Furthermore, this research can be done in an iterative fashion, querying the
factual databases recursively as needed. For example, for the query "What other
events happened on the day that Haruki Murakami's latest novel was published?"
requires that you first look up the publication date of his latest novel, and
then secondly look up events on that date, once that date is known. Each step of
this process is just basic common sense and can clearly be executed by an LLM.

## Related work and differences

This is basically the same as ChatGPT Browse or Bing Search, which force the LLM
to cite its answers from the web. ChatGPT is also already able to research
questions in a recursive fashion:
[example](https://chat.openai.com/share/1c2a4082-d566-4e0f-9477-a44e9865b2c6).
One difference here is that I want to extend the idea so that it can use any
API, not just the single API of Bing Search. Although the web contains nearly
"all" possible information, there are still plenty of databases that are not
indexed by web search engines, for example legal databases or medical databases.
Furthermore, information on the web may not be trustworthy and we may want to
limit our LLM's knowledge base to a smaller set of trustworthy sources. One can
also imagine that eventually websites themselves will contain prompt injection
attacks.

Another related project is the Berkeley
[Gorilla](https://gorilla.cs.berkeley.edu/) project, which implements an LLM
with the ability to call over 1500 different APIs. But Gorilla is built with the
assumption that one query will only call one API. Our aim here is to be
maximally general and allow for multiple API calls if needed.

## Further extensions

The MVP implementation is to use knowledge databases, but this idea can be
extended further to any database of any kind. Specifically, I am most interested
in large codebases. One should be able to use an LLM to debug errors by reading
the code and then recursively tracing the functions throughout different files
(either by using a code search engine or by traversing the AST), gathering all
of the relevant information, and then finally synthesizing it to provide coding
assistance.

## Technical implementation

The Question object consists of:

- An associated string question
- A list of Researchers, such as WikipediaResearcher, GoogleResearcher, etc.
- A list of Research objects.
  - Each Research object consists of a query, a list of facts corresponding to
    the query, and a source (which Researcher produced this Research).

The main method is do_research() which does the following in a loop:

- If research_is_finished(), stop researching.
- Otherwise, call produce_next_query() which produces a query and selects a
  Researcher to conduct that research. This method takes into account all the
  Research produced so far.
- Given this Researcher and query, call researcher.do_research(question, query)
  and add its output Research into the list of Research done so far.
  - In the case of WikipediaResearcher, the query can be the name of the
    Wikipedia article that we want to research and extract all sentences that
    are relevant to the question.

Now we have produced all the research needed for the question. We finally call
synthesize_research() on the Question to produce a answer.

Note that research_is_finished() and produce_next_query() will be implemented
with a GPT call. The Researcher method do_research() will be implemented with an
external API call (e.g. reading from a Wikipedia page) combined with a GPT call
(e.g. asking GPT to read the Wikipedia page and extract all relevant sentences).

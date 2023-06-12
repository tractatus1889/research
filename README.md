# GPT research bot

by K.L. // June 7, 2023

## Problem statement

LLMs are very simple: They are statistical next-token predictors. However, their
output is not necessarily grounded in fact, a phenomenon commonly known as
"hallucination".

For example, when you ask ChatGPT the question:

> Why did Jacqueline prevent Picasso's children Claude and Paloma from attending
> his funeral?

[It responds](https://chat.openai.com/share/b565b242-057b-4785-964b-f4884401b94c):

> There is no documented evidence to suggest that Jacqueline Roque, Pablo
> Picasso's second wife, prevented his children Claude and Paloma from attending
> his funeral. In fact, both Claude and Paloma did attend their father's funeral
> in 1973.

However, ChatGPT's response is false, as the
[Wikipedia page for Jacqueline Roque](https://en.wikipedia.org/wiki/Jacqueline_Roque)
states:

> After Picasso's death, Jacqueline prevented his children Claude and Paloma
> Picasso from attending his funeral.

## Prototype: General knowledge research

LLMs are not repositories of factual knowledge. If you ask a plausible-sounding
question, then you will get a plausible-sounding answer. But a
plausible-sounding answer does not make a correct or true answer.

How do humans answer questions they don’t know the answer to? They research the
question.

How can we give LLMs the same power? Force the LLM to research all of its
answers, and to give citations for every claim that it makes. This research can
be done in an iterative fashion, querying the factual databases recursively as
needed.

For example, answering the question

> What other events happened on the day that Haruki Murakami's latest novel was
> published?

requires that you first look up the publication date of his latest novel, and
then secondly look up events that happened on that date.

Instead of thinking of LLMs as agents that know _everything_, we can think of
them as agents that know _nothing_, but give them the ability to research their
questions via access to factual databases. By using LLMs as a "glue layer" on
top of these databases, we can answer questions with _evidence_, and thus
prevent hallucinations that are just statistically likely combinations of words.

This idea can be extended further to any database of any kind.

## Future extension: Coding assistance for large codebases

Large codebases can also be viewed as databases. We should be able to engineer a
similar setup wherein an LLM can debug errors in code by searching through
relevant files (either by using a code search engine or by traversing the AST),
gathering all of the relevant information, and finally synthesizing that
information to provide coding assistance.

Concretely, for large codebases at large corporations, the abstractions can get
quite complex and it can be quite difficult and time consuming for engineers to
decipher how things work. To understand one class can often require tracing
through many parent classes. Instead of a human engineer manually reading all of
that code, an LLM can read it for you, and extract the relevant parts, and make
useful suggestions.

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
python question.py "your question here"
```

## Examples

Full example output is in the directory `examples/`.

### True positive: What songs by the Goo Goo Dolls has Phoebe Bridgers covered?

[ChatGPT answer](https://chat.openai.com/share/bc66cda8-31ba-4205-9173-be2a3d469dfb):

> As of my knowledge cutoff in September 2021, Phoebe Bridgers has not
> officially covered any songs by the Goo Goo Dolls.

The truth:

> [Phoebe Bridgers' cover of "Iris"](https://soundcloud.com/bruh-bruh-629710116/iris-phoebe-bridgers-and-maggie-rogers)
> was released on November 13, 2020.

Our system's answer:

> Phoebe Bridgers has covered "Iris" by Goo Goo Dolls.
>
> CITATIONS:
>
> "Phoebe Bridgers covered "Iris" by Goo Goo Dolls." from the Wikipedia page
> Phoebe Bridgers.
>
> "Phoebe Bridgers' cover of "Iris" as a single specifically raised money for
> Stacey Abrams' Fair Fight Action." from the Wikipedia page Phoebe Bridgers.

### True positive: What has Conor Oberst said about Elliott Smith?

[ChatGPT answer](https://chat.openai.com/share/c4b6d1ec-3c4d-411a-8bec-959964eb2dbc):

> As of my knowledge cutoff in September 2021, Conor Oberst, the American
> musician and songwriter, has expressed his admiration for Elliott Smith on
> several occasions. Conor Oberst has referred to Elliott Smith as one of his
> musical influences and has praised his songwriting skills.
>
> In an interview with The A.V. Club in 2005, Oberst mentioned Elliott Smith as
> someone he looked up to, saying, "I think he's one of the greatest songwriters
> of our generation. I'd put him up there with Dylan or any of those guys. And
> his playing and his guitar playing are also really unique." He further
> acknowledged Smith's ability to capture complex emotions through his lyrics.`

The truth:

> There is
> [no interview with Conor Oberst](https://www.avclub.com/search?q=conor%20oberst)
> in The A.V. Club in 2005.

Our system's answer:

> Conor Oberst has said that Elliott Smith wrote the "sweetest, saddest, most
> gentle songs" in an October 22, 2003 All Things Considered interview.
>
> CITATIONS:
>
> "Oberst was greatly influenced by Daniel Johnston, whose "Devil Town" was
> covered and featured on Noise Floor, and profoundly influenced by Elliott
> Smith, stating in an October 22, 2003 All Things Considered interview that,
> "sometimes when you're not feeling good, you have to listen to really sad
> music like Elliott Smith's" and that [Smith] "wrote the sweetest, saddest,
> most gentle songs"." from the Wikipedia page Conor Oberst.

### True negative: What did Winston Churchill think of Alan Turing?

[ChatGPT answer](https://chat.openai.com/share/95f26ef5-8ad5-40df-8dab-2fed661491c7):

> Churchill recognized Turing's accomplishments and acknowledged his
> contributions. After the war, Churchill reportedly referred to Turing as
> having made the single biggest contribution to Allied victory in the war
> through his code-breaking efforts. Turing's work was highly classified during
> the war, so the full extent of his achievements only became widely known
> later.

The truth:

> [According to Donald Knuth](https://cs.stanford.edu/~knuth/chatGPT20.txt),
> there is no evidence that Churchill had any specific opinion or memory of
> Turing.

Our system's answer:

> NO ANSWER

### True negative: Why did Jacqueline prevent Picasso's children Claude and Paloma from attending his funeral?

Our system's answer:

> ANSWER: Jacqueline prevented Picasso's children Claude and Paloma from
> attending his funeral. There is no information provided that explains why she
> did so. NO ANSWER

## Related work and differences

This is basically the same as ChatGPT Browse or Bing Search, which force the LLM
to cite its answers from the web. ChatGPT Browse is also already able to
research questions in a recursive fashion:
[example](https://chat.openai.com/share/1c2a4082-d566-4e0f-9477-a44e9865b2c6).

One difference here is that I want to extend the idea so that it can use any
API, not just the single API of Bing Search, or the pre-defined APIs of ChatGPT
Plugins. There are still plenty of databases that are not indexed by web search
engines or that are non-public, for example: legal databases, medical databases,
internal corporate documentation, an individual's tax documents, etc.
Furthermore, information on the web may not be trustworthy and we may want to
limit our LLM's knowledge base to a smaller set of trustworthy sources. One can
also imagine that eventually websites themselves will contain prompt injection
attacks, so we may not want to use the entire web for security reasons.

Another difference is that I intend to make a stricter requirement that every
single claim is cited, whereas ChatGPT Browse or Bing Search do not seem to have
such a strict requirement.

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
- WikipediaResearcher currently only looks at paragraphs in the wikipedia page.
  We should also look at tables. I am not really sure how well LLMs perform on
  tabular data. It would be interesting to investigate.
- Include section titles in the wikipedia data.
- Include the "key facts" box in the wikipedia data.
- Try implementing this in
  [LangChain](https://python.langchain.com/en/latest/index.html).
- Use this
  [trick](https://github.com/minimaxir/simpleaichat/blob/main/PROMPTS.md#call-1)
  to make GPT outputs more reliable (e.g. output digits only):
  [code](https://github.com/minimaxir/simpleaichat/blob/ddf02ed5481d73d7e5ebe389aaca94c6a8a2a759/simpleaichat/chatgpt.py#L139).
  Also look into [Guidance](https://github.com/microsoft/guidance).

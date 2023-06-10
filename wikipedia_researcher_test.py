import unittest
from wikipedia_researcher import WikipediaResearcher

class WikipediaResearcherTestCase(unittest.TestCase):
  def test_wikipedia_researcher(self):
    wikipedia_researcher = WikipediaResearcher()
    research = wikipedia_researcher.do_research(
        "Where was Caveh Zahedi born?", "Caveh Zahedi")
    self.assertEqual(research.query, "Caveh Zahedi")
    self.assertGreaterEqual(len(research.facts), 1)
    self.assertEqual(research.source, "wikipedia")

if __name__ == '__main__':
    unittest.main()


import unittest

from server import search_docs


class TestSearchDocs(unittest.TestCase):
    def test_authentication_search(self):
        result = search_docs("authentication bearer token")
        self.assertIn("Source:", result)
        self.assertTrue(
            "authentication" in result.lower()
            or "bearer" in result.lower()
        )

    def test_http_429_search(self):
        result = search_docs("HTTP 429 rate limit")
        self.assertIn("429", result)
        self.assertIn("Source:", result)

    def test_empty_query(self):
        result = search_docs("")
        self.assertIn("specific", result.lower())

    def test_unknown_query(self):
        result = search_docs("xylophone meteorology")
        self.assertIn("No matching documentation", result)


if __name__ == "__main__":
    unittest.main()

import unittest

from src.social_discovery.google_discovered_pages import google_search_url, parse_html


class GoogleDiscoveryTests(unittest.TestCase):
    def test_google_url_encodes_query_without_calling_google(self):
        url = google_search_url('NVIDIA "supply rumor"')
        self.assertTrue(url.startswith("https://www.google.com/search?q="))
        self.assertIn("%22supply+rumor%22", url)

    def test_extracts_metadata_canonical_and_visible_text(self):
        html = """
        <html><head>
          <title>Example NVIDIA report</title>
          <meta property="og:description" content="Reported supplier delay">
          <meta property="article:published_time" content="2026-11-12T09:00:00-05:00">
          <link rel="canonical" href="/story/nvidia">
          <script>SHOULD_NOT_APPEAR</script>
        </head><body><nav>Navigation noise</nav>
        <main><p>Reported supplier delay. This is an allegation, not a confirmed fact.</p></main>
        </body></html>
        """
        result = parse_html(html, "https://example.com/news")
        self.assertEqual(result["title"], "Example NVIDIA report")
        self.assertEqual(result["description"], "Reported supplier delay")
        self.assertEqual(result["published_at"], "2026-11-12T09:00:00-05:00")
        self.assertEqual(result["canonical_url"], "https://example.com/story/nvidia")
        self.assertIn("Reported supplier delay.", result["content"])
        self.assertNotIn("SHOULD_NOT_APPEAR", result["content"])
        self.assertNotIn("Navigation noise", result["content"])
        self.assertEqual(result["status"], "partial")

    def test_missing_publication_date_is_not_invented(self):
        result = parse_html("<html><title>Short page</title><body>Only a few words.</body></html>",
                            "https://example.com/short")
        self.assertIsNone(result["published_at"])
        self.assertEqual(result["status"], "partial")
        self.assertTrue(result["retrieved_at"].endswith("+00:00"))


if __name__ == "__main__":
    unittest.main()

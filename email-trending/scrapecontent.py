from newspaper import Article


class Error(Exception):
    """Base class for other exceptions"""
    pass


class ScrapeError(Error):
    """Raised when error in scraping article"""
    pass


class EmptyScrape(Error):
    """Raised when the scraped contents are empty"""
    pass


class SummaryError(Error):
    """Raised when summary of article does not return a result"""
    pass


class ScrapeArticle(ScrapeError, EmptyScrape, SummaryError):
    """
    Scrape article of defined url

    Note: must download nltk package (Natural Language Toolkit)
    - In your python environment run: nltk.download()
    """

    def __init__(self, url):
        self.url = url
        self.article = Article(url)
        try:
            self.article.download()
            self.article.parse()
            if self.article is None:
                raise EmptyScrape(f"Empty contents for article {url}...")
        except Exception as e:
            raise ScrapeError(f"Error when scraping article {url}...\n{e}")

    def get_html(self):
        """Get html contents of article"""
        return self.article.html

    def get_authors(self):
        """Get html contents of article"""
        return self.article.authors

    def get_publish_date(self):
        """Get publish date of article"""
        return self.article.publish_date

    def get_text(self):
        """Get article text"""
        return self.article.text

    def summary(self):
        """
        Get summary and keywords of article
        Returns dict with keywords:
        - keywords: list of keywords in article
        - summary: summarised version of article
        """
        result = {}
        try:
            self.article.nlp()
            result["keywords"] = self.article.keywords
            result["summary"] = self.article.summary
        except Exception as e:
            raise SummaryError(f"Cannot summarise article {self.url}...\n{e}")
        return result

    def get_all(self):
        """
        Get all info on article
        Returns dict with keywords:
        - html
        - publish_date
        - text
        - summary
        - keywords
        """
        results = {"html": self.get_html(), "authors": self.get_authors(), "publish_date": self.get_publish_date(),
                   "text": self.get_text()}
        summ = self.summary()
        if summ["summary"].strip() == "":
            raise SummaryError(f"Cannot summarise article {self.url}\nBlank content")
        results["summary"] = summ["summary"]
        results["keywords"] = summ["keywords"]
        return results

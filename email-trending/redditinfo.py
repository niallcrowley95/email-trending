import praw
from requests import Session
import pathlib
import pandas as pd
from datetime import datetime, timedelta


class GetRedditInfo:
    """
    Get Reddit info from specified subreddits
    - subreddits: list of subreddits to check
    - credentials: dict of needed credentials:
        - client_id
        - client_secret
        - password
    - exclude (default None): list of URLs to exclude, ie. no articles from Breitbart
    - use_ratio (default False): upvotes / (active users).
                                 Designed to account for subreddit size.
                                 Results will be ranked by ratio, high to low
    - timeframe (default 1): amount of days back to go
    - amount (default 10): number of articles to return
    """

    def __init__(self, subreddits, credentials, exclude=None, use_ratio=False, timeframe=1, amount=10):
        self.subreddits = subreddits
        self.credentials = credentials
        self.exclude = []
        for item in exclude:
            # adding dot so it only excludes URL domain
            self.exclude.append(item + '.')
        self.use_ratio = use_ratio
        self.timeframe = timeframe
        self.amount = amount

        self.__top_articles = {}

        # initialise session
        self.session = Session()
        self.session.verify = pathlib.Path(credentials['pem_file_loc'])
        self.reddit = praw.Reddit(client_id=credentials['client_id'],
                                  client_secret=credentials['client_secret'],
                                  password=credentials['password'],
                                  user_agent=credentials['user_agent'],
                                  username=credentials['username'])

    def __order_results(self, data, headers, column_to_order, dt_column):
        """Reorder results"""
        df = pd.DataFrame(data)
        df.columns = headers

        # filter out posts more than timeframe days back
        timeback = (datetime.now() - timedelta(days=self.timeframe)).strftime("%Y-%m-%d %H:%M:%S")
        df = df[(df[dt_column] >= f'{timeback}')]

        # sort output
        df.sort_values(by=[column_to_order])

        # return the amount requested
        return df.head(self.amount)

    def get_subscribers(self, subreddit):
        """Get amount of subscribers in a subreddit"""
        try:
            subs = self.reddit.get(f'/r/{subreddit}/about.json').subscribers
            if subs is None or subs == 0:
                raise ValueError(f"Cannot get subscribers from {subreddit}")
        except Exception as e:
            raise ValueError(f"Cannot get subscribers from {subreddit}\n{e}")
        else:
            return subs

    def get_top_articles(self, pd_dataframe=True):
        """
        Get the top articles from list of subreddits
        Returns ordered pandas dataframe (default) by score descending or else list of lists
        for ratio_score true:
            Returns pandas dataframe or list of lists containing:
            - title
            - subreddit
            - score
            - ratio
            - id
            - url
            - comms_num
            - created
            - body
        for ratio_score false:
            Returns pandas dataframe containing:
            - title
            - subreddit
            - score
            - id
            - url
            - comms_num
            - created
            - body
        """
        if self.use_ratio:
            results = []
            column_headers = ["title", "subreddit", "score", "ratio", "id", "url", "comms_num", "created", "body"]
            for subreddit in self.subreddits:
                sub = self.reddit.subreddit(subreddit)
                subscriber_amount = self.reddit.get(f'/r/{subreddit}/about.json').subscribers

                # add 25 in the event of links being excluded
                top_posts = sub.hot(limit=self.amount + 25)

                for post in top_posts:
                    # skip if url in excluded list
                    if any(x in post.url for x in self.exclude):
                        continue

                    # apply ratio_score
                    ratio = post.score / subscriber_amount
                    results.append([post.title,
                                    post.subreddit,
                                    post.score,
                                    ratio,
                                    post.id,
                                    post.url,
                                    post.num_comments,
                                    datetime.fromtimestamp(post.created),
                                    post.selftext])
            final = self.__order_results(results, column_headers, 'ratio', 'created')
        else:
            results = []
            column_headers = ["title", "subreddit", "score", "id", "url", "comms_num", "created", "body"]
            for subreddit in self.subreddits:
                sub = self.reddit.subreddit(subreddit)

                # add 25 in the event of links being excluded
                top_posts = sub.hot(limit=self.amount + 25)

                for post in top_posts:
                    # skip if url in excluded list
                    if post.url in self.exclude:
                        continue

                    results.append([post.title,
                                    post.subreddit,
                                    post.score,
                                    post.id,
                                    post.url,
                                    post.num_comments,
                                    datetime.fromtimestamp(post.created),
                                    post.selftext])
            final = self.__order_results(results, column_headers, 'score', 'created')
        if pd_dataframe:
            # return dataframe
            return final
        else:
            # return list of lists
            return final.values.tolist()

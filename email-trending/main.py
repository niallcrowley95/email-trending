import redditinfo
import scrapecontent
import logging
import configReader
import pathlib
import renderhtml
import emailsender
import securityinfo
import misc
from datetime import datetime, timedelta

# this is to make it OS agnostic
config_folder = pathlib.Path('config/')
CONFIG = configReader.readFile(config_folder / "config.json")
CSS_STYLE = configReader.readFile(config_folder / "style.json")

# set logging
logging.basicConfig(level=logging.WARNING,
                    filename=pathlib.Path(CONFIG['logging']['dir']) / CONFIG['logging']['filename'],
                    filemode='a',
                    format='%(asctime)s-%(process)d-[%(levelname)s]-%(name)s-%(lineno)d: %(message)s')


def main():
    """Runs all processes for scraping and storing articles"""
    print("Starting email-trending process...")
    sections = {}

    # collect article data for each category, add to sections var
    sections['articles'] = {}
    for category in CONFIG["reddit"]["categories"]:
        print(f"\nCollecting data for {category} section...")
        logging.info(f"Collecting data for {category} section...")
        reddit = redditinfo.GetRedditInfo(
            subreddits=CONFIG["reddit"]["categories"][category]["subreddits"],
            credentials=CONFIG["reddit"]["praw_credentials"],
            exclude=CONFIG["reddit"]["exclude"],
            use_ratio=CONFIG["reddit"]["use_ratio"],
            timeframe=CONFIG["reddit"]["timeframe"],
            amount=CONFIG["reddit"]["amount"]
        )
        top_articles = reddit.get_top_articles(pd_dataframe=True)
        sections['articles'][category] = []

        # add additional blank columns
        top_articles["keywords"] = ""
        top_articles["summary"] = ""
        misc.print_progressbar(0, len(top_articles), prefix="Summarizing articles:")
        for i, article in top_articles.iterrows():
            logging.info(f"Scraping {article['url']}...")
            try:
                run = scrapecontent.ScrapeArticle(article['url'])
            except Exception as e:
                # catch if article cannot be scraped
                logging.warning(f"Exception scraping {article['url']}...\n{e}")
                continue
            try:
                content = run.summary()
                # set values in dataframe
                top_articles['keywords'].at[i] = content['keywords']
                # prepare for html
                top_articles['summary'].at[i] = content['summary'].replace("\n", "<br/>").strip()
            except scrapecontent.SummaryError as e:
                logging.warning(f"SummaryError scraping {article['url']}...\n{e}")
                continue
            # skip if content is blank
            if top_articles['summary'].at[i].strip() == "":
                continue
            # add relevant info to sections dict for email building
            sections['articles'][category].append({"title": top_articles['title'].at[i],
                                       "link": top_articles['url'].at[i],
                                       "content": top_articles['summary'].at[i]})
            misc.print_progressbar(i + 1, len(top_articles), prefix="Summarizing articles:")

    # build the email html
    logging.debug("Rendering email template")
    # use the markets section or not
    print("Building html email template")
    sections['quote'] = misc.get_quote()
    if CONFIG["markets"]["run"]:
        sections['markets'] = []
        today = datetime.today()
        # take 5 days back for weekends and public holidays
        past = today - timedelta(days=5)
        for ticker in CONFIG["markets"]["tickers"]:
            try:
                temp = securityinfo.get_sec_info(ticker=ticker,
                                                 start_date=past.strftime("%Y-%m-%d"),
                                                 end_date=today.strftime("%Y-%m-%d"))
            except Exception as e:
                logging.warning(f"Cannot get quote for {ticker}:\n{e}")
                continue
            sections['markets'].append({"ticker": ticker,
                            "price": temp["close"],
                            "change": temp['change_pc']})
    html = renderhtml.get_render(style=CSS_STYLE, sections=sections)

    # send email
    logging.debug("Sending email")
    print("Sending email")
    emailsender.send_email(sender=CONFIG['email']['sender'],
                           sender_pwd=CONFIG['email']['sender_pwrd'],
                           to_list=CONFIG['email']['to_list'],
                           html_content=html,
                           subject="email-trending")


if __name__ == '__main__':
    main()
    print("Process complete")

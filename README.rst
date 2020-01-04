===========================================
**email-trending** - Get popular article content emailed to you
===========================================


|Generic badge|

.. |Generic badge| image:: https://img.shields.io/badge/Python-3.6+-green.svg
   :target:
   
   
|MIT license|

.. |MIT license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://lbesson.mit-license.org/
email-trending scrapes articles linked to top reddit posts in the last 24 hours and emails them to you.


Setup
--------
**Clone** this repo to your system

``git clone https://github.com/niallcrowley95/email-trending``



**Run setup.py file** in a venv

``py setup.py``


**Configure the config.json file** found in ``\email-trending\src\config`` to your specs. 
  
  
  See Config Setup section below on how to setup.



**Run the script**

``py \email-trending\src\main.py``


  **Bonus Tip:** Set this up to run on a server and schedule to run with `crontab` or `windows task scheduler` every morning for a morning catchup email


Config Setup
----------------
``config.json``

  Customize what news is sent and your own personal settings

  Navigate to the `config.json` file in ``\email-trending\src\config``

  reddit:

  - `categories`: Each dict key will be its own section. Adjust the list for what subreddits should be scraped
  - `use_ratio`: If set to true will use the upvotes / subscribers ratio to adjust for smaller subreddits
  - `exclude`: What domains you don't want to be scraped and will be skipped
  - `timeframe`: How many days to go back
  - `amount`: Amount of articles to be returned per section
  - `credentials`: Reddit API credentials. Setup your reddit API credentials at https://www.reddit.com/prefs/apps/


  email:

  - `sender`: Gmail account to send from. For added security it is recommended to setup a throwaway gmail account
  - `sender_pwrd`: Sender password
  - `send_to`: list of recipients


``style.json``

  This contains the CSS styling that will be placed into the html email when rendered.


  CSS is directly placed in the html tag ``style="padding 10px; color: #000000"`` as many email clients will not enable the use of a CSS file or in the head tag. Be careful when adding a lot of styling, if the email file size is greater than 100kb gmail will not display the whole text body


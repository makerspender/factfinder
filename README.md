# factfinder
Pulls Reddit Top Facts from todayilearned subreddit based on user input query using PRAW, then retrieves Pixabay images for each fact using REQUESTS, and uploads the images to WordPress media manager via XMLRPC, then creates a draft post with images, facts and source links.

### Installation
Simply clone factfinder.py and save it in a folder of your choosing. You can create a subfolder in the directory called "/img/" or similar for storing the images that will be uploaded to WordPress.

Factfinder requires [Python](https://python.org/) v3+ to run.

Factfinder also uses a few different dependencies:

```sh
pip install praw
pip install python-wordpress-xmlrpc
pip install requests
```
### Configuration
To configure factfinder.py lines 8-14 needs to modified.

1. First you need to setup your WordPress URL, USERNAME and PASSWORD
```
wp = Client('https://wordpress.url/xmlrpc.php', 'USERNAME', 'PASSWORD')
```
2. Then go to [Reddit API doc](https://github.com/reddit/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) and follow the steps to get your client id, client secret and user agent information.
```
reddit = praw.Reddit(client_id='REDDIT-CLIENT-ID',
                     client_secret='REDDIT-CLIENT-SECRET',
                     user_agent='REDDIT-USER-AGENT')
```
3. Next you need a Pixabay username and API key. Login to your Pixabay account, and go to their [API docs](https://pixabay.com/api/docs/) and find your API KEY
```
pixabayUser = "USERNAME"
pixabayKey = "API-KEY"
```
4. Finally you can set up your path to your image folder, or just the root folder if you wish to mix images and scripts.
```
pathtoimagefolder = "C:/USERS/COMPUTERNAME/FACTFINDER/IMG/"
```
5. All done! Run the script by using your command line or create a .BAT file
```
python factfinder.py
```



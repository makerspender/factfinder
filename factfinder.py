import praw, io
import requests
from urllib import request
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
#CONFIGURE THESE SETTINGS
wp = Client('https://wordpress.url/xmlrpc.php', 'USERNAME', 'PASSWORD')
reddit = praw.Reddit(client_id='REDDIT-CLIENT-ID',
                     client_secret='REDDIT-CLIENT-SECRET',
                     user_agent='REDDIT-USER-AGENT')
pixabayUser = "USERNAME"
pixabayKey = "API-KEY"
pathtoimagefolder = "C:/USERS/COMPUTERNAME/FACTFINDER/IMG/"
#CONFIGURATION END
#asking for search term
query = input("Keyword: ")
#setting up a few local variables
wpcontent = []
imgurls = []
counter = 1
# For list of requests https://pixabay.com/api/docs/
r = requests.get('http://pixabay.com/api/'
                 '?username=%s'
                 '&key=%s'
                 '&search_term=%s'
                 '&orientation=horizontal'
                 '&image_type=all'
                 '&safesearch=true'
                 '&per_page=16'
                 '&page=1' % (pixabayUser,pixabayKey,query))
r = r.json()
# Saving list of image URLs
for item in r['hits']:
    imgurls.append(item['webformatURL'])
# Starting reddit search for settings check  http://praw.readthedocs.io
for submission in reddit.subreddit('todayilearned').search(query, sort='top', limit=15):
    tempImage = imgurls[counter]
    filename = pathtoimagefolder + counter + ".jpg"
    request.urlretrieve(tempImage, filename)
    # prepare metadata
    data = {
        'name': '%s.jpg' % counter,
        'type': 'image/jpeg',  # mimetype
    }
    # read the binary file and let the XMLRPC library encode it into base64
    with open(filename, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())
    # send image to WordPress
    response = wp.call(media.UploadFile(data))
    # save URL in temporary variable
    attachment_url = response['url']
    # set up the html content in wpcontent list
    wpcontent.append("<h3>" + submission.title + "</h3>")
    wpcontent.append("<img src='%s'><br>" % attachment_url)
    wpcontent.append("<a rel='nofollow' target='_blank' href='" + submission.url +"'>[Source]</a>")
    # count up for each reddit fact
    counter += 1
# join all strings in list for one big html chunk
postcontent = ''.join(wpcontent)
post = WordPressPost()
# simply use query word as post title
post.title = query
# post our big newly joined html chunk
post.content = postcontent
# just set as draft for now
post.post_status = 'draft'
post.id = wp.call(posts.NewPost(post))
print("Thanks for posting with factfinder!")
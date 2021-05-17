from flask import Flask
from google.transit import gtfs_realtime_pb2
from dotenv import load_dotenv
import os
import requests

#make python transit data available

def app():

    @app.route('/')
    def my_form():
        return render_template('my-form.html')

    @app.route('/', methods=['POST'])
    def my_form_post():
        text = request.form['text']
        processed_text = text.upper()
        return processed_text

def main():
    load_dotenv()
    feed = gtfs_realtime_pb2.FeedMessage()
    url = ('http://datamine.mta.info/mta_esi.php?key='
            + os.getenv("API_KEY")
            + '&feed_id=1')
    get_feed(feed, url)

def get_feed(feed, url):
    response = requests.get(url, allow_redirects=True)
    feed.ParseFromString(response.content)
    with open('output.txt', mode='w') as f:
        for entity in feed.entity:
            if entity.HasField('trip_update'):
                f.write(str(entity.trip_update))
# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''

    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))

# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

#import urllib2
import json
import requests
import os
import time
import re
import slack

ombi_url = 'http://www.omdbapi.com/?i=tt3896198&'
ombi_api = 'apikey=INSERT YOUR KEY'
root_folder = '/Users/azuser/media/movies'


headers = {
    'Content-Type': 'application/json',
    }

params = (
    ('apikey', 'xxxxxx'),
        )



# instantiate Slack client
rtmclient = slack.RTMClient(token='INSERT YOUR TOKEN')
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None


@slack.RTMClient.run_on(event='message')
def get_movie(**payload):
    data = payload['data']
    if 'add' in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        full_url = ombi_url + ombi_api + "&" + "t=" + data['text']
        params = { 'apikey': 'INSERT API KEY', 't':  data['text'].strip('add ') }
        #print (data['text'].strip('add'))
        print (params)
        response = requests.get(ombi_url, params=params)
        om_data = response.json()
        print (om_data)

        radarr_data = {'title':om_data['Title'],'qualityProfileId':'4', 'tmdbid':om_data['imdbID'].strip('tt'),'year':om_data['Year'],'titleslug':om_data['Title'] + '-' + om_data['imdbID'].strip('tt'), 'monitored':'true', 'rootFolderPath':root_folder, 'images':[{'covertype':'poster','url':om_data['Poster']}]}
        response = requests.post('http://YOUR.RADARR.HOST:7878/api/movie', headers=headers, params=params, data=json.dumps(radarr_data))

        webclient = payload['web_client']
        webclient.chat_postMessage(
            channel=channel_id,
            text= response.json(),
            thread_ts=thread_ts
        )

rtmclient.start()

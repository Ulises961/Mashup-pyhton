from sense_emu import SenseHat
from time import sleep
from requests import get  #--it comes with get and a json parser
from time import sleep

from Adafruit_IO import Client, Feed, Data, RequestError
# Import my_username, my_key
from Adafruit_key import my_username, my_key
import json
from gtts import gTTS
from pygame import mixer
import os
from math import ceil

aio = Client(my_username, my_key)

try :  # access a feed and store in feeds dictionary
    weather_feed = aio.feeds('weatherfeed')
    weather_map = aio.feeds('weathermap')
except RequestError:
    
  #  weather_feed = aio.create_feed(Feed(name='weatherfeed', key='weatherfeed', history=False))
    weather_map = aio.create_feed(Feed(name='weathermap', key='weathermap', history=False))
        # test

sense = SenseHat()
sense.clear()


url =  'http://api.openweathermap.org/data/2.5/weather?q=Trento&units=metric&appid=0e53fa039f38945cd1d62c6423362dd9'

response = get(url)
result = response.json()
print(response)



## Creates the String to 



def make_text():
    string = city + '\n'
    for items,value in output_list:
      if items == 'Humidity:':
        string += str(items) + ' ' + str(int(ceil(value))) + ' %' + '\n'
      else: string += str(items) + ' ' + str(int(ceil(value))) + ' degrees Celcius' + '\n'
  
    return string


def playAudioFile(filename):
  mixer.init()
  mixer.music.load(filename)
  mixer.music.play()
  while mixer.music.get_busy()==True:
    pass

def text2speech(text):
  filename='./Assignments/Gtts.mp3'
  tts=gTTS(text=text)
  tts.save(filename)
  playAudioFile(filename)
  os.remove(filename)
    
# Sending information to Adafruit to display in Map and Text dashboards
def post_information():
    
    coordinates = result['coord']
   

    metadata = {'lat': coordinates['lat'],
                'lon': coordinates['lon'],
                'ele': 0,
                'created_at': None}
    aio.send_data(weather_map.key, city, metadata)
    aio.send_data(weather_feed.key,make_text())

def clearFeed():
  aio.send_data(weather_map.key, city)
  aio.send_data(weather_feed.key,'-')



main_dict = result['main'].items()



## Finding the city for the map dashboard in Adafruit
city ='City: '+result['name']


## Choosing the values of our interest
raw_output=[ values for  (key,values) in main_dict if key == 'temp' or key == 'feels_like' or key == 'humidity']

##Setting the keys to be displayed in the dashboards
output_keys = ['Temperature:', 'Humidity:', 'Perceived temperature:']
## Combining 
output_list=[(key, value) for (key, value) in zip(output_keys, raw_output)]



event= sense.stick.wait_for_event()

if event.action == 'pressed':
  if event.direction == 'middle':
      
      if response.status_code > 200:
          sense.clear(255,0,0)
          sense.show_message(str(response.status_code)+ ' error')
          
      else:
          sense.clear(0,255,0)
          post_information()
          text2speech(make_text())
                   
sleep (3)      
clearFeed()
sense.show_message("bye")
sense.clear()









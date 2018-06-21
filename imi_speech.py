#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import subprocess
import aiy.i18n
import requests
from urllib.parse import quote

URL = 'http://140.112.18.214:8001/'

def main():
  aiy.i18n.set_language_code('zh-Hant')
  recognizer = aiy.cloudspeech.get_recognizer()
  recognizer.expect_phrase('關燈')
  recognizer.expect_phrase('開燈')
  recognizer.expect_phrase('閃燈')

  button = aiy.voicehat.get_button()
  led = aiy.voicehat.get_led()
  aiy.audio.get_recorder().start()

  while True:
    print('請按鈕並說話'.encode('utf-8'))
    button.wait_for_press()
    print('我正在聽...'.encode('utf-8'))
    text = recognizer.recognize()
    if not text:
      print('抱歉，我沒聽到你說什麼'.encode('utf-8'))
    else:
      print('你說："'.encode('utf-8'), text.encode('utf-8'), '"')
      resp = requests.get(URL + quote(text))
      resp_text=resp.content.decode('utf-8')
      cmd='espeak -v '+'zh+f3 '+ resp_text.replace(' ','')
      subprocess.call(cmd,shell=True)
      print('我說："'.encode('utf-8'), resp_text.encode('utf-8'), '"')
      if '開燈' in text:
        led.set_state(aiy.voicehat.LED.ON)
      elif '關燈' in text:
        led.set_state(aiy.voicehat.LED.OFF)
      elif '閃燈' in text:
        led.set_state(aiy.voicehat.LED.BLINK)
      elif '再見' in text:
        break


if __name__ == '__main__':
  main()
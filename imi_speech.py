#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import aiy.i18n
import jieba

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
    print('請按鈕並說話')
    button.wait_for_press()
    print('我正在聽...')
    text = recognizer.recognize()
    if not text:
      print('抱歉，我沒聽到你說什麼')
    else:
      print('你說："', text, '"')
      segmented = jieba.cut(text)
      print('切割如下：')
      print(' '.join(segmented))
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
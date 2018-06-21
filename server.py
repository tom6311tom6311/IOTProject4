#!/usr/bin/env python3
# _*_ coding: utf-8 _*

from word_analyzer import WordAnalyzer

"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost

"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote

class S(BaseHTTPRequestHandler):
  def do_GET(self):
    sentence = unquote(self.path[1:])
    print('Query: ', sentence.encode('utf-8'))
    resp_sentence = word_analyzer.find_similar_sentence(sentence, random_choice=False, use_jieba_seg=False)
    resp_sentence = ' '.join(resp_sentence)
    print('Response: ', resp_sentence.encode('utf-8'))
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    self.wfile.write(resp_sentence.encode("utf-8"))
        
def run(server_class=HTTPServer, handler_class=S, port=8001):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  print('Starting httpd...')
  httpd.serve_forever()

if __name__ == "__main__":
  from sys import argv

  word_analyzer = WordAnalyzer()

  if len(argv) == 2:
    run(port=int(argv[1]))
  else:
    run()

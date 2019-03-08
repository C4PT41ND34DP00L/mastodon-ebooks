import markovify
import json
import time
import sys
from os import path
from mastodon import Mastodon

api_base_url = "https://botsin.space"
access_token_path=path.join(sys.argv[1], "usercred.secret") 
corpus_path=path.join(sys.argv[1], "corpus.txt")


client = Mastodon(
        client_id="clientcred.secret", 
        access_token=access_token_path,
        api_base_url=api_base_url)

with open(corpus_path) as fp:
    model = markovify.NewlineText(fp.read())

print("tooting")
sentence = None
# you will make that damn sentence
while sentence is None:
    sentence = model.make_sentence(tries=100000)
client.status_post(sentence.replace("\0", "\n"),visibility="unlisted")

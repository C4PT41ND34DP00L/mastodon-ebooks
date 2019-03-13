import markovify
import json
import time
import sys
from os import path
from mastodon import Mastodon

api_base_url = "https://botsin.space"

def create_toot(corpus_path):
    with open(corpus_path) as fp:
        model = markovify.NewlineText(fp.read())
        sentence = None
        while sentence is None:
            sentence = model.make_sentence(tries=100000)
        return sentence

def post_toot(access_token_path, toot):
    client = Mastodon(
        client_id="clientcred.secret", 
        access_token=access_token_path,
        api_base_url=api_base_url)
    client.status_post(sentence.replace("\0", "\n"),visibility="unlisted")


if __name__ == "__main__":
    access_token_path=path.join(sys.argv[1], "usercred.secret") 
    corpus_path=path.join(sys.argv[1], "corpus.txt")
    print("tooting")
    sentence = create_toot(corpus_path)
    post_toot(access_token_path, sentence)

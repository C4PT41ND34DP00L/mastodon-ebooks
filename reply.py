import mastodon
from mastodon import Mastodon
import gen
from os import path, listdir
import threading

api_base_url = "https://botsin.space"

class ReplyListener(mastodon.StreamListener):
    def __init__(self, client, corpus_path):
        self.client = client
        self.corpus_path = corpus_path

    def on_notification(self, notification):
        print("got notification")
        print(notification)
        if notification['type'] == 'mention': #if we're mentioned:
            acct = "@" + notification['account']['acct'] #get the account's @
            post_id = notification['status']['id']
            # mention = extract_toot(notification['status']['content'])
            # toot = functions.make_toot(True)['toot'] #generate a toot
            toot = gen.create_toot(self.corpus_path)
            toot = acct + " " + toot #prepend the @
            # print(acct + " says " + mention) #logging
            visibility = notification['status']['visibility']
            if visibility == "public":
                visibility = "unlisted"
            self.client.status_post(toot, post_id, visibility=visibility) #send toost
            print("replied with " + toot) #logging


def createListener(user_directory):
    access_token_path=path.join(user_directory, "usercred.secret") 
    corpus_path=path.join(user_directory, "corpus.txt")
    client = Mastodon(
        client_id="clientcred.secret", 
        access_token=access_token_path,
        api_base_url=api_base_url)
    r1 = ReplyListener(client, corpus_path)
    print("listening...")
    client.stream_user(r1)


if __name__ == "__main__":
    import sys
    print("creating listener for", sys.argv[1])
    # createListener(sys.argv[1])
    user_directory = sys.argv[1]
    directories = [path.join(user_directory, x) for x in listdir(user_directory) if not path.isfile(path.join(user_directory, x))]
    for x in directories:
        t0 = threading.Thread(target=createListener, args=[x,])
        t0.start()



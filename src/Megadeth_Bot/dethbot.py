import praw
import time
import pickle
reddit = praw.Reddit(client_id='6kT_gyVrnaVw1w', client_secret='zr97OD57mCrQnoxQ_v2lHe8hYc0' , username='megadeth_bot' , password='iamabot', user_agent='itwillworkv1')

try:
  with open('filename.pickle', 'rb') as handle:
      bad_users_hash = pickle.load(handle)
except:
    bad_users_hash={}

def increase_violation_points(redditor):
    if str(redditor.name) in bad_users_hash:
        bad_users_hash[str(redditor.name)] = bad_users_hash[str(redditor.name)] + 1
    else:
        bad_users_hash[str(redditor.name)] = 0

def create_reply(redditor):
    print("HI create_reply")
    increase_violation_points(redditor)
    temp = bad_users_hash[str(redditor.name)]
    if temp == 0:
        return "Hi u/" + str(
            redditor.name) + "Please note that it is spelt \"Megadeth\" and not \"Megadeath\" "
    elif temp == 1:
        return "Hi u/" + str(redditor.name) + "This is your second violation. it is \"Megadeth\" and not \"Megadeath\""
    else:
        time.sleep(60)
        redditor.block()
        return "u/" + str(redditor.name) + " has been blocked on grounds of deliberate incorrect spelling."


try:
   for comment in reddit.subreddit('megadeth').stream.comments(skip_existing=True):
      if 'megadeath' in str(comment.body).lower():
          if str(comment.author.name) != "megadeth_bot":
            print("HI reply_1")

            comment.reply(create_reply(comment.author))
            print("HI reply_2")
          time.sleep(60)

except :
    with open('filename.pickle', 'wb') as handle:
        pickle.dump(bad_users_hash, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("ERROR")
    print(bad_users_hash)

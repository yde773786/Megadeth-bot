import praw
import urllib.request
import os

reddit = praw.Reddit(client_id='HWfJUOBWL1w9ZQ', client_secret='FsQn8mig4rKBDXfxFPZ0ESzo7nQ',
                     username='Picture-Organizer', password='iamabot', user_agent='imageanalyzer')

def supportedformat(geturl):

    return geturl[-3:len(geturl)] == "png" or geturl[-3:len(geturl)] == "jpg" or geturl[-4:len(geturl)] == "jpeg" \
           or geturl[-3:len(geturl)] == "gif"


def targetPath(suffix):

    home = str(os.getenv('HOME'))
    sub_path_dir = "Picture_Organizer"
    logFile_dir = os.path.join(home , sub_path_dir)
    if not os.path.isdir(logFile_dir):
        os.mkdir(logFile_dir)
    return os.path.join(logFile_dir,suffix)

def generateName():

    global current
    logFile = targetPath("tempLog.txt")
    if os.path.isfile(logFile):
       with open(logFile, 'r') as file:
          current_str = file.readline()
       if current_str[-1] == '\n':
          current_str = current_str[0:len(current_str)-1]
       current = int(current_str) + 1
       with open(logFile, 'w') as file:
          file.write(str(current))
    else:
        current = 0
        with open(logFile, 'w+') as file:
            file.write(str(current))

    return targetPath("image " + str(current))


def downloadurl(geturl):

    if supportedformat(geturl):
        picture = urllib.request.urlretrieve(geturl,generateName())
        return True
    else:
        return False


for comment in reddit.subreddit('bottest').stream.comments(skip_existing=True):
    if '!pictureorganizer' == str(comment.body):
        submission = comment.submission
        geturl = submission.url
        if downloadurl(geturl):
            comment.reply("Succesful!")
        else:
            print(geturl)
            comment.reply("The file format of submission cannot be recognized by Picture Organizer.")

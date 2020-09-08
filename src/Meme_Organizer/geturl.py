import praw
import urllib.request
import os

reddit = praw.Reddit(client_id='HWfJUOBWL1w9ZQ', client_secret='FsQn8mig4rKBDXfxFPZ0ESzo7nQ',
                     username='Picture-Organizer', password='iamabot', user_agent='imageanalyzer')


def target_path(suffix, type_input):
    home = str(os.getenv('HOME'))
    sub_path_dir = "Meme_Organizer"
    log_file_dir = os.path.join(home, sub_path_dir)
    assets_dir = os.path.join(log_file_dir, "Assets")
    if not os.path.isdir(log_file_dir):
        os.mkdir(log_file_dir)
        os.mkdir(assets_dir)

    if type_input == 0:
        return os.path.join(log_file_dir, suffix)
    else:
        return os.path.join(assets_dir, suffix)


def generate_name():
    log_file = target_path(".tempLog.txt", 0)
    if os.path.isfile(log_file):
        with open(log_file, 'r') as file:
            current_str = file.readline()
        if current_str[-1] == '\n':
            current_str = current_str[0:len(current_str) - 1]
        current = int(current_str) + 1
        with open(log_file, 'w') as file:
            file.write(str(current))
    else:
        current = 0
        with open(log_file, 'w+') as file:
            file.write(str(current))

    return "image " + str(current)


def supported_format():
    return get_url[-3:len(get_url)] == "png" or get_url[-3:len(get_url)] == "jpg" or \
                       get_url[-4:len(get_url)] == "jpeg" or get_url[-3:len(get_url)] == "gif"


def insert_asset():
    if supported_format():
        urllib.request.urlretrieve(get_url, target_path(generate_name(), 1))
        comment.reply("Successful!")
    else:
        comment.reply("The file format of submission cannot be recognized by Picture Organizer.")


def has_asset():
    path = target_path("Assets", 0)
    num_assets = len(os.listdir(path))
    return num_assets >= 1


def insert_pic():
    if has_asset() and supported_format():
        urllib.request.urlretrieve(get_url, target_path(generate_name(), 0))
        comment.reply("Successful!")
    elif supported_format():
        comment.reply("Cannot insert without asset. add flag --assets as well to make picture both asset and inserted")
    else:
        comment.reply("The file format of submission cannot be recognized by Picture Organizer.")


for comment in reddit.subreddit('bottest').stream.comments(skip_existing=True):
    comment_str = str(comment.body)
    if '!memeorganizer' in comment_str:
        submission = comment.submission
        get_url = submission.url
        count = 0
        if '--assets' in comment_str:
            comment.reply(insert_asset())
            count = count + 1
        if '--insert' in comment_str:
            comment.reply(insert_pic())
            count = count + 1
        if count == 0:
            comment.reply("missing or incorrect flag. use flag --assets or --insert")

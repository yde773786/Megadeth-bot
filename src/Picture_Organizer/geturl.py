import praw
import urllib.request
import os

from src.Picture_Organizer import compare

reddit = praw.Reddit(client_id='HWfJUOBWL1w9ZQ', client_secret='FsQn8mig4rKBDXfxFPZ0ESzo7nQ',
                     username='Picture-Organizer', password='iamabot', user_agent='imageanalyzer')


def target_path(suffix, type_input):
    home = str(os.getenv('HOME'))
    sub_path_dir = "Picture_Organizer"
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
        possible_asset = target_path(generate_name(), 1)
        urllib.request.urlretrieve(get_url, possible_asset)
        if compare.is_face(possible_asset):
            comment.reply("Successful!")
        else:
            os.remove(possible_asset)
            comment.reply("Not a face.. asset not stored")
    else:
        comment.reply("The file format of submission cannot be recognized by Picture Organizer.")


def get_assets():
    path = target_path("Assets", 0)
    asset_set = []
    for asset in os.listdir(path):
        asset_set.append(os.path.join(path, asset))

    return asset_set


def insert_pic():
    asset_set = get_assets()
    target_pic = target_path(generate_name(), 0)
    if len(asset_set) >= 1 and supported_format():
        urllib.request.urlretrieve(get_url, target_pic)
        target_folder_name = compare.assign_folder(asset_set, target_pic)
        target_folder_path = target_path(target_folder_name, 0)
        if not os.path.isdir(target_folder_path):
            os.mkdir(target_folder_path)
        os.rename(target_pic, os.path.join(target_folder_path, compare.matched_folder(target_pic)))
        comment.reply("Successful! Stored file in " + target_folder_path)
    elif supported_format():
        comment.reply("Cannot insert without asset. add flag --assets as well to make picture both asset and inserted")
    else:
        comment.reply("The file format of submission cannot be recognized by Picture Organizer.")


for comment in reddit.subreddit('all').stream.comments(skip_existing=True):
    comment_str = str(comment.body)
    if '!pictureorganizer' in comment_str:
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

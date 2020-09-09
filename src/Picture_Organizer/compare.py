import face_recognition


def find_match(asset_path, unknown_path):
    asset_image = face_recognition.load_image_file(asset_path)
    unknown_image = face_recognition.load_image_file(unknown_path)
    asset_encoding = face_recognition.face_encodings(asset_image)
    unknown_encoding = face_recognition.face_encodings(unknown_image)
    len_image = len(unknown_encoding)
    if len_image > 0:
        asset_face = asset_encoding[0]
        unknown_face = unknown_encoding[0]
        return face_recognition.compare_faces([asset_face], unknown_face)
    else:
        return False


def assign_folder(asset_set, target_pic):
    for asset_pic in asset_set:
        if find_match(asset_pic, target_pic):
            return matched_folder(asset_pic)

    return "Extraneous"


def matched_folder(asset_pic):
    folder_name = ""
    for ch in reversed(asset_pic):
        if ch == '\\' or ch == '/':
            break
        folder_name = ch + folder_name

    return folder_name


def is_face(possible_asset):
    asset_image = face_recognition.load_image_file(possible_asset)
    asset_encoding = face_recognition.face_encodings(asset_image)

    return len(asset_encoding) > 0

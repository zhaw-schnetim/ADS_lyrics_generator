import os


def create_folders():
    folders = ["results", "original_audio", "output", "transcripts", "information"]

    for folder in folders:
        if folder == "results":
            path = folder
        else:

            path = "results/" + folder

        is_exist = os.path.exists(path)

        if not is_exist:
            os.makedirs(path)

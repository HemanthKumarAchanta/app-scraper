import re

##App store reviews
def get_app_name_from_link(url):
    match = re.search(r"\/app\/([^\/]+)", url)
    if match:
        app_id = match.group(1)
        return app_id
    else:
        print("No ID found in the URL.")    

def get_id_from_link(url):
    match = re.search(r"\/id(\d+)", url)
    if match:
        app_id = match.group(1)
        return app_id
    else:
        print("No ID found in the URL.")
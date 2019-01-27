
import os.path
import re
import json
import requests
import time
import configparser

"""
 Checks if given string is a valid url
 @param {String} str - given string
 @return {Boolean}
"""


def is_url(checked_string):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return (re.match(regex, checked_string) is not None)


"""
 Checks if given url is mobile friendly
 @param {String} site_url - given url
 @return {Boolean}
"""


def is_url_friendly(site_url):
    url = "https://www.googleapis.com/pagespeedonline/v3beta1/mobileReady?url=%s" % site_url
    data = requests.get(url).text
    data = json.loads(data)

    if('error' in data):
        print("Test for '%s' has an error: %s" %
              (site_url, data['error']['errors'][0]['message']))
        return False
    if('ruleGroups' in data):
        message = None
        if(data['ruleGroups']['USABILITY']['pass'] == True):
            message = "Success"
        else:
            message = "Failed"
        print("%s - %s" % (site_url, message))
        return (data['ruleGroups']['USABILITY']['pass'])
    return False


"""
Get (and parse) settings from config.ini
@return {Object}
"""


def getSettings():
    config = configparser.ConfigParser()
    config.read("config.ini")

    arr = {}
    arr['delay'] = config.get('Settings', 'Delay')
    arr['filePath'] = config.get('Settings', 'FilePath')

    return arr


def __main__():

    # get settings from config file
    settings = getSettings()

    # check for urls.txt
    print(settings)
    if not os.path.isfile(settings['filePath']):
        print("urls.txt is missing")
        return

    # urls.txt parsing
    with open("urls.txt", "r") as f:
        arr = []
        for line in f:
            line = line.replace("\n", "")
            if(is_url(line)):
                print(line)
                arr.append(line)
            else:
                print("%s is not a valid url" % line)

    # check if urls were found
    if(len(arr) == 0):
        print("No valid urls were found on urls.txt")
        return

    # DO THE CHECk
    failed = []

    for url in arr:
        if(not is_url_friendly(url)):
            failed.append(url)
        # Sleep for 2 seconds
        time.sleep(int(settings['delay']))

    if(len(failed) == 0):
        print("The whole urls has passed the test!")
    else:
        print("%s urls are failed in the mobile friendly test." % len(failed))
        print(failed)


if(__name__ == "__main__"):
    __main__()

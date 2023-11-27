# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
import re
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def parse_date_time(date_time_string):
    try:
        return datetime.strptime(date_time_string, "%a, %d %b %Y %H:%M:%S %Z")
    except:
        pass
    try:
        return datetime.strptime(date_time_string, "%a, %d %b %Y %H:%M:%S %z")
    except:
        pass
    try:
        return datetime.fromisoformat(date_time_string)
    except:
        pass
    raise ValueError("Cannot parse " + date_time_string)


def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        try:
            description = translate_html(entry.description)
        except Exception as e:
            print(e)
            description = "No description"
        pubdate = translate_html(entry.published)

        pubdate = parse_date_time(pubdate)
        pubdate.replace(tzinfo=pytz.timezone("GMT"))

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


# ======================
# Data structure design
# ======================

# Problem 1

class NewsStory(object):

    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):

    def __init__(self, phrase):
        self.phrase = phrase.lower().split(" ")

    def is_phrase_in(self, text):
        text = re.split(f"[ {string.punctuation}]", text.lower())
        text = list(filter(lambda s: len(s) != 0, text))
        try:
            start_index = text.index(self.phrase[0])
        except ValueError:
            return False

        for shift in range(1, len(self.phrase)):
            if start_index + shift >= len(text) or self.phrase[shift] != text[start_index + shift]:
                return False
        return True


# Problem 3
class TitleTrigger(PhraseTrigger):

    def evaluate(self, story):
        return self.is_phrase_in(story.title)


# Problem 4
class DescriptionTrigger(PhraseTrigger):

    def evaluate(self, story):
        return self.is_phrase_in(story.description)


# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):

    def __init__(self, date_time):
        self.date_time = datetime.strptime(date_time, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone("EST"))


class BeforeTrigger(TimeTrigger):

    def evaluate(self, story):
        return story.pubdate.replace(tzinfo=pytz.timezone("EST")) < self.date_time


class AfterTrigger(TimeTrigger):

    def evaluate(self, story):
        return story.pubdate.replace(tzinfo=pytz.timezone("EST")) > self.date_time


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):

    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)


# Problem 8
class AndTrigger(Trigger):

    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)


# Problem 9
class OrTrigger(Trigger):

    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    return list(filter(lambda news_item: any(trigger.evaluate(news_item) for trigger in triggerlist), stories))


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    parsed_triggers = {}
    result_triggers = []
    for line in lines:
        if line.startswith("ADD"):
            for trigger_name in line.split(",")[1:]:
                result_triggers.append(parsed_triggers[trigger_name])
        else:
            arguments = line.split(",")
            trigger_name = arguments[0]
            trigger_type = arguments[1]
            match (trigger_type):
                case "TITLE":
                    parsed_triggers[trigger_name] = TitleTrigger(arguments[2])
                case "DESCRIPTION":
                    parsed_triggers[trigger_name] = DescriptionTrigger(arguments[2])
                case "BEFORE":
                    parsed_triggers[trigger_name] = BeforeTrigger(arguments[2])
                case "AFTER":
                    parsed_triggers[trigger_name] = AfterTrigger(arguments[2])
                case "NOT":
                    parsed_triggers[trigger_name] = NotTrigger(parsed_triggers[arguments[2]])
                case "AND":
                    parsed_triggers[trigger_name] = AndTrigger(parsed_triggers[arguments[2]],
                                                               parsed_triggers[arguments[3]])
                case "OR":
                    parsed_triggers[trigger_name] = OrTrigger(parsed_triggers[arguments[2]],
                                                               parsed_triggers[arguments[3]])
    return result_triggers


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            # stories = process("http://news.google.com/news?output=rss")
            stories = []
            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

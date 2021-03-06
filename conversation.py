#!/bin/python3

import os
import aiml
from apis import quotes
from apis import dictionary
from database import Database

k = None
d = None

def initBrain():
    os.chdir("/home/rikilg/mysite/")
    brain_file = "brain_files/brain.dump"

    global k
    k = aiml.Kernel()

    if os.path.exists(brain_file):
        print("Loading brain file: " + brain_file)
        k.loadBrain(brain_file)
    else:
        k.bootstrap(learnFiles="learningFileList.aiml", commands="LEARN AIML")
        print("Saving brain file: " + brain_file)
        k.saveBrain(brain_file)


def botAnswer(query):
    global k
    global d
    if k is None:
        initBrain()
    if d is None:
        d = Database()
        d.initDB()
    response = k.respond(query)
    if response is None or response == "": response = "I'm not yet programmed to understand your query!" # custom response
    d.addToDB(query, response)
    if response[0] != '/': # not a user command
        return response

    # if user command (for api)
    response = response[1:].split()

    if response[0] == 'define':
        if len(response) < 2: return "Define *what*?"
        return dictionary.define(response[1])
    elif response[0] == 'quote':
        return quotes.getQuote()

    return "Looks like a command i'm not sure of!"


def main():
    global k
    while True:
        reply = botAnswer(input("BOT > "))
        if reply:
            print("BOT > ", reply)
        else:
            print("BOT > :) ", )


if __name__ == "__main__":
    initBrain()
    main()
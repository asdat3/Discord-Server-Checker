# Discord-Server-Checker
sends Discord Webhooks when Server is running low on memory

## Setup
simply download the repository and start the main.py

## Requirements
Python3 (I used 3.6.2)
modules: discord_webhook + psutil

## How to get memory?
I am getting the memory using a module named "psutil"
since it gives me the data in bytes I have to divide by 1073741824 and round it to get it in GB
depending on how much memory there is still left the status changes from good to warning and critical

## when will the webhook be sent?
If the status changes it the webhook will be send (always(also if from critical to good))
The Status is getting displayed in the Embed
color will change too

## Databases
simple txt files :D

import datetime

from django.http import HttpResponse
from .models import RegisteredUsers, UnRegisteredUsers, tickets
# Importing Loggeres for logging execution
import logging
logger = logging.getLogger(__name__)

import smtplib, ssl
import time
from datetime import datetime


def Users_List(license):
    # Retrieving registered users and unregistered users from sqli8 database.
    users = RegisteredUsers.objects.all()
    unReg = UnRegisteredUsers.objects.all()
    licenseNum = license
    # Checking license using a string. Gets updated as yes/no based on user is registered or not.
    checklicense = ''
    print(licenseNum)
    for usr in users:
        logger.info('Entered for loop registered users')
        if usr.license == licenseNum:
            logger.info('Entered If condition')
            checklicense = 'yes'
        else:
            for unreg in unReg:
                logger.info('Entered unregistered users loop')
                if unreg.license == licenseNum:
                    logger.info('Entered unregistered users loop IF condition')
                    checklicense = 'no'
    print(checklicense)
    return checklicense

# Function to issue a ticket.
def issueTicket(license):
    licenseNum = license
    issued = ''
    # Retrieving all tickets form database to check if the ticket is already issued to the user or not.
    ticks = tickets.objects.all()
    for i in ticks:
        if i == licenseNum:
            issued = 'no'
        else:
            new_ticket = tickets(license=request.POST.get('license'))
            new_ticket.save()
            print("Issued ticket Successfully")
            issued = 'yes'
            break
    print("Issuing complete")
    logger.warning('Issuing Ticket to : ' + str(licenseNum))
    return issued

# Fucntion to send an email to the unregistered user
def email_service(license):
    unReg = UnRegisteredUsers.objects.all()
    sentStatus = ''
    ln = license
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "your email"  # Enter your address
    receiver_email = ""  # Enter receiver address
    password = "your papssword"
    # to show the current time to show in email
    timenow = datetime.now()
    print(timenow)
    message = """\
    Subject: Issued Ticket to car """ + str(ln) + """ at """ + str(timenow) + """

    Unauthorized parking at UMKC parking area. Please pay your ticket price UMKC office."""
    # Searching for unregistered users and matching with license plate
    for unreg in unReg:
        logger.info('Entered unregistered users loop')
        if unreg.license == ln:
            logger.info('Entered unregistered users loop IF condition')
            # updating receiver email with the matched user email
            receiver_email = str(unreg.email)
            print("Sending ticket email to: ", receiver_email)
    # Setting up the mail configuration
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            # Updating flag to respond back to the function call
            sentStatus = 'yes'
    except Exception as e:
        print("An error occured while sending email", e)
        sentStatus = 'no'
    return sentStatus

# Main fuction to trigger once the Scan button is clicked on UI
def checkImage():
    # Flag to iteratively check until flag is false
    waitFlag = True
    timeout = time.time() + 60*10 # Wait 10 minutes
    timeout_start = time.time()
    # Grabbing initial fize size
    with open('/Users/anilkumar/Downloads/eyeconic/main/drone/images/output.txt') as f:
        if f.readlines == "\n": lenOfFile = 0
        # If the first line of file is space, ignore it.
        else: lenOfFile = len(f.readlines())
        print("Length of file in first check: ", lenOfFile)
        # Initiating recursive check to wait until the output.txt is updated with the processed license plate.
    while waitFlag == True:
        print("Sleeping 1 min for license plate")
        time.sleep(10)  #  Sleep 10s and check again
        with open('/Users/anilkumar/Downloads/eyeconic/main/drone/images/output.txt') as f:
            if f.readlines == "\n": lenOfFile1 = 0
            else: lenOfFile1 = len(f.readlines())
            print("Length of file read in the latest check: ", lenOfFile1)
            # IF the length is greater than previous checked length and timeout is not  greater than 10 minutes
        if (lenOfFile1 > lenOfFile) & (time.time() < timeout_start + timeout):
            print("Data found in output.txt")
            with open('/Users/anilkumar/Downloads/eyeconic/main/drone/images/output.txt') as f:
                # Grab the last processed ticket
                lines = f.readlines()[-1]
                print("License Platae Number: ", lines)
            waitFlag = False
    # Function call to check user is registered or not.
    user_status = Users_List(lines)
    #Issue Ticket
    issued = issueTicket(lines)
    # Function call to initiate email service
    emailstatus = email_service(lines)
    #send response to Angular UI in JSON format
    return HttpResponse({'userValidation': user_status, 'license': lines, 'email': emailstatus})

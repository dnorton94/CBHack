# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
#import imutils
import time
import cv2
import requests
#import json
#import re

#TODA account ids
donor_account = '0de821c6-fc66-4f9d-a17b-5232dbf81b01'
homeless_account = '31ae06a7-0ef5-4087-8b0b-096b112cd8d2'
charity_account = 'b28f7b4d-42f2-4ec6-b935-1cc50a22bd77'
merchant_account = 'b3133137-f0cd-4001-8b8f-3e22b03b3d83'
bank_account = '3c46fcf4-299c-43df-869f-aad71c069de8'

#luno account ids
#donor_luno = #fin luno
bank_luno = 'janasholidays@gmail.com' #jana luno
merchant_luno = 'fin.brown@cantab.net' #fin luno again
charity_luno = 'fin.brown@cantab.net'#fin luno again

cambridge_coin_id_number = ' '
coffee_id_number = ' '

#functions

#send bitcoin from donor to the bank
def send_XBT_donor_to_bank():
    data = {
      'amount': '0.0001',
      'currency': 'XBT',
      'address': bank_luno,
      'description': 'Donation to homeless',
      'message': 'XU'
    }
    
    print("Sending bitcoin from donor to bank:")
    response = requests.post('https://api.mybitx.com/api/1/send', data=data, auth=('fbt46uaczqp3j', 'vuIZ_O1TFyr7IiZLY2k4vFpk3UyluVbXHG0srLMoQTU'))
    print("Response from Luno API:")
    if response.ok == True:
        print('200: Successfully sent bitcoin!\n')
    #print(response.text)

#send bitcoin from bank to the merchant and charity   
def send_XBT_bank_to_merchant_and_charity():
    
    #send to merchant
    data = {
      'amount': '0.000095',
      'currency': 'XBT',
      'address': merchant_luno,
      'description': 'Payment for coffee',
      'message': 'XU'
    }
    
    print("Sending bitcoin from bank to merchant:")
    response = requests.post('https://api.mybitx.com/api/1/send', data=data, auth=('mjgggbsa75a6y', 'cVPBv0U5kTJXtnneGlyLHuHFHueUbYKA24PQ68rKO0Q'))
    print("Response from Luno API:")
    if response.ok == True:
        print('200: Successfully sent bitcoin!\n')
    #print(response.text)
    
    
    #send to charity
    data = {
      'amount': '0.000005',
      'currency': 'XBT',
      'address': charity_luno,
      'description': 'Charity transaction fee',
      'message': 'XU'
    }
    
    print("Sending bitcoin from bank to charity:")
    response = requests.post('https://api.mybitx.com/api/1/send', data=data, auth=('mjgggbsa75a6y', 'cVPBv0U5kTJXtnneGlyLHuHFHueUbYKA24PQ68rKO0Q'))
    print("Response from Luno API:")
    if response.ok == True:
        print('200: Successfully sent bitcoin!\n')
    
#create file of specified type
def create_file(item_type, account_id):
    url = "https://api.todaqfinance.net/files"
    item_id = datetime.datetime.now()
    payload = "{\r\n    \"data\": {\r\n    \t\"type\":\"file\",\r\n    \t\"attributes\":{\r\n    \t\t\"payload\":{ \r\n    \t\t\t\"id\": \"%s\",\r\n\t\t\t\t \"type\": \"%s\"\r\n    \t\t}\r\n    \t},\r\n    \t\"relationships\":{\r\n    \t\t\"initial-account\":{\r\n    \t\t\t\"data\":{\r\n\t    \t\t\t\"type\":\"account\",\r\n    \t\t\t\t\"id\":\"%s\"\r\n    \t\t\t}\r\n    \t\t},\r\n    \t\t\"file-type\": {\r\n    \t\t\t\"data\": {\r\n    \t\t\t\t\"id\": \"%s\"\r\n    \t\t\t}\r\n    \t\t}\r\n    \t}\r\n    }\r\n}"%(item_id, item_type, account_id, item_id)
    headers = {
        'Content-Type': "application/json",
        'x-api-key': "92cdf65d-62aa-46c0-8ca5-81aceffbc6dc",
        'cache-control': "no-cache",
        'Postman-Token': "be3e3e23-8d50-432f-9bb0-d20d3d226ba4"
        }
    
    response = requests.request("POST", url, data=payload, headers=headers)
    #print(response.text)
    print("Response from TodaQ API:")
    if response.ok == True:
        start = 'type\":"c'
        end = '\"},\"'
        s = response.text    
        cam_coin_id_number = s[s.find(start)+len(start):s.rfind(end)]
        print('200: Successfully created ' + s[s.find(start)- 1+len(start):s.find(end)])
    else:
        print(response.text)

    if item_type == 'cambridge_coin':
        start = '{\"data":[{\"type\":\"file\",\"id\":\"'
        end = '\",\"attributes\":{\"payload\":'
        s = response.text    
        cam_coin_id_number = s[s.find(start)+len(start):s.rfind(end)]
        return cam_coin_id_number
    
    if item_type == 'coffee':
        start = '{\"data":[{\"type\":\"file\",\"id\":\"'
        end = '\",\"attributes\":{\"payload\":'
        s = response.text    
        coffee_id_number = s[s.find(start)+len(start):s.rfind(end)]
        return coffee_id_number

#transact file of specified ID    
def transact_file(sender_account_id, recipient_id, item_id):
    url = "https://api.todaqfinance.net/transactions"
    
    payload = "{\n    \"data\": {\n    \t\"relationships\":{\n    \t\t\"sender\":{\n    \t\t\t\"data\": {\n\t    \t\t\t\"type\":\"account\",\n    \t\t\t\t\"id\":\"%s\"\n    \t\t\t}\n    \t\t},\n    \t\t\"recipient\":{\n    \t\t\t\"data\": {\n\t    \t\t\t\"type\":\"account\",\n    \t\t\t\t\"id\":\"%s\"\n    \t\t\t}\n    \t\t},\n    \t\t\"files\":{\n    \t\t\t\"data\":[{\"type\":\"file\",\n\t\t    \t\t\t\"id\":\"%s\"}]\n    \t\t}\n    \t}\n    }\n}"%(sender_account_id, recipient_id, item_id)
    headers = {
        'Content-Type': "application/json",
        'x-api-key': "92cdf65d-62aa-46c0-8ca5-81aceffbc6dc",
        'cache-control': "no-cache",
        'Postman-Token': "ecc38b29-40d1-43ed-8b36-4448c148ca3a"
        }
    
    response = requests.request("POST", url, data=payload, headers=headers)

    print("Response from TodaQ API:")
    #print(response.text)
    if response.ok == True:
        print('200: Successfully transferred!')
    else:
        print(response.text)

    
def donor_charity_transaction(item_type, account_id):
    #create a cam coin
    create_file(item_type, account_id)

def bank_merchant_transaction(sender_account_id, recipient_id, item_id):
    #Bank gives cam coin to merchant
    transact_file(sender_account_id, recipient_id, item_id)
    
def recipient_merchant_transaction(merchant_account, homeless_account):
    #Coffee is created
    coffee_id_number = create_file("coffee", merchant_account)
    
    #brewing progress bar to elapse time
    items = list(range(0, 100))
    l = len(items)
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, item in enumerate(items):
        # Do stuff...
        time.sleep(0.1)
        # Update Progress Bar
        printProgressBar(i + 1, l, prefix = 'Brewing a delicious coffee!', suffix = 'Complete', length = 50)

    print("\nTransferring coffee to recipient:")
    #transfer coffee to homeless
    transact_file(merchant_account, homeless_account, coffee_id_number)
    
def merchant_charity_transaction(sender_account_id, recipient_id, item_id):
    #exchange cam coin for GBP
    #integrate with luno?
    #insert code
    transact_file(sender_account_id, recipient_id, item_id)
    #merchant is then given GBP

#Code to read QR code
def read_homeless_QR():

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
        help="path to output CSV file containing barcodes")
    args = vars(ap.parse_args())
    
    # initialize the video stream and allow the camera sensor to warm up
    #print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    #vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    barcode_found = False
    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        frame = vs.read()
        #frame = imutils.resize(frame, width=400)
    
        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)
        
            # loop over the detected barcodes
        for barcode in barcodes:
            
            barcodeData = barcode.data.decode("utf-8")
            #barcodeType = barcode.type
            barcode_found = True
    
            # draw the barcode data and barcode type on the image
            #text = "{} ({})".format(barcodeData, barcodeType)

        # show the output frame
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF
     
        # if the `q` key was pressed, break from the loop
        if barcode_found == True:
            break
    
    #do a bit of cleanup
    print("Found: Joe Bloggs \n") 
    cv2.destroyAllWindows()
    vs.stop()
    return barcodeData

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()


###################################
x = input("What would you like to donate?\n")
x = input("Which store?\n")
x = input("Which charity would you like to support?\n")
x = input("Confirm by pressing Enter:\n")               
print("\nScan QR code of the recipient:\n")
homeless_account = read_homeless_QR()        
        
print("\nDonor exchanges £ for Cambridge Coin from Bank:\n")
#send bitcoin to bank from donor
send_XBT_donor_to_bank()

#'Recieve' Cam Coin token
cambridge_coin_id_number = create_file('cambridge_coin', bank_account)

#Pause to let creation finish
time.sleep(5.0)

#Bank sends cam coin to merchant w/ smart contract (smart contract not implemented)
print("\nBank transfers cambridge coin from bank to merchant:")
bank_merchant_transaction(bank_account, merchant_account, cambridge_coin_id_number)

print('\n')
items = list(range(0, 200))
l = len(items)
printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
for i, item in enumerate(items):
    # Do stuff...
    time.sleep(0.1)
    # Update Progress Bar
    printProgressBar(i + 1, l, prefix = 'Recipient walks to merchant:', suffix = 'Complete', length = 50)

print("\nRecipient arrives at merchant and presents ID to merchant:\n")    
homeless_account = read_homeless_QR()

#brew coffee an d give to homeless
recipient_merchant_transaction(merchant_account, homeless_account)

print("\n**Short pause to allow transactions to complete**")
time.sleep(20.0)

#send coin from merchant to bank as part of smart contract (smart contract not implemented)
print("\nMerchant sends Cambridge Coin to bank and charity in return for £:")
merchant_charity_transaction(merchant_account, bank_account, cambridge_coin_id_number)
print('')

#send bitcoin from bank to merchant (and charity for 'fee')
send_XBT_bank_to_merchant_and_charity()
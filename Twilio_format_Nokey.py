import urllib.request as urlr
import urllib.parse as url
import urllib.error as urle
import json
import os
import re
from flask import Flask, request, redirect
from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse
#   python /Users/cricket/Documents/GitHub/INST126/Twilio_format.py

app = Flask(__name__)
@app.route('/sms', methods=['GET', 'POST'])

def sms_reply():
    r = MessagingResponse()
    body = request.values.get('Body', None) #this is the function that parses the messages sent. 
    if body.strip().lower() == "begin":
       r.message("Welcome to SenText! Text 'Phone XXXXX', 'Web XXXXX', or 'Address XXXXX' Replacing X's w/ 5-Digit ZipCode for Senator Info. (No DC Data Available)")        
    elif body.lower().strip().startswith('pho'):                                                                         
        extract = re.findall(r'\d+', body)  #this function extracts all the integers from the string and puts them in a list 
        extract = str(list(extract))        #this converts the list to a string, and the next one strips brackets and quotes
        extract_num = extract[2:-2]
        try:                                #this assures that the actually inputted a 5 digit zipcode. 
            if len(extract_num) == 5:      
                s = 'https://www.googleapis.com/civicinfo/v2/representatives?address='                                
                z = str(extract_num)
                k = '&key=xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                serviceurl = s+z+k
                address = serviceurl
                json_df = urlr.urlopen(address).read().decode('utf-8')
                info = json.loads(json_df)
                Senate_reps = {}                                                                                       
                for item in info['offices']: #create a list of the Official Indexes of Senate/House reps to pull info from API
                    if 'Senate' in item['name']:                                                
                        Senate_reps = item['officialIndices']
                entries_count = 0
                rep_number = 1
                Senator_Info = {}
                while entries_count < len(info['officials']):
                    for item in info['officials']:
                        if entries_count in Senate_reps:
                            Senator_Info.update({item['name']:item['phones']})
                            rep_number += 1
                        entries_count += 1
                entries_count = 0
                rep_number = 1
                r.message(str(Senator_Info).replace("{","").replace("}","").replace("[","").replace("]","").replace("'","")) #this removes braces/brackets
            else:
                print("Error")
                r.message("Error: Zip must be 5-Digits")
        except:
            pass
        
    elif body.strip().lower().startswith('web'):
        extract = re.findall(r'\d+', body)
        extract = str(list(extract))
        extract_num = extract[2:-2]
        try:
            if len(extract_num) == 5: 
                s = 'https://www.googleapis.com/civicinfo/v2/representatives?address='
                z = str(extract_num)
                k = '&key=xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                serviceurl = s+z+k
                address = serviceurl
                json_df = urlr.urlopen(address).read().decode('utf-8')
                info = json.loads(json_df)
                Senate_reps = {}
                for item in info['offices']: #create a list of the Official Indexes of Senate/House reps to pull info from
                    if 'Senate' in item['name']:
                        Senate_reps = item['officialIndices']
                entries_count = 0
                rep_number = 1
                Senator_Info = {}
                while entries_count < len(info['officials']):
                    for item in info['officials']:
                        if entries_count in Senate_reps:
                            Senator_Info.update({item['name']:item['urls']})
                            rep_number += 1
                        entries_count += 1
                entries_count = 0
                rep_number = 1
                r.message(str(Senator_Info).replace("{","").replace("}","").replace("[","").replace("]","").replace("'",""))
            else:
                print("Error")
                r.message("Error: Zip must be 5-Digits")
        except:
            pass
                
    elif body.strip().lower().startswith('ad'):
        extract = re.findall(r'\d+', body)
        extract = str(list(extract))
        extract_num = extract[2:-2]
        try:
            if len(extract_num) == 5: 
                s = 'https://www.googleapis.com/civicinfo/v2/representatives?address='
                z = str(extract_num)
                k = '&key=xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                serviceurl = s+z+k
                address = serviceurl
                json_df = urlr.urlopen(address).read().decode('utf-8')
                info = json.loads(json_df)
                Senate_reps = {}
                for item in info['offices']: #create a list of the Official Indexes of Senate/House reps to pull info from
                    if 'Senate' in item['name']:
                        Senate_reps = item['officialIndices']
                entries_count = 0
                rep_number = 1
                Senator_Info = {}
                while entries_count < len(info['officials']):
                    for item in info['officials']:
                        if entries_count in Senate_reps:
                            Senator_Info.update({item['name']:item['address']})
                            rep_number += 1
                        entries_count += 1
                entries_count = 0
                rep_number = 1        
                r.message(str(Senator_Info).replace("{","").replace("}","").replace("[","").replace("]","").replace("'",""))
            else:
                print("Error")
                r.message("Error: Zip must be 5-Digits")
        except:
            pass                     
    else:
        r.message("Sorry, you need to check the format guidelines and try again.")
    return str(r)

if __name__ == "__main__":
    app.run(debug=True)




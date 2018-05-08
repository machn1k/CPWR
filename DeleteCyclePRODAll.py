# ////////////////////////////////////////////////////////////////////////////
# //
# //  D SOFTWARE INCORPORATED
# //  Copyright 2007-2014 D Software Incorporated
# //  All Rights Reserved.
# //
# //  NOTICE: D Software permits you to use, modify, and distribute this file
# //  in accordance with the terms of the license agreement accompanying it.
# //
# //  Unless required by applicable law or agreed to in writing, software
# //  distributed under the License is distributed on an "AS IS" BASIS,
# //  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# //
# ////////////////////////////////////////////////////////////////////////////
#
# This is a sample of what can be done by using API with Zephyr for JIRA through the Python coding language.
# The goal of the sample is to create a new test cycle and add existing test issues into it
# 
# IDLE IDE - Version: 2.7.5
# Python - Version: 2.7.5
# 
# Author: Daniel Gannon, Technical Support Analyst, D Software Inc.

# Import from libraries 'urllib2', 'urllib', 'json', 'base64'
from urllib2 import Request, urlopen
from urllib import quote
from json import dumps, load
from base64 import b64encode
from datetime import datetime
import sys

# Variables used:
# 'username' and 'password' variables for encoding into header below
# 'projectId' variable used to determine which project new execution schedules will be made in
# 'versionId' variable used to determine which version in the chosen project new execution schedules will be made in ("-1" is Unscheduled)
# 'cycleId' variable used to determine which cycle in the chosen version new execution schedules will be made in ("-1" is Ad Hoc)
# 'defectsToLink' list used to determine which defects will be linked to tests executed in code
username = 'zapiplugin'
password = 'redwing1'
projectId = 12801
versionId = 19400
cycleId = -1
defectsToLink = ["ZEP-5"]

testIssueIdList = []
testResultList = []

productname = sys.argv[1]
print "product name " + productname

versionname = sys.argv[2]
print "Version name " + versionname

startdate = sys.argv[3]
print "Start Date " + startdate

cyclename = sys.argv[4]
print "Cycle name " + cyclename


# 'baseURL' holds basic data for JIRA server that will be used in API URL calls
# 'issueSearchURL' holds URL sent to JIRA to search based on query provided
# 'assignmentURL' holds URL sent to ZAPI to POST new execution assignments
baseURL = 'https://agile.compuware.com'
getCyclesURL = baseURL + '/rest/zapi/latest/cycle?projectId=' + str(projectId) + '&versionId=' + str(versionId)

# 'headers' holds information to be sent with the JSON data set
# Initialized with Auth and Content-Type data
# Authorization header uses base64 encoded username and password string
headers = {"Authorization": " Basic " + b64encode(username + ":" + password), "Content-Type": "application/json"}
     
# 'versionUrl' holds URL sent to JIRA to return all version for a given project
versionUrl = baseURL + "/rest/api/2/project/" + str(projectId) + "/versions"

print "Running get versions..."

request = Request(versionUrl, None, headers=headers)
js_res = urlopen(request)

objResponse = load(js_res)

#print objResponse

for versions in objResponse:
      vName = versions['name']
      vId = versions['id']

      if vName == versionname:
         print "name/value returned =" + vName + ":" + vId
         #request = Request('https://agile.compuware.com/rest/zapi/latest/cycle?projectId=' + str(projectId) + '&versionId=' + vId, headers=headers)

         break
      
     
print "Retrieved version ID!"

print "Getting cycles..."

#values = ({})

#request = Request(getCyclesURL, None, headers=headers)

request = Request('https://agile.compuware.com/rest/zapi/latest/cycle?projectId=' + str(projectId) + '&versionId=' + vId, headers=headers)

response_body = urlopen(request)

objResponse = load(response_body)

#print objResponse

for cycles in objResponse:
      cycleid = str(cycles)

	  #print "Beginning cycle id = " + cycleid
	  
      if cycleid == 'recordsCount':
            continue

      if cycleid == '-1':
            continue
      
      #Get individual cycle
      #request = Request('https://agile.compuware.com/rest/zapi/latest/cycle?id=' + cycleid, headers=headers)
      request = Request('https://agile.compuware.com/rest/zapi/latest/cycle/' + cycleid, headers=headers)

      response_body = urlopen(request)

      objResponse = load(response_body)
	  
      print "product name = " + objResponse['environment']
	  
	  

      a = datetime.strptime(startdate, '%d/%b/%y')
      b = datetime.strptime(objResponse['startDate'], '%d/%b/%y')

      if not cyclename:
         if (b <= a):
            print "cycle id = " + cycleid
            print "startdate = " + objResponse['startDate']
            print "product = " + objResponse['environment']
      
            request = Request('https://agile.compuware.com/rest/zapi/latest/cycle/' + cycleid, headers=headers)
            request.get_method = lambda: 'DELETE'

            response_body = urlopen(request)
            objResponse = load(response_body)
            print objResponse
      else:
         if ((cyclename == objResponse['name']) and (productname == objResponse['environment'])):
            print "cycle id = " + cycleid
            print "startdate = " + objResponse['startDate']
            print "product = " + objResponse['environment']
            print "cycle name = " + objResponse['name']
            
            request = Request('https://agile.compuware.com/rest/zapi/latest/cycle/' + cycleid, headers=headers)
            request.get_method = lambda: 'DELETE'

            response_body = urlopen(request)
            objResponse = load(response_body)
            print objResponse
            break
		 

      

      

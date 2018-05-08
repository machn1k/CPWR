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
versionId = -1
cycleId = -1
defectsToLink = ["ZEP-5"]

testIssueIdList = []
testResultList = []
testReasonList = []

# 'query' variable used to store JQL that will be plugged into 'issueSearchURL'
# Takes projectId variablized above and appends the JQL provided. Zephyr for JIRA does not allow assignment of test issues across projects
# If your copied JQL from JIRA includes the project, you can edit the query to only include your string
query = 'project = ' + str(projectId)
query = query + ' AND issuetype = Test AND assignee in ("manoj.singh@compuware.com") AND "test script name" ~ PLITST06_VWR'

# 'baseURL' holds basic data for JIRA server that will be used in API URL calls
# 'issueSearchURL' holds URL sent to JIRA to search based on query provided
# 'assignmentURL' holds URL sent to ZAPI to POST new execution assignments
baseURL = 'https://agile.compuware.com'
issueSearchURL = baseURL + "/rest/api/2/search" + "?jql=" + quote(query, '()"')
createCycleURL = baseURL + '/rest/zapi/latest/cycle'
assignmentURL = baseURL + "/rest/zapi/latest/execution"

# 'execute' is the JSON data set that houses information for what status the assigned tests will be set to
# Currently, this is set to a static "Pass" (1) value
executePass = dumps({
    "status": "1"
})

executeWIP = dumps({
    "status": "3"
})

executeNotEx = dumps({
    "status": "-1"
})

# 'headers' holds information to be sent with the JSON data set
# Initialized with Auth and Content-Type data
# Authorization header uses base64 encoded username and password string
headers = {"Authorization": " Basic " + b64encode(username + ":" + password), "Content-Type": "application/json"}

#Read and parse test results file
print "Fetching Tests..."


#file=open("c:/python/resultsuat.txt",'r')
file=open(sys.argv[1],'r') 

buildnum = ""

if len(sys.argv) == 3:
    buildnum = sys.argv[2]

row = file.readlines()

#Get the common info first
i = 0
for line in row:

   if i == 0:
      #Get cycle name
      info = row[i].split("=")
      cyclename = str(info[1]).strip()
      print "cycle name " + cyclename
      i = i + 1
      continue

   if i == 1:
      #Get product name
      info = row[i].split("=")
      productname = str(info[1]).strip()
      print "product name " + productname
      i = i + 1
      continue

   if i == 2:
      #Get version name
      info = row[i].split("=")
      versionname = str(info[1]).strip()
      print "Version name " + versionname
      i = i + 1
      continue
   
   info = line.split("=")

   testscriptname = str(info[0])

   print "script name = " + testscriptname
   
   #The second value contains results and reason
   resultset = info[1].split("%")
   
   result = str(resultset[0]).strip()
   print "result = " + result
   
   reason = str(resultset[1]).strip()
   print "reason = " + reason
  

   # ///// Run JQL query /////

   # 'query' variable used to store JQL that will be plugged into 'issueSearchURL'
   # Takes projectId variablized above and appends the JQL provided. Zephyr for JIRA does not allow assignment of test issues across projects
   # If your copied JQL from JIRA includes the project, you can edit the query to only include your string
   query = 'project = ' + str(projectId)
   #query = query + ' AND issuetype = Test AND assignee in ("manoj.singh@compuware.com") AND "test script name" ~ ' + testscriptname
   #query = query + ' AND issuetype = Test AND "test script name" ~ ' + "'" + testscriptname + "'"
   query = query + ' AND issuetype = Test AND "Product/s" = ' + "'" + productname + "'" + ' AND "test script name" ~ ' + "'" + testscriptname + "'"

   # 'issueSearchURL' holds URL sent to JIRA to search based on query provided
   issueSearchURL = baseURL + "/rest/api/2/search" + "?jql=" + quote(query, '()"')

   print issueSearchURL
   print "Running JQL query..."

   request = Request(issueSearchURL, None, headers=headers)
   js_res = urlopen(request)

   objResponse = load(js_res)

   print "Running JQL query completed!"
   
   issueList = []

   issueList = objResponse["issues"]

   for testIssue in issueList:
	   testId = testIssue['id']
	   print "id returned =" + testId
	   testIssueIdList.append(testId)

	   if result in ['PASS', 'Pass']:
		  testResultList.append("1")
		  testReasonList.append(reason)
	   elif result in ['FAIL', 'Fail']:
		  testResultList.append("2")
		  testReasonList.append(reason)
	   elif result in ['WIP','Wip']:
		  testResultList.append("3")
		  testReasonList.append(reason)
	   else:
		  testResultList.append("-1")
		  testReasonList.append(reason)
	   break
print "Fetch Completed!"

# 'versionUrl' holds URL sent to JIRA to return all version for a given project
versionUrl = baseURL + "/rest/api/2/project/" + str(projectId) + "/versions"

print "Running get versions..."

request = Request(versionUrl, None, headers=headers)
js_res = urlopen(request)

objResponse = load(js_res)

for versions in objResponse:
      vName = versions['name']
      vId = versions['id']

      if vName == versionname:
            print "name/value returned =" + vName + ":" + vId
            versionId = vId
            break
     
     
print "Retrieved version ID!"


# ///// Create New Cycle /////
# Create new cycle in Zephyr for JIRA. Cycle information defined above in 'newCycleValues' object
# Save new cycle ID from ZAPI response

d = datetime.now()

mon = d.month

if d.month == 1:
	mon = "Jan"
elif d.month == 2:
	mon = "Feb"
elif d.month == 3:
	mon = "Mar"
elif d.month == 4:
	mon = "Apr"
elif d.month == 5:
	mon = "May"
elif d.month == 6:
	mon = "Jun"
elif d.month == 7:
	mon = "Jul"
elif d.month == 8:
	mon = "Aug"
elif d.month == 9:
	mon = "Sep"
elif d.month == 10:
	mon = "Oct"
elif d.month == 11:
	mon = "Nov"
elif d.month == 12:
	mon = "Dec"

	
sdate = str(d.day) + "/" + str(mon) + "/" + str(d.year)

print "sdate " + sdate



# 'newCycleValues' is the JSON data set that houses the information for the new cycle
# 'projectId' & 'versionId' initialized above
newCycleValues = dumps({
    "clonedCycleId": "",
    #"name": "Created In ZAPI",
    "name":  cyclename,
    "build": buildnum,
    "environment": productname,
    "description": "Created In ZAPI",
    "startDate": sdate,
    "endDate": sdate,
    "projectId": projectId,
    "versionId": versionId
})

print "Creating new cycle..."

request = Request(createCycleURL, data=newCycleValues, headers=headers)
js_res = urlopen(request)

objResponse = load(js_res)
newCycleId = objResponse['id']

print "cycle id = " + str(newCycleId)

print "New Cycle Created!"

# ///// Assign Fetched Tests in Unscheduled version - Ad Hoc cycle /////
# Use issue ID to create a new execution assignment and append execution ID to list

print "Assigning Fetched Tests..."

assignmentList = []
for testIssueId in testIssueIdList:
    assignment = dumps({
        "issueId": testIssueId,
        "versionId": versionId,
        "cycleId": newCycleId,
        "projectId": projectId
    })

    request = Request(assignmentURL, data=assignment, headers=headers)
    js_res = urlopen(request)
    objResponse = load(js_res)

    i = iter(objResponse)
    j = str(i.next())
    assignmentList.append(j)

print "Assignment Completed!"

# ///// Execute Assigned Tests /////
# Use execution schedule ID to perform execution and change status

print "Executing Assignments..."

i = 0
for assignmentId in assignmentList:
    quickExecuteURL = baseURL + "/rest/zapi/latest/execution/" + assignmentId + "/execute"
	
    executeFail = dumps({"status":"2","comment":testReasonList[i]})

    if testResultList[i] == "1":
        request = Request(quickExecuteURL, data=executePass, headers=headers)
    elif testResultList[i] == "2":
        request = Request(quickExecuteURL, data=executeFail, headers=headers)            
    elif testResultList[i] == "3":
        request = Request(quickExecuteURL, data=executeWIP, headers=headers)            
    else:
        request = Request(quickExecuteURL, data=executeNotEx, headers=headers)
        
    request.get_method = lambda: 'PUT'
    
    urlopen(request)

    i = i + 1

print "Execution Completed!"

print "Fetch, Create Cycle, Execute, and Defect Linking Completed!"

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
# Author: Manoj Singh

# Import from libraries 'urllib2', 'json', and 'base64'
from urllib2 import Request, urlopen
from json import dumps, load
from base64 import b64encode
from time import localtime, gmtime, strftime
 
import sys

# Variables used:
reason = ""

#Read, parse test results and create a ZAPI compliant resuts file
print "Reading RCPTT test results file..."

#file=open("C:\Users\pfhmks0\Documents\Automation\RCPTTProjects\Python\out.txt",'r')
file=open(sys.argv[1],'r')
fileout = open(sys.argv[5], 'w')  

#Read product code, product and version info
cycle = sys.argv[2]
product = sys.argv[3]
version = sys.argv[4]

#Generate a test cycle name
#cycle = productcode + "-" + strftime("%Y-%m-%d-%H:%M", localtime())

print "cycle = " + cycle

#Write the cycle, product and version to the output file
fileout.write("Cycle=" + cycle + '\n')
fileout.write("Product=" + product + '\n')
fileout.write("Version=" + version + '\n')

#Get the tests

row = file.readlines()

for line in row:

   if (line.find("processed.") != -1):
      
      #Split the line on period
      info = line.split(".")

      #Get test case name
      testcasename = str(info[3])

      #Strip of leding and trailing spaces
      testcasename = testcasename.strip()
      
      print "Test Case Name: " + testcasename

      #Get the test result (pass/fail)
      testresult = str(info[0])[:4]

      print "Test Result: " + testresult      

      #Get the failure cause from the line
      cause = line.split("Cause:")

      print "cause length: " + str(len(cause))

      if len(cause) > 1:
         reason = str(cause[1])
         print "reason: " + reason
      
      #Write to results file      
      fileout.write(testcasename + "=" + testresult + "%" + reason.strip() + '\n')

      #Reset reason
      reason = ""
      
#Close files
file.close()
fileout.close()
print "Execution Completed!"


from __future__ import division
import os
import subprocess
import re
import threading
import time
import sys
import string
LIMIT_a=0
LIMIT_b=0
percentage=0

if len(sys.argv)>1:
        first_file = sys.argv[1]
        second_file = sys.argv[2]

#file_name = "009git_log.txt"
first_log = open(first_file,"r+")
first_log_content = first_log.readlines()
first_parsed_file = first_file[:-4] + "_parse.txt"
log_parsed = open(first_parsed_file,"w+").close()
log_parsed = open(first_parsed_file,"w+")
count =0
temp = 0

for line in first_log_content :
        if "commit" in line:
                count=0
                temp=5
        count+=1
        if "Merge:" in line:
                temp += 1
        if count == temp:
                content = line
        elif "Change-Id:" in line:
                ch_id_raw = line.split()
                ch_id = ch_id_raw[1:]
                ch_id = string.join(ch_id)
                log_parsed.write(ch_id)
                log_parsed.write(" ")
                log_parsed.write(content)
                #log_parsed.write("\n")
                LIMIT_a+=1
log_parsed.close()
first_log.close()

second_log = open(second_file,"r+")
second_log_content = second_log.readlines()
second_parsed_file = second_file[:-4] + "_parse.txt"
log_parsed = open(second_parsed_file,"w+").close()
log_parsed = open(second_parsed_file,"w+")
count =0

for line in second_log_content :
        if "commit" in line:
                count=0
                temp =5
        count+=1
        if "Merge:" in line:
                temp += 1
        if count == temp:
                content = line
        elif "Change-Id:" in line:
                ch_id_raw = line.split()
                ch_id = ch_id_raw[1:]
                ch_id = string.join(ch_id)
                log_parsed.write(ch_id)
                log_parsed.write(" ")
                log_parsed.write(content)
                #log_parsed.write("\n")
                LIMIT_b+=1
log_parsed.close()
second_log.close()

if LIMIT_a > LIMIT_b:
        LIMIT = LIMIT_a
else:
        LIMIT = LIMIT_b

total = (LIMIT_a + LIMIT_b)+2

a = [""]*(LIMIT)
b = [""]*(LIMIT)
a_id = [""]*(LIMIT)
b_id = [""]*(LIMIT)

log009 = open(first_parsed_file,"r+")
content009 = log009.readlines()
log200 =open(second_parsed_file,"r+")
content200 = log200.readlines()
log_diff = open("diff_log.html","w+").close()
log_diff = open("diff_log.html","w+")

#print_result = "{0:^6}|{1:^50}|{2:^50}|".format("no.","Missing from "+first_file,"Missing from "+second_file)
#log_diff.write(print_result)
#log_diff.write("\n")

print_result = """<table style=\"width:1000px\">
<tr>
  <th style="width: 30px">no.</th>
  <th style="width: 400px">Missing from """ + first_file+"""</th>
  <th style="width: 400px">Missing from """+ second_file+"""</th>
  </tr>
<tr>"""
log_diff.write(print_result)
log_diff.write("\n")


diff="not used"
count_a =0
count_200 = 0
count_009 = 0
counting_diff =1

per_count = 0
percent_temp = 0
#print "total : ",
#print total
total_a=0
total_b =0

for line in content009:
        description_raw = line.split()
        description = description_raw[0]
        description_str = string.join(description," ")
        for sentence in content200:
                description200_raw = sentence.split()
                description200 = description200_raw[0]
                description200_str = string.join(description200," ")
                if description_str == description200_str :
                        count_a +=1
                        per_count += 1
                        percentage = (per_count / total) *100
                        if int(percentage) != int(percent_temp):
                                result = str(int(percentage))+"%"
                                print '\r{0}'.format(result),
                                percent_temp = percentage
                        content200.remove(sentence)
                        break
        if count_a == 0:
                line = line[:-1]
                id_raw = line.split()
                id = id_raw[0]
                line2 =  str(string.join(id_raw[1:]," "))
                b_id[count_200]=str(id)
                b[count_200] = line2
                count_200 +=1
                total_a +=1
        count_a =0

count_b=0

for line in content200:
        description_raw = line.split()
        description = description_raw[0]
        description_str = string.join(description," ")
        for sentence in content009:
                description009_raw = sentence.split()
                description009 = description009_raw[0]
                description009_str = string.join(description009," ")

                if description_str == description009_str :
                        count_b +=1
                        per_count += 1
                        #print per_count
                        percentage = (per_count / total) *100
                        #print percentage
                        #print total
                        if int(percentage) != int(percent_temp):
                                result = str(int(percentage))+"%"
                                print '\r{0}'.format(result),
                                percent_temp = percentage
                        content009.remove(sentence)
                        break
        if count_b == 0:
                line = line[:-1]
                id_raw = line.split()
                id = id_raw[0]
                line2 = str(string.join(id_raw[1:]," "))
                a_id[count_009]=str(id)
                a[count_009] = line2
                #print line
                count_009 +=1
                total_b +=1
        count_b =0

if total_a>total_b:
        length = total_a
else:
        length = total_b

count =1
item =0
while item <length:
        log_diff.write("""<tr>
  <td style="width: 30px">"""+str(count)+"""</td>
  <td style="width: 400px"><a href='https://review-android.quicinc.com/#/q/"""+a_id[count-1]+""",n,z' target='_blank'>"""+a[count-1]+"""</a></td>
  <td style="width: 400px"><a href='https://review-android.quicinc.com/#/q/"""+b_id[count-1]+""",n,z' target='_blank'>"""+b[count-1]+"""</a></td>
  </tr>
</tr>""")
        count+=1
        log_diff.write("\n")
        item +=1
result ="100%"
print '\r{0}'.format(result),



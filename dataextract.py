import glob
import re, urllib2


def course(url):

	response = urllib2.urlopen(url)
	content = response.read()

	# content = content.encode("utf8")
	x=""
	for item in content.split("<!-- END COURSES OFFERED SECTION-->"):
		if '<!-- START COURSES OFFERED SECTION -->' in item:
			x+=  item [item.find('<!-- START COURSES OFFERED SECTION -->')+len('<!-- START COURSES OFFERED SECTION -->') : ]
	lis=[]
	for item in x.split("</li>"):
		if('<li>') in item:

			final = item [item.find('<li>')+len('<li>') : ]
			mylist = re.split(' \xe2\x8b\x84 | &diam; | : |-',final)
			lis.append(mylist)
	for idx,item in enumerate(lis):
		print("Sr No.: " + str(idx))
		print("Start Year: " + item[0].replace(" ",""))
		print("End Year: " + item[1])
		print("Semester: " + item[2])
		print("Course Code: " + item[3])
		print("Course Name: " + item[4].replace("&amp;","&"))
		print("")

url=raw_input()

course(url)
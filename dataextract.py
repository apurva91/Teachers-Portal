import re, glob

def course():
	response = open('abc.txt','r')
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
		print "Sr No.: " + str(idx)
		print "Start Year: " + item[0].replace(" ","")
		print "End Year: " + item[1]
		print "Semester: " + item[2]
		print "Course Code: " + item[3]
		print "Course Name: " + item[4].replace("&amp;","&")
		print ""

def Profile():
	f = open('abc.txt', 'r')
	content = f.read()
	x=""
	for item in content.split("<!-- END PROFILE INFO SECTION -->"):
		if '<!-- START PROFILE INFO SECTION -->' in item:
			x+=  item [item.find('<!-- START PROFILE INFO SECTION -->')+len('<!-- START PROFILE INFO SECTION -->') : ]
	lis=[]

	for item in x.split("\" alt=\""):
		if '<img src=\"' in item:
			lis.append("iitg.ernet.in"+ item [item.find('<img src=\"')+len('<img src=\"') : ])

	for item in re.split('<br />|</p>',x):
		if ':' in item:
			lis.append(item [item.find(':')+len(':') : ])
	lis.pop()

	for idx,item in enumerate(x.split("</div>")):
		if '<p>' in item:
			if idx==1:
				for idx,item2 in enumerate(item.split("</label>")):
					if '<label>' in item2:
						lis.append(item2 [item2.find('<label>')+len('<label>') : ])

				y = (item [item.find('<p>')+len('<p>') : ])
				v = re.split("<br />|,",y)
				lis.append(v[0])
				lis.append(v[1])

	print(lis)

def Publications():
	f = open('abc.txt', 'r')
	content = f.read()
	x=""
	for item in content.split("<!-- END Publications SECTION -->"):
		if '<!-- START Publications SECTION -->' in item:
			x+=  item [item.find('<!-- START Publications SECTION -->')+len('<!-- START Publications SECTION -->') : ]
	lis=[]
	pub=[]
	for item in x.split("</p>"):
		if '<p align="justify">' in item:
			pub.append(item [item.find('<p align="justify">')+len('<p align="justify">') : ])

	for idx,item in enumerate(pub):
		print "\nSr No.: "+str(idx)
		print item.split('"')[0][:-2]
		print item.split('"')[1]
		print item.split(item.split('"')[1])[1][3:]


def Books():
	f = open('abc.txt', 'r')
	content = f.read()
	x=""
	for item in content.split("<!-- END BOOKS/BOOK CHAPTERS SECTION -->"):
		if '<!-- START BOOKS/BOOK CHAPTERS SECTION -->' in item:
			x+=  item [item.find('<!-- START BOOKS/BOOK CHAPTERS SECTION -->')+len('<!-- START BOOKS/BOOK CHAPTERS SECTION -->') : ]
	lis=[]
	pub=[]
	for item in x.split("</p>"):
		if '<p align="justify">' in item:
			pub.append(item [item.find('<p align="justify">')+len('<p align="justify">') : ])

	for idx,item in enumerate(pub):
		print "\nSr No.: "+str(idx)
		print item.split('"')[0][:-2]
		print item.split('"')[1]
		print item.split(item.split('"')[1])[1][4:]

def Education():
	f = open('abc.txt', 'r')
	content = f.read()
	x=""
	for item in content.split("<!-- END ACADEMIC PROFILE SECTION -->"):
		if '<!-- START ACADEMIC PROFILE SECTION -->' in item:
			x+=  item [item.find('<!-- START ACADEMIC PROFILE SECTION -->')+len('<!-- START ACADEMIC PROFILE SECTION -->') : ]
	lis=[]
	pub=[]
	for item in x.split("</p>"):
		if '<p align="justify">' in item:
			pub.append(item [item.find('<p align="justify">')+len('<p align="justify">') : ])
	for item in pub:
		for item2 in item.split("</strong>"):
			if '<strong>' in item2:
				print item2 [item2.find('<strong>')+len('<strong>') : ]
		for item2 in item.split(","):
			if '<br />' in item2:
				print item2 [item2.find('<br />')+len('<br />') : ].replace("\n","").replace("\t","")
		print item.split(",",1)[-1][1:-7]
		print item.split(",")[-1][1:-1]


	# for idx,item in enumerate(pub):
	# 	print "\nSr No.: "+str(idx)
	# 	print item.split('"')[0][:-2]
	# 	print item.split('"')[1]
	# 	print item.split(item.split('"')[1])[1][4:]

def CrawlGet(start,end,code):
	urls=[]
	for item in code.split(end):
		if start in item:
			urls.append(item [item.find(start)+len(start) : ])
	return urls


def Projects():
	f = open('abc.txt', 'r')
	content = f.read()
	x=""
	for item in content.split("<!-- END SPONSORED RESEARCH PROJECTS SECTION -->"):
		if '<!-- START SPONSORED RESEARCH PROJECTS SECTION -->' in item:
			x+=  item [item.find('<!-- START SPONSORED RESEARCH PROJECTS SECTION -->')+len('<!-- START SPONSORED RESEARCH PROJECTS SECTION -->') : ]
	lis=[]
	pub=[]
	for item in x.split("</p>"):
		if '<p align="justify">' in item:
			pub.append(item [item.find('<p align="justify">')+len('<p align="justify">') : ])

	for item in pub:
		print CrawlGet('<strong>','<br />', item)
	# for idx,item in enumerate(pub):
	# 	print "\nSr No.: "+str(idx)
	# 	print item.split('"')[0][:-2]
	# 	print item.split('"')[1]
	# 	print item.split(item.split('"')[1])[1][4:]

print "\nCourses:"
course()
print "\nProfile:"
Profile()
print "\nPublications:"
Publications()
print "\nBOOKS:"
Books()
print "\nEducation:"
Education()
print "\nProjects:"
Projects()

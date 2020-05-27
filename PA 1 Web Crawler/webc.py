from bs4 import BeautifulSoup as bs
import requests as req
import urllib.parse as up
from urllib.parse import urlparse
import time
import os

'''
webcrawl_weber takes input from user.
In while loop, it requests and download .text of response and write it to .html file. 
url duplication is handled. further, if there's a link that leaves orignal domain given by user (external links), 
it will also be ignored (to stop infinite looping). 
Once url is requested, it won't be requested again
'''

links = []
newdir_path = ""
invalid_characters = ['|',"\\",':','*','"', "/",'<','>']


def create_directory():
	try:
		current_directory = os.getcwd()
		folder_name = "\\website"
		global newdir_path
		newdir_path = current_directory + folder_name

		if not os.path.isdir(newdir_path):
			os.makedirs(newdir_path)
		else:
			pass
	except IOError as exception:
		raise IOError("Error: {}".format(exception))


def website_domain(weblink):
	#temp = urlparse(weblink).hostname
	temp = weblink.split("://")[-1].split("/")[0]
	if "www." in temp:
		local = temp.split(".")
		#print ("local")
		#print (local)
		local = ".".join(local[1:])
		return local
	else:
		return temp


def crawl_web(url):
	count = 0
	original_url = links[0]
	#slash_count = original_url.count("/")

	#print ("slash_count: " + str(slash_count))
	create_directory()
	original_domain = website_domain(original_url)
	print ("\noriginal domain: " + str(original_domain))

	while(count < len(links)):
		print ("No. of links in list: " + str(len(links)))
		try:
			print ("\nrequesting url: \n" + str(links[count]))
			response = req.get(links[count], timeout=8)
			current_url = links[count]

			if response.status_code == 200:
				soup = bs(response.content, "html.parser")
				page_name = soup.title.string + ".html"

				#remove invlid characters from page title string of soup
				for x in invalid_characters:
					page_name = page_name.replace(x, '')
				
				filepath = os.path.join(newdir_path, page_name)
				
				#print ("filepath: " + str(filepath))
				with open(filepath, 'w', encoding="utf-8") as file:
					file.write(response.text)
				print ("requested url downloaded :)")
				print ("\npages downloaded so far: " + str(count + 1))
				
				for link in soup.findAll('a'):
					# for removing duplication of weblinks
					temp_url = link.get('href')
					new_url = up.urljoin(original_url, temp_url)
					#print (new_url)

					if not new_url.endswith('/'):
						new_url = new_url + "/" 

					#links with # downlaod same page again and again that add data duplication and extra-storage use 
					if "#" in new_url:
						continue
					
					if new_url not in links:
						temp_domain = website_domain(new_url)
						# for ignoring external links that will lead outside the original webdomain entered by user

						if original_domain in temp_domain:
							links.append(new_url)
						'''
						else:
							print ("ignored url: " + str(new_url))
							print ("ignored domain: " + str(temp_domain))
						'''
				count = count + 1
				time.sleep(1.5)
			else:
				print ("Error: Unexpected response from server. Error code: " + str(response.status_code))
				print ("Moving to next url is list")
				del links[count]
				count = count + 1
				time.sleep(1.5)

		except req.exceptions.RequestException as exception:
			print ("Error: {}".format(exception))
			print ("Moving to next url")
			del links[count]
			count = count + 1
			time.sleep(1.5)


	print ("\nSuccessfully downloaded webpages from orignal url are:\n")
	print (*links, sep='\n')
	print ("\nWebcrawling of url " + str(links[0] + " has been completed."))
	print ("\nNo. of pages downloaded successfully: " + str(len(links)))


def main():
	url = ''
	print("Enter URL for crawling")
	url = input()
	if not url.endswith('/'):
		url = url + "/"
	links.append(url)
	crawl_web(url)
	return 0


if __name__ == "__main__":
    main()
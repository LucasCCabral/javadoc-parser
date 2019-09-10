#!/usr/bin/env python3
'''
 * Created by Lucas Costa Cabral.
 * Email: lucascostacabra@gmail.com
 * Date: 04/09/19
'''
import glob
import os
from bs4 import BeautifulSoup
PRJ_NAME = "zookeeper"

KEYWORDS = ["must",
	"should",
	"has",
	"hasn't",
	"shall",
	"ensure"
]

CHILDREN_TAGS=[
	"pre",
	"div"
]


def get_separator(sep, quantity = 20):
	return sep*quantity

class parsed_method(object):
	METHOD_NAME_TAG = "h4"
	METHOD_DESCRIPTION_TAG = "div"

	name = ""
	description = list()
	anchor = ""

	def __init__(self, method, soup):
		self.name = method.find(self.METHOD_NAME_TAG).get_text(' ', strip=True)
		self.set_description(method)
		self.set_anchor(soup)

	def set_description(self, method):
		"""
			Each method may habe more than one description.
		"""
		for method_description in method.findAll(self.METHOD_DESCRIPTION_TAG):
			self.description.append(method_description.get_text(' ', strip=True))
	
	def set_anchor(self, soup):
		"""
			Gets the anchor to the method javadoc.
		""" 

		link_block = soup.findAll("span", class_="memberNameLink")
		for link in link_block:
			link_tag = link.find("a")
			if(self.name == link_tag.string):
				self.anchor = "file://" + os.getcwd() + "/" + str(link_tag.get('href')).replace("../","")
				break

	def print(self):
		print("Method Name: " + self.name)
		for descr in self.description:
			print("Description: " + descr)
		print("Anchor: " + self.anchor)
		print(get_separator("-"))


class parsed_class(object):

    METHOD_DETAIL = "Method Detail"
    METHOD_SUMMARY = "Method Summary"

    file_ = ""	
    methods = list()
    # The class "constructor" - It's actually an initializer 
    def __init__(self, file):
        self.file_ = file

    def add_method(self, method):
    	self.methods.append(method)	

    def get_container(self, soup, desired_value):
        """
			Returns the desired container of the desired value or False
			in case it doesn't exist.
        """
        html_tag = soup.find_all("h3")
        if html_tag == None:
        	return False
        else: 
	        for tag in html_tag:
	            if(tag.string == desired_value):
	                return tag.parent

    def get_methods(self, method_container):
        methods = list()
        for method_detail in method_container.find_all():
            if(method_detail.name == "ul"):
                methods.append(method_detail)
        return methods

    def print(self):
    	print(get_separator("*"))
    	print("Class Name: " + self.file_)
    	print(get_separator("-"))
    	for method in self.methods:
    		method.print()
    	print(get_separator("*"))


class parsed_project(object):
	prj_name = ""
	classes = list()

	def __init__(self, prj_name):
		self.prj_name = prj_name

	def add_class(self, class_):
		self.classes.append(class_)

	def log_file(self):
		"""
			Should write the result to a log file.
		"""
		with open(self.prj_name+".txt", "w") as log_file:
			for class_ in self.classes:
				log_file.write(get_separator("*") + '\n')
				log_file.write(class_.file_ + '\n')
				log_file.write(get_separator("*") + '\n')
				log_file.write(get_separator("-") + '\n')
				for method in class_.methods:
					if(method.method_description != []):
						log_file.write("Method Name: " + method.method_name + '\n')		
						for description in method.method_description:
							for keyword in KEYWORDS:
								if(keyword in description):
									log_file.write("Description: " + description + '\n')
									break
						log_file.write("Method Anchor: " + method.method_anchor + '\n')
						log_file.write(get_separator("-") + '\n' )

def find_pattern(query):
	"""
		Uses the query specified to find all files that match the queries 
		pattern.
		@param query the pattern that will be used to find items,
		@returns a list with all the java files found in dir.
	"""
	return  glob.glob(query, recursive=True)


def documented(methods_details_container):
	"""
		Checks if the current class has any documentation.
	"""
	method_details_tags = [x.name for x in methods_details_container.find_all()]
	
	# checks if the method detail has all needed descripitions
	for tag in CHILDREN_TAGS:
		if (not tag in method_details_tags):
			return False

	return True

def has_method_detail(soup):
	"""
		Looks for the "method.detail" id in the given soup
		objects.
	"""
	method_detail = soup.find("a", {"id" : "method.detail"})
	if(method_detail == None):
		return False
	return True

def get_anchor(method):
	"""
		Gets the anchor to the method javadoc.
	"""
	for link in method.find_all("a"):
		if(link.get_text(' ', strip=True) == method.h4.string):
			return "file://" +PROJECT_DIR + str(link.get('href')).replace("../","")
	return "no anchor"
	#raise Exception('This method signature has not been associated with a file.')


def get_method_summary(soup):
	"""
	"""
	method_summary = soup.find_all("h3")
	
	for val in method_summary:
		if(val.string == METHOD_SUMMARY):
			print("this one has")
			return val.parent
	
	return False


def get_methods(soup):

	if(not has_method_detail(soup)):
		return []

	methods_details_container = soup.find("a", {"id" : "method.detail"}).parent
	methods = list()	
	for method_detail in methods_details_container.find_all():
		if(method_detail.name == "ul"):
			methods.append(method_detail)

	return methods

def filter_by_documentation(file_list):
	"""
		Receives a list with the fully specified path of the files and filters the 
		files by the presence of documentation.
	"""
	p = parsed_project(PRJ_NAME)

	for file_ in file_list:
		curr_class = parsed_class(file_)
		with open(file_, "r") as f:
			soup = BeautifulSoup(f, 'html.parser')
			print("Examining file " + str(file_list.index(file_)) +
			 " of "  + str(len(file_list)))
			#creates a BeautifulSoup element with the html file
			method_detail = curr_class.get_container(soup, curr_class.METHOD_DETAIL)
			method_summary = curr_class.get_container(soup, curr_class.METHOD_SUMMARY)
			if(method_detail != None):
				methods = curr_class.get_methods(method_detail)
				for method in methods:
					print(file_)
					method = parsed_method(method, soup)
					method.print()

			"""
			methods = get_methods(soup)
			for method in methods:
				if(method.h4 != None):
					# gets the method name
					method_name = method.h4.string
					# gets the  method anchor
					method_anchor = get_anchor(method)
					# list of method descriptions
					method_descriptions = list()
					if(documented(method)):	
						# a method may have more than one "div field", with(apparently) no way
						# of differentiating between the others e.g.: when a method description
						# is copied from another method.		
						for tag in method.find_all("div"):
							method_descriptions.append(tag.get_text(' ', strip=True))
						#create a method object for this class

					curr_method = parsed_method(method_name, method_descriptions[:], method_anchor)
					#appends the former method to the current class being analysed
					method_descriptions.clear()
					curr_class.add_method(curr_method)		
				p.add_class(curr_class)
			#prints the information
			#curr_class.print()
			"""
	return p

def main():
	my_query = os.getcwd() + "/**/*.html"
	my_files = find_pattern(my_query)
	res = filter_by_documentation(my_files)
	res.log_file()

if __name__ == "__main__":
	main()

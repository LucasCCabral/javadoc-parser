from parsed_method import ParsedMethod
from bs4 import BeautifulSoup

class ParsedClass(object):

    METHOD_DETAIL = "Method Detail"
    METHOD_SUMMARY = "Method Summary"
    ANCHOR_TAG = 'a'

    file_ = ""	
    methods = list()
    soup = None
    # The class "constructor" - It's actually an initializer 
    def __init__(self, file):
        self.file_ = file

    def add_method(self, method):
    	self.methods.append(method)	

    def mine_container(self):
        """
		Returns the desired container of the desired value or False
		in case it doesn't exist.
        """
        html_tag = self.soup.find_all("h3")
        if html_tag == None:
        	return False
        else: 
	        for tag in html_tag:
	            if(tag.string == self.METHOD_DETAIL):
	                return tag.parent

    def mine_methods(self, method_container):
        methods = list()
        for method_detail in method_container.find_all():
            if(method_detail.name == "ul"):
                methods.append(method_detail)
        return methods

    def mine_anchors(self, method_container):
    	anchors = list()
    	for tag in method_container.find_all(self.ANCHOR_TAG):
    		anchor = tag.attrs.get("name")
    		if(anchor != None and anchor != "method.detail"):
        		print(anchor)
        		anchors.append(anchor)
    	
    	return anchors

    def get_all_methods(self):

        with open(self.file_, "r") as f:
            self.soup = BeautifulSoup(f, 'html.parser')
            method_container = self.mine_container()
            if(method_container != False and method_container != None):
                methods = self.mine_methods(method_container)
                anchors = self.mine_anchors(method_container)
                print(self.file_)
                #print(mine_anchors)

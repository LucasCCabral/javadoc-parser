from parsed_method import ParsedMethod
from bs4 import BeautifulSoup

class ParsedClass(object):

    METHOD_DETAIL = "Method Detail"
    METHOD_SUMMARY = "Method Summary"
    ANCHOR_TAG = 'a'
    CLASS_SEPARATOR="************************************************************************* \n"
    METHOD_SEPARATOR="------------------------------------------------------------------------- \n"

    file_ = ""	
    soup = None
    # The class "constructor" - It's actually an initializer 
    def __init__(self, file):
        self.file_ = file
        self.class_methods = list()


    def add_method(self, method):
    	self.class_methods.append(method)	

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
            if(method_detail.name == "ul" and method_detail.h4 != None):
                methods.append(method_detail)
        return methods

    def mine_anchors(self, method_container):
    	anchors = list()
    	for tag in method_container.find_all(self.ANCHOR_TAG):
    		anchor = tag.attrs.get("name")
    		if(anchor != None and anchor != "method.detail"):
        		anchors.append(anchor)
    	
    	return anchors

    def get_all_methods(self):

        with open(self.file_, "r") as f:
            self.soup = BeautifulSoup(f, 'html.parser')
            method_container = self.mine_container()
            if(method_container != False and method_container != None):
                methods = self.mine_methods(method_container)
                anchors = self.mine_anchors(method_container)
                #(method, anchor, file_path)
                if(len(methods) != len(anchors)):
                    pass
                    #raise Exception("The number of methods(#{}) is different from the number of anchors(#{}).\r File:".format(len(methods), len(anchors)))
                for method, anchor in zip(methods, anchors):
                    parsed_method = ParsedMethod(method, anchor, self.file_)
                    self.class_methods.append(parsed_method)

    def log_class(self, dest_file):

        with open(dest_file, "a") as log_file:
            log_file.write(self.CLASS_SEPARATOR)
            log_file.write("Class: " + self.file_ + "\n")
            log_file.write(self.CLASS_SEPARATOR)
            log_file.write(self.METHOD_SEPARATOR)
             
            for method in self.class_methods:

                if(method.description == []):
                    break

               log_file.write("Method Name: " + method.name + '\n')
                
                for description in method.description:
                    log_file.write("Description: " + description + '\n')
                
                if(len(method.description) == 0):
                    log_file.write("Description: None")
                
                log_file.write("Method Anchor: " + method.anchor + '\n')        
                log_file.write(self.METHOD_SEPARATOR)

import glob
import os
from parsed_class import ParsedClass

class ParsedProject(object):
	prj_path = ""
	classes = list()

	def __init__(self, prj_path):
		self.prj_path = prj_path

	def find_all_html(self, query):
		"""
		Uses the query specified to find all html files in the folder.
		@param query the pattern that will be used to find items,
		@returns a list with all the java files found in dir.
		"""
		return  glob.glob(self.prj_path, recursive=True)


	def add_class(self, class_):
		"""
		Appends a class to the project classes.
		"""
		self.classes.append(class_)

	def get_all_classes(self):
		for file_ in self.find_all_html(self.prj_path):
			class_ = ParsedClass(file_)
			class_.get_all_methods()

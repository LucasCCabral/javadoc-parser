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
		html_query = self.prj_path + "**/*.html"
		return  glob.glob(html_query, recursive=True)


	def add_class(self, class_):
		"""
		Appends a class to the project classes.
		"""
		self.classes.append(class_)

	def get_all_classes(self):

		all_html_files = self.find_all_html(self.prj_path)
		for file_ in all_html_files:
			class_ = ParsedClass(file_)
			class_.get_all_methods()			
			self.classes.append(class_)
			print("Parsing file #{} of #{}.".format(self.classes.index(class_), len(all_html_files)))

	def gen_log_file(self, dest_file):

		try:
		    os.remove(dest_file)
		except OSError:
		    pass

		for class_ in self.classes:
			if(class_.class_methods!= []):
				class_.log_class(dest_file)

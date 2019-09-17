#!/usr/bin/env python3
from parsed_project import ParsedProject

PROJECT_PATH = "/home/lucas/workspace/eng-teste/prj/zookeper2/"
LOG_PATH = "/home/lucas/workspace/eng-teste/prj/javadoc-parser/log.txt"

p = ParsedProject(PROJECT_PATH)
p.get_all_classes()
p.gen_log_file(LOG_PATH)

# -*- coding: utf-8 -*-
import os

def switch_path_relative(absolute_path, keyword):
    idx = absolute_path.index(keyword)
    path = "\\" + absolute_path[idx:]
    path = '/'.join(path.split("\\"))
    return path

# -*- coding: utf-8 -*-"
"""
Spyder Editor

mapper.py

Tim Drysdale 28 Feb 2024 Created
"""
import graphviz
import yaml

with open('example.yaml', 'r') as file:
    definition = yaml.safe_load(file)

pages = definition["pages"]

dot = graphviz.Digraph('links', comment='link map')
dot.graph_attr.update({'rankdir': 'BT'})

names = [] #known names list for checking parents and links

# first pass, record nodes
for page in pages:
    name = ""
    
    if "name" in page:
        name = page["name"].lower() #avoid forcing users to be strict on capitalisation
        
    if "label" in page:
        label = page["label"]
    else:
        label = name.replace("_", " ").title()
    
    if not name == "":
        names.append(name)
        dot.node(name, label, shape="box")   
   
for page in pages:
    if "name" in page: #sanity check there is a name
        name = page["name"].lower()
        if "parent" in page: #ignore parent link if not included 
            parent = page["parent"].lower() #avoid forcing users to be strict on capitalisation
            
            if not parent in names:
                print("warning: " + name + " has parent " + parent + " but it is missing")
            
            dot.edge(name, parent, color="blue")
        else:
            if not name == "home":
                print("warning: " + name + " does not have a parent")
            
    
for page in pages:
    if "name" in page: #sanity check there is a name
        name = page["name"].lower() #avoid forcing users to be strict on capitalisation
        if "links" in page: #ignore parent link if not included 
            for link in page["links"]:
                link = link.lower() #avoid forcing users to be strict on capitalisation
                dot.edge(name, link, color="red", constraint="false")
        else:
            if not name == "home":
                print("warning: " + name + " does not have a parent")
            

#
dot.render(directory='doctest-output', view=True)  
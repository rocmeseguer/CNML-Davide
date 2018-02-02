#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import collections

from igraph import *

def cnmlReader(filename):
    gr = Graph()
    nv_dict = dict()
    node_id = 0

    tree = ET.parse(filename)
    elem = tree.getroot()

    for parent in tree.getiterator():
        for child in parent:
            if child.tag == "node" and child.get("status") == "Working":
                nv_dict[child.get("id")] = node_id
                node_id = node_id + 1
                gr.add_vertex(name = child.get("id"))

                for d in child.findall("device"):
                    for r in d.findall("radio"):
                        for i in r.findall("interface"):
                            for l in i.findall("link"):
                                if l.get("link_status") == "Working":
                                    from_name = child.get("id")
                                    to_name = l.get("linked_node_id")

                                    if (from_name != to_name):

                                        if nv_dict.get(from_name) is None:
                                            nv_dict[from_name] = node_id
                                            node_id = node_id + 1
                                            gr.add_vertex(name = str(from_name))

                                        if nv_dict.get(to_name) is None:
                                            nv_dict[to_name] = node_id
                                            node_id = node_id + 1
                                            gr.add_vertex(name = str(to_name))

                                        gr.add_edge(str(from_name), str(to_name))


    return(gr)

def servicesReader(filename):
    services_dict = defaultdict(list)

    with open(filename, 'r') as input_file:
        for s in input_file.readlines():
            info = s.split("|")

            node_name = info[0]
            services = info[1].rstrip()

            for service in services.split(","):
                services_dict[service].append(node_name)

    input_file.close()

    return services_dict

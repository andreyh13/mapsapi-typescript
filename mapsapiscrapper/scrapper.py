import urllib
import libxml2dom
import re


class GoogleMapsAPIScrapper:
    '''This class is responsible for scrapping of Maps JavaScript API docs'''

    def __init__(self, path, nodes):
        sock = urllib.urlopen(path)
        html_source = sock.read()
        sock.close()
        doc = libxml2dom.parseString(html_source, html=1)
        self.content = doc.getElementById("gc-wrapper")
        self.wrapper = self.__get_wrapper()
        self.__nodes = nodes
        self.__collect_nodes()

    def __get_wrapper(self):
        wrapper = None
        node = self.__get_child_node_first(
            self.content.childNodes, 'div', None, 'devsite-main-content clearfix')
        if node is not None:
            node = self.__get_child_node_first(node.childNodes, 'article')
        if node is not None:
            node = self.__get_child_node_first(
                node.childNodes, 'div', 'article', 'devsite-article-inner')
        if node is not None:
            wrapper = self.__get_child_node_attribute_first(
                node.childNodes, 'div', 'itemprop', 'articleBody')
        return wrapper

    def __get_child_node_first(self, parent_nodes, tag_name, tag_name1=None, class_name=None):
        res = None
        for node in parent_nodes:
            if (node.tagName == tag_name or (node.tagName == tag_name1 and tag_name1 is not None)) and (class_name is None or (class_name is not None and node.hasAttribute('class') and node.getAttribute('class') == class_name)):
                res = node
                break
        return res

    def __get_child_node_attribute_first(self, parent_nodes, tag_name, attribute, attr_value):
        res = None
        for node in parent_nodes:
            if node.tagName == tag_name and node.hasAttribute(attribute) and node.getAttribute(attribute) == attr_value:
                res = node
                break
        return res

    def __collect_nodes(self):
        if self.wrapper is not None:
            for node in self.wrapper.childNodes:
                if node.tagName == 'div' and node.hasAttribute('itemscope') and node.hasAttribute('itemtype') and node.getAttribute('itemtype') == 'http://developers.google.com/ReferenceObject':
                    self.__nodes.add_node(node)

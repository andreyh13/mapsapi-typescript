class GoogleMapsAPIDocNodes:
    '''This class collects nodes from the API documentation'''

    def __init__(self):
        self.__nodes = list()

    def add_node(self, node):
        self.__nodes.append(node)

    def get_nodes(self):
        return self.__nodes

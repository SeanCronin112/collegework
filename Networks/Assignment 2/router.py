import pandas as pd 
import math

class Router(object):
    def __init__(self, name, graph):
        self.name = name 
        self.graph = graph

        # shortest_distance_from_start_node is a dictionary containing all the values of the router names, and the distance they are through the quickest path from the start node.
        # Initially, they are set to math.inf, meaning the distacne between them is not yet known. The shortest_distance of the router name is set to 0, because that;s the
        self.shortest_distance_from_start_node = {}

        for value in self.graph.router_list:
            self.shortest_distance_from_start_node[value] = math.inf
        self.shortest_distance_from_start_node[self.name] = 0

        #self.shortest_distance_from_start_node_copy is a clone of the shortest_distances_from_start_node, which allows it to reset the shortest distances each time the get_path function is called.
        #This means that when a router is removed, it can start from scratch.
        self.shortest_distance_from_start_node_copy = dict(self.shortest_distance_from_start_node)

    def get_path(self, router_name):

        """ Description
        :type self: Router
        :param self: The current router

        :type router_name: string
        :param router_name: The name of the router that you want to find the path of.

        :raises:

        :rtype: Tuple(length path travels from start to goal, path it took to travel from start to goal)
        """
        start = self.name
        goal = router_name
        graph_list = self.graph.graph_list

        #unseenNodes is a list of the nodes that t a
        unseenNodes = graph_list
        track_predecessor = {}
        track_path = []
    
        self.shortest_distance_from_start_node = dict(self.shortest_distance_from_start_node_copy)
        graph_list_holder = dict(self.graph.graph_list)

        #This Loop preforms the Dijkstras Algorithm, and adds the path it takes to the track_path variable.

        while unseenNodes:
            minimum_distance_from_start_node = None
            for node in unseenNodes:
                if minimum_distance_from_start_node is None:
                    minimum_distance_from_start_node = node
                elif self.shortest_distance_from_start_node[node] < self.shortest_distance_from_start_node[minimum_distance_from_start_node]:
                    minimum_distance_from_start_node = node
                
            path_options = graph_list[minimum_distance_from_start_node].items()

            for child_node, distance in path_options:
                if distance + self.shortest_distance_from_start_node[minimum_distance_from_start_node] < self.shortest_distance_from_start_node[child_node]:
                    self.shortest_distance_from_start_node[child_node] = distance + self.shortest_distance_from_start_node[minimum_distance_from_start_node]
                    track_predecessor[child_node] = minimum_distance_from_start_node

            unseenNodes.pop(minimum_distance_from_start_node)

        self.graph.graph_list = graph_list_holder

        currentNode = goal

        while currentNode != start:
            if currentNode not in track_predecessor.keys():
                break
            else:
                track_path.insert(0, currentNode)
                currentNode = track_predecessor[currentNode]

        track_path.insert(0, start)

        if goal in self.shortest_distance_from_start_node.keys():
            if self.shortest_distance_from_start_node[goal] != math.inf:
                return (self.shortest_distance_from_start_node[goal],  '->'.join(track_path))
        else:
            return 'No Path could be found.'

    #The following 4 functions are primarily to be used in the print_routing_table function.

    #This function takes the router_list of all different nodes, and returns a list of the path nodes that are not the start node.
    def generate_different_nodes(self):    
        """ Description:     This function takes the router_list of all different nodes, and returns a list of the path nodes that are not the start node.
        :type self: Router
        :param self: The Current Router
    
        :rtype: List
        """

        return sorted([node for node in self.graph.router_list if node != self.name])

    def generate_start_nodes(self):
        
        """ Description: This function takes the different_nodes list, and makes a list equal in length containing only the name of the current router.
        :type self: Router
        :param self: Current Router

        :rtype: List
        """
        
        return [self.name for node in self.generate_different_nodes() if node != self.name]

    #This function makes a list of the paths by calling the get_path function on each of the nodes in generate_different_nodes().
    def generate_quickest_paths(self):
        """ Description: This function makes a list of the paths by calling the get_path function on each of the nodes in generate_different_nodes().

        :type self: Router
        :param self: Current Router

        :rtype: List
        """
        
        paths = []

        for node in self.generate_different_nodes():
            if self.get_path(node) != None:
                paths.append(self.get_path(node)[1])
            else:
                paths.append("No Path!")

        return paths

    #This returns the cost of the paths for the same list.

    def generate_cost_of_quickest_paths(self):
        """ Description:  This returns the cost of the paths for the same list.

        :type self: Router
        :param self: Current Router

        :rtype: List
        """

        costs = []

        for node in self.generate_different_nodes():
            if self.get_path(node) != None:
                costs.append(self.get_path(node)[0])
            else:
                costs.append('')

        return costs

    #Uses the pandas 'from_dict' memory to print out the lists, calling each of the above functions and assigning them to a respective dictionary key.

    def print_routing_table(self):

    
        """ Description: Uses the pandas 'from_dict' memory to print out the lists, calling each of the above functions and assigning them to a respective dictionary key.

        :type self: Router
        :param self: The Current Router
    

        :rtype: None
        """
        pandas_dictionary = {
        'from': self.generate_start_nodes(),
        'to'  : self.generate_different_nodes(),
        'cost': self.generate_cost_of_quickest_paths(),
        'path': self.generate_quickest_paths()
        }

        print(pd.DataFrame.from_dict(pandas_dictionary))

    #Searches through the router graph and removes any instance of the router_name given as an argument.

    def remove_router(self, router_name):

        """ Description:  Searches through the router graph and removes any instance of the router_name given as an argument.

        :type self: Router
        :param self: The Current Router
    
        :type router_name: String
        :param router_name: The name of the router you want to remove.
    
        :raises:
    
        :rtype:
        """    
        
        for value in list(self.graph.graph_list.keys()):
            if value == router_name:
                del self.graph.graph_list[value]
            else:    
                for sub_value in list(self.graph.graph_list[value]):
                    if sub_value == router_name and sub_value in self.graph.graph_list[value]:
                        del self.graph.graph_list[value][sub_value]

        self.graph.router_list = [node for node in self.graph.router_list if node != router_name]

        self.print_routing_table()
        


class Graph(object):
    def __init__(self):
        self.graph_list = {}
        self.router_list = []

    #Graph is represented as a dictionary.pyth

    def add_edge(self, router_1, router_2, distance):
    
        """ Description
        :type self: Graph
        :param self: The current Graph
    
        :type router_1: string
        :param router_1: name of the first router you want to connect
    
        :type router_2: string
        :param router_2: name of the router you want to connect to the first router
    
        :type distance: int
        :param distance: the distance between the two nodes
        
        :rtype: None
        """        
        if router_1 not in self.router_list:
            self.router_list.append(router_1)
        if router_2 not in self.router_list:
            self.router_list.append(router_2)
        if router_1 not in self.graph_list.keys():
            self.graph_list[router_1] = {router_2: distance}
        else:
            self.graph_list[router_1][router_2] = distance


def main():

    router_graph = Graph()

    router_graph.add_edge("a", "b", 7)
    router_graph.add_edge("a", "c", 9)
    router_graph.add_edge("a", "f", 14)
    router_graph.add_edge("b", "c", 10)
    router_graph.add_edge("b", "d", 15)
    router_graph.add_edge("c", "d", 11)
    router_graph.add_edge("c", "f", 2)
    router_graph.add_edge("d", "e", 6)
    router_graph.add_edge("e", "f", 9)

    router = Router('a', router_graph)
    router_two = Router('b', router_graph)
    print("First Routing Table: ")
    router.print_routing_table()

    print("\nSecond Routing Table: ")
    router_two.print_routing_table()

    print("\nUpdated First Routing Table:")
    router.remove_router('c')

    print("Updated Second Routing Table: ")
    router_two.print_routing_table()


if __name__ == "__main__":
    main()
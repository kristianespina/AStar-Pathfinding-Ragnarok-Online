from mapreader import read_map
import matplotlib.pyplot as plt
import numpy as np
import heapq
from datetime import datetime
import collections

class Node:
    
    def __init__(self, parent = None, position : tuple = None, flags : int = 0):
        """ Initializes a node

        Args:
            parent (Node, optional): parent node. Defaults to None.
            position (tuple, optional): coordinates of the node. Defaults to None.
            flags (int, optional): cell type (0 for walkable, 1 for non-walkable). Defaults to 0.
        """
        self.parent = parent
        self.position = position
        self.flags = flags
        
        # Shouldn't this be set to infinity?
        self.f = 0
        self.g = 0
        self.h = 0
     
    def children(self):
        """ Returns the neighboring coordinates

        Returns:
            list: returns a list of tuple
        """
        offsets = [(0,1),(1,0),(0,-1),(-1,0)]
        children = []
        for offset in offsets:
            children.append(self.__add__(offset))
        return children
    
    def distance(self, other):
        """ Returns the distance to the other node

        Args:
            other (Node): target node

        Returns:
            int: distance of the node
        """
        dist = (self.position[0] - other.position[0])**2 + (self.position[1] - other.position[1]) ** 2
        return dist
    
    def __add__(self, offset):
        return (self.position[0] + offset[0], self.position[1] + offset[1])
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other): # used in heapqueue
        return self.f < other.f
    
    def __hash__(self):
        return hash(self.position)
    
    def __str__(self):
        return "Node: ("+str(self.position[0])+","+str(self.position[1])+")"
    
    def __repr__(self):
        return self.__str__()

class Map:
    
    def __init__(self, grid : list):
        """ Creates a Map instance from a given grid

        Args:
            grid (list): 2d grid of 0's and 1's
        """
        self.grid = grid
        
        self.width = len(grid[0])
        self.length = len(grid)
        
    def show(self, src : tuple, dst : tuple, path : list = None):
        """ Displays the map in matplotlib

        Args:
            src (tuple): coordinates of the source
            dst (tuple): coordinates of the direction
            path (list, optional): list of coordinates of route. Defaults to None.
        """
        plt.scatter(src[0], self.length-src[1], s=75, c='red', marker='o')
        plt.scatter(dst[0], self.length-dst[1], s=150, c='yellow', marker='x')

        if path is not None:
            for point in path:
                plt.scatter(point[0], self.length-point[1], s=5, c='yellow', marker='o')

        np_map = np.asarray(self.grid)
        map_colored = np.flip(to_rgb(np_map), axis=0)
        plt.imshow(map_colored)
        
    def get_flags(self, position : tuple):
        """ Returns the cell type of a given coordinate

        Args:
            position (tuple): coordinates

        Returns:
            int: cell type
        """
        return self.grid[position[1]][position[0]]
        
    def astar(self, _src : tuple, _dst : tuple):
        """ Returns the shortest path using A* algorithm

        Args:
            _src (tuple): coordinates of the source
            _dst (tuple): coordinates of the destination

        Returns:
            Node: Node containing info of the route
        """
        src = Node(parent = None, position = _src, flags = self.get_flags(_src))
        dst = Node(parent = None, position = _dst, flags = self.get_flags(_dst))
        
        openSet = set()
        openHeap = []
        closedSet = set()
        
        openSet.add(src)
        openHeap.append((0,src))
        
        while openSet is not None:
            try:
                current = heapq.heappop(openHeap)[1] # Lowest cost from openSet. [0] = cost [1] = Node
            except:
                return None
            #f current in openSet:
            #   openSet.remove(current) # Remove from the open set
            openSet.remove(current)
            closedSet.add(current)
            
            if current == dst:
                return current
            
            for _child in current.children(): # _child : tuple (coordinates)
                child = Node(parent=current, position=_child, flags=self.get_flags(_child))
                
                # Check if child is already visited
                if child in closedSet:
                    continue
                
                # Check if child is walkable cell
                if child.flags != 0:
                    continue
                
                child.g = current.g + 1
                child.h = child.distance(dst)
                child.f = child.g + child.h
                
                # Check if child is not in openSet
                if child not in openSet:
                    openSet.add(child)
                    heapq.heappush(openHeap, (child.f, child))
                    continue
                    
                # If child is in openSet : compare the cost
                for openChild in openSet:
                    if openChild == child and child.f < openChild.f: # Replace if this path is better
                        openSet.remove(openChild)
                        openSet.add(child)
                        # Update Heap
                        openHeap.remove((openChild.f, openChild))
                        heapq.heapify(openHeap)
                        heapq.heappush(openHeap, (child.f, child))
                        continue
    
    def find_path(self, src : tuple, dst : tuple):
        path = self.astar(src, dst)
        if path is not None:
            return node_to_list(path)
        return None

def to_rgb(im):
    """ converts grayscale 2d list to rgb

    Args:
        im (np.array): 2d numpy array

    Returns:
        np.array: np.array with rgb color
    """
    return (np.asarray(np.dstack((im, im, im)), dtype=np.uint8) * 255)

def node_to_list(node : Node):
    """ Retraces path from node into a list of coordinates (tuple)

    Args:
        node (Node): end node

    Returns:
        collections.deque: list of coordinates (tuple)
    """
    # https://stackoverflow.com/questions/8537916/whats-the-idiomatic-syntax-for-prepending-to-a-short-python-list
    # deques are more performant than list on longer lists
    route = collections.deque()
    while node is not None:
        route.appendleft((node.position[0], node.position[1]))
        node = node.parent
    return route

"""
Usage:
src = (x,y)
dst = (x,y)
path = pathfinder.astar(src, dst)
pathlist = node_to_list(path)
pathfinder.show_path(src, dst, pathlist)

# or
path = pathfinder.find_path(src, dst)
pathfinder.show_path(src, dst, path)
"""
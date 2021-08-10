# -*- coding: utf-8 -*-
"""
(c) 2021 James & Anshul
Date: 7/11/2021
Name: James Rozsypal & Anshul Chauhan
Student ID: 015668339 & 016246735
Email: james.rozsypal@student.csulb.edu & anshul.chauhan@student.csulb.edu
"""


class Maze(object):
    # Initialize the maze
    def __init__(self, maze):
        # Create an empty graph to store a maze
        self.g = Graph()
        
        # Load in the maze thorugh the .lay file 
        self.m = open(maze, 'r')
        
        # Track rows and coloumns of the maze
        self.rows = 0
        self.columns = 0
        
        # Building the matrix using the maze.lay file
        lines = []
        self.matrix = []
        for l in self.m:
            # increment rows by 1 each time a new line is read
            self.rows += 1
            # add the line to the set of lines
            lines.append(l)
            # the length of the line is the number of coloumns within that line
            self.columns = len(l)            
            # Make a matrix of the maze
            self.matrix += [list(l)]
        
        # Make a Graph of the maze using the matrix we just created
        self.Graph_Maze()
        
        # Instantiate the start and target indices using the matrix
        self.Start()
        self.Target()
        
    
    # Find the start of the maze indicated by 'P'    
    def Start(self):
        # Use the matrix we created in __init__ to find the start of the maze
        # for each row in the matrix...
        for row in range(len(self.matrix)):
            # ...assess each coloumn within the row
            for column in range(len(self.matrix[row])):
                # if the node at (row, coloumn) is equal to 'P' then we've found the start of the maze
                if self.matrix[row][column] == 'P':
                    # record the starting position
                    self.s = (row, column)

        
    # Find the target in the maze indicated by '.'
    def Target(self):
        # Use the matrix we created in __init__ to find the target in the maze
        # for each row in the matrix...
        for row in range(len(self.matrix)):
            # ...assess each coloumn within the row
            for column in range(len(self.matrix[row])):
                # if the node at (row, coloumn) is equal to '.' then we've found the target of the maze
                if self.matrix[row][column] == '.':
                    # record the target position
                    self.t = (row, column)
    


    # Add the verticies of the maze to the graph
    def Graph_Maze(self):
        # for each row in the matrix...
        for row in range(len(self.matrix)):
            # ...assess each coloumn within the row
            for column in range(len(self.matrix[row])):
                if self.matrix[row][column] in [' ','P','.']:
                    # instantiate the adjacent vertices 
                    up = row - 1
                    down = row + 1
                    left = column - 1
                    right = column + 1
                    
                    # set the index of current vertex that we're looking at
                    currV = row * self.columns + column
                    self.g.add_vertex(currV) 
                    
                    
                    # assess the space above the current vertex
                    if up > -1:
                        # if we can move to the vertex above self(current vertex)...
                        if self.matrix[up][column] in [' ','P','.']:
                            # subtract self.columns to get the index of the vertex directly above
                            aboveNeighbour = currV - self.columns
                            
                            # check that the vertex above is within the matrix
                            if aboveNeighbour < (self.rows * self.columns) > -1:
                                # if so then add the edge to the graph
                                self.g.add_edge(currV, aboveNeighbour) 
            
                    # assess the space below the current vertex
                    if down < (self.rows * self.columns):
                        # if we can move to the vertex below self(current vertex)...
                        if self.matrix[down][column] in [' ','P','.']:
                            # add self.columns to get the index of the vertex directly above
                            belowNeighbour = currV + self.columns
                            
                            # check that the vertex below is within the matrix
                            if belowNeighbour < (self.rows * self.columns) > -1:
                                # if so then add the edge to the graph
                                self.g.add_edge(currV, belowNeighbour) 
            
                    # assess the space to the left of the current vertex
                    if left > -1:
                        # if we can move to the vertex to the left of self(current vertex)...
                        if self.matrix[row][left] in [' ','P','.']:
                            # subtract 1 to get the index of the vertex to the left
                            leftNeighbour = currV - 1
                            
                            # check that the vertex to the left is within the matrix
                            if leftNeighbour < (self.rows * self.columns) > -1:
                                # if so then add the edge to the graph
                                self.g.add_edge(currV, leftNeighbour) 
            
                    # assess the space to the right of the current vertex
                    if right < (self.rows * self.columns):
                        # if we can move to the vertex to the right of self(current vertex)...
                        if self.matrix[row][right] in [' ','P','.']:
                            # add 1 to get the index of the vertex to the right
                            rightNeighbour = currV + 1
                            
                            # check that the vertex to the right is within the matrix
                            if rightNeighbour < (self.rows * self.columns) > -1:
                                # if so then add the edge to the graph
                                self.g.add_edge(currV, rightNeighbour)     
     
        
    # BFS Algorithm   
    def BFS(self):
        # FIFO queue 
        fifo = []
        # To track vertices that have been visited
        self.visited = []
        # To track the parents of each vertex
        self.parent = {}
        
        # Save the start and target indicies 
        start = self.s[0] * self.columns + self.s[1]
        target = self.t[0] * self.columns + self.t[1]
        
        # Set the starting vertex as visited
        self.visited.append(start)
       
        # Set the current vertex as the vertex at the starting index to begin
        curr = self.g.get_vertex(start)
        
        # Add the neighbours of the starting to the vertices array
        for v in curr.get_connections():
            fifo.append(v.get_id())            
            # Set the parent of v as the starting position
            self.parent[v.get_id()] = start
        
        # Track the maximum fringe values using the FIFO queue   
        self.maxFringe = len(fifo)
            
        while len(fifo) >  0:
            # Mark the new current vertex by popping the first element in FIFO
            curr = self.g.get_vertex(fifo.pop(0))
            
            # Set the new current vertex as visited
            self.visited.append(curr.get_id())
            
            # If the current vertex is equal to the target
            if curr.get_id() == target:
                # We've found the target and are done searching
                self.output()
                
            # Otherwise continue searching
            else:     
                # Search through the neighbours of the current vertex
                for v in curr.get_connections():
                    # If v has not been visited
                    if v.get_id() not in self.visited:
                        # Set the parent of v as curr
                        self.parent[v.get_id()] = curr.get_id()
                        
                        # Add v to the FIFO array
                        fifo.append(v.get_id())    
                        
                        # If FIFO is larger than the current max fringe then we've found a new max fringe
                        if len(fifo) > self.maxFringe:
                            self.maxFringe = len(fifo)                            


    # DFS Algorithm
    def DFS(self):
        # Vertices will hold all of the vertices (LIFO) 
        vertices = []
        # To track vertices that have been visited
        self.visited = []
        # To track the parents of each vertex
        self.parent = {}
        
        # Save the start and target indicies 
        start = self.s[0] * self.columns + self.s[1]
        target = self.t[0] * self.columns + self.t[1]
        
        # Set the current vertex as the vertex at the starting index to begin
        curr = self.g.get_vertex(start)

        # Add the neighbours of the starting to the vertices array
        for v in curr.get_connections():
            vertices.append(v.get_id())            
            # Set the parent of v as the starting position
            self.parent[v.get_id()] = start

        # Track the maximum fringe values using the vertices array
        self.maxFringe = len(vertices)
        
        # While there are still vertices to visit
        while len(vertices) > 0:
            # Mark the new current vertex by popping the last element in vertices
            curr = self.g.get_vertex(vertices.pop())
            
            # Set the new current vertex as visited
            self.visited.append(curr.get_id())
            
            # If the current vertex is equal to the target
            if curr.get_id() == target:
                # We've found the target and are done searching
                self.output()
            
            # Otherwise continue searching
            else:     
                # Search through the neighbours of the current vertex
                for v in curr.get_connections():
                    # If v has not been visited
                    if v.get_id() not in self.visited:
                        # Set the parent of v as curr
                        self.parent[v.get_id()] = curr.get_id()
                        
                        # Add v to the vertices array
                        vertices.append(v.get_id())
                        
                        # If vertices is larger than the current max fringe then we've found a new max fringe
                        if len(vertices) > self.maxFringe:
                            self.maxFringe = len(vertices)                      
      
        
    # Get the path taken by the algorithm by traversing visited in reverse
    def get_path(self):
        # Get the index of the maze's starting vertex
        start = self.s[0] * self.columns + self.s[1]
        
        # Get the last vertex that was visited by the algorithm
        curr = self.visited[len(self.visited)-1]
        
        # Add curr to the path
        self.path = [curr]
        
        # Working backwards, add each vertex in visited to the path
        while curr != start:
            curr = self.parent[curr]
            self.path.append(curr)
          
        # Reverse the order of path as we built it working backwards  
        self.path.reverse()   
        
        
    # A generic output function that can be used by each of our algorithms
    def output(self):
        # Get the path used to find the solution
        self.get_path()
        
        # Make a string that contains the maze with periods(".") that indicate the path taken to get the solution
        solvedMaze = ""
        for row in range(len(self.matrix)):
            for column in range(len(self.matrix[row])):
                # Set the current index within the maze
                curr = row * self.columns + column
                
                # If the current index was visited along the path
                if curr in self.path:
                    # Mark that vertex as visited by putting a period(".") there
                    solvedMaze = solvedMaze + "."
                else:
                    # Otherwise don't make any changes
                    solvedMaze = solvedMaze + self.matrix[row][column]
        
        # Print the solved maze   
        print(solvedMaze)
        
        # Print a report of how the algorithm solved the maze with required statistics
        print("Path taken: ", self.path)
        print("Path cost: ", len(self.path))
        print("Number of vertices expanded: ", len(self.visited))
        print("Maximum size of the fringe: ", self.maxFringe)


# =============================================================================
# END OF MAZE / START OF GRAPH
# =============================================================================


class Graph(object):
    # Instantiate properties of object by using self
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0


    # Creating a new Vertex object    
    def add_vertex(self, node): 
        new_v = Vertex(node)
        # Adding a new vertex in dictionary where key is a node label and the value is the vertex object
        self.vert_dict[node] = new_v
        # new_v.add_coordinates(coordinates[0], coordinates[1])
        self.num_vertices = self.num_vertices + 1

    
    def get_vertex(self, node):
        # Returns the requested node from dictionary otherwise returns nothing
        if node in self.vert_dict:
            return self.vert_dict[node]
        else:
            return None
      
        
    # Used to add the neighbours from edge and to edge
    def add_edge(self, from_edge, to_edge, weight = 1):
        if from_edge not in self.vert_dict:
            self.add_vertex(from_edge)
        if to_edge not in self.vert_dict:
            self.add_vertex(to_edge)
        self.vert_dict[from_edge].add_neighbor(self.vert_dict[to_edge], weight)


    # Returns an array for all of the vertices in the graph
    def get_vertices(self):
        return self.vert_dict.keys()
  
    
    # Creates a summary of the nodes in a graph including each vertex's neighbors and the weight between them
    def graph_summary(self):
        for v in self.vert_dict.values():
            for w in v.get_connections():
                v_id = v.get_id()
                w_id = w.get_id()
              
                # Print the summary
                print(v_id, w_id, v.get_weight(w))
 
    
# =============================================================================
# END OF GRAPH / START OF VERTEX        
# =============================================================================
    
    
class Vertex:
    # Initialize the vertex 
    def __init__(self, node):   
        self.id = node
        # self.coordinates = coordinates
        self.parent = None
        self.adjacent = {}


    # This will return the adjacent nodes using dictionary keys     
    def get_connections(self):
        return self.adjacent.keys()


    # Adds a neighbor to the current vertex and defines the weight between
    def add_neighbor(self, neighbour, weight = 1):
        self.adjacent[neighbour] = weight
        
    # Adds coordinates to a vertex    
    def add_coordinates(self, x, y):
        self.coordinates = (x, y)


    # Returns the id/value associated with the vertex
    def get_id(self):
        return self.id
    
    # Returns the coordinates of a vertex
    def get_corrdinates(self):
        return self.coordinates
  
    
    # Returns the weight/distance between vertices
    def get_weight(self, neighbor):
        return self.adjacent[neighbor]
    
    
# =============================================================================
# END OF VERTEX / START OF MAIN   
# =============================================================================


# Main class for running the code
class main():
    
    smallMaze = Maze('smallMaze.lay')
    
    print("\nBreadth First Search:")
    smallMaze.BFS()
    
    print("\nDepth First Search:")
    smallMaze.DFS()
    



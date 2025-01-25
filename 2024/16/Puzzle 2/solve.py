#!/usr/bin/env python3

import time
from collections import namedtuple
import re
from typing import Callable

def get_test_file_path( i = None ) :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( file_path ) :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

robot_re = re.compile( r"^p=(?P<px>[-+]?\d+),(?P<py>[-+]?\d+) v=(?P<vx>[-+]?\d+),(?P<vy>[-+]?\d+)$" )

Coordinate = namedtuple( "Coordinate", [ "x", "y" ] )
Vector = namedtuple( "Vector", [ "dx", "dy" ] )
State = namedtuple( "State", [ "coord", "dir" ] )
Node = namedtuple( "Node", [ "estimated_cost", "heuristic_to_end", "cost_from_start", "from_set", "state" ] )
Maze = namedtuple( "Maze", [ "width", "height", "tiles", "start", "end" ] )
NodeDict = dict[ State, Node ]

# the directions expressed as characters (to represent them in the maze)
DIR_REPR = ( ">", "^", "<", "v" )
# the same directions (in the same order) expressed as vectors
DIR_VECTORS = ( Vector(+1,0), Vector(0,-1), Vector(-1,0), Vector(0,+1) )

START_TILE = "S"
END_TILE = "E"
PATH_TILE = "."
WALL_TILE = "#"
START_DIR = ">"
VISITED_TILE = "O"
REJECTED_TILE = "x"

COST_STEP = 1
COST_TURN = 1000

def parse_data( str_data, verbose = False ) :
    start, end = None, None
    lines = str_data.split( "\n" )
    width, height = len( lines[0] ), len( lines )
    tiles = dict()
    for y, line in enumerate( lines ) :
        for x, char in enumerate( line ) :
            if char == WALL_TILE :
                # we don't map walls...
                continue
            coord = Coordinate( x, y )
            tiles[ coord ] = char
            if char == START_TILE :
                start = State( coord=coord, dir=DIR_REPR.index(START_DIR) )
            elif char == END_TILE :
                end = coord
    maze = Maze( width, height, tiles, start, end )
    return maze

def print_maze( maze, visited = None, cost = None, closed = None, draw_walls = True ) :
    print()
    print( f"Maze {maze.width}x{maze.height}:" )
    if visited is None and closed is None :
        tiles = maze.tiles
    else :
        # visited is a list of coordinates
        # for each element of the path (except start & end of the maze)
        # we replace the empty PATH_TILE "." with the direction
        tiles = maze.tiles.copy() # we don't want to alter the original maze
        for coord, dir in closed :
            tiles[ coord ] = REJECTED_TILE
        for coord in visited :
            tiles[ coord ] = VISITED_TILE
    for y in range( maze.height ) :
        line = ""
        for x in range( maze.width ) :
            coord = Coordinate( x, y )
            line += tiles.get( coord, WALL_TILE if draw_walls else ' ' )
        print( line )
    print( f"Starting state: @{maze.start.coord}, direction: {DIR_REPR[maze.start.dir]}" )
    print( f"End: @{maze.end}" )
    if visited is not None :
        print( f"Nb of visited tiles: {len(visited)}" )
    if cost is not None :
        print( f"Shortest path cost: {cost}" )
    print()

def get_neighbours( state: State , maze: Maze, verbose = False ) :
    neighbours = [
        State( state.coord, ( state.dir + 1 ) % len( DIR_VECTORS ) ), # +90° turn, i.e. anti-clockwise
        State( state.coord, ( state.dir - 1 ) % len( DIR_VECTORS ) ), # -90° turn, i.e. clockwise
    ]
    vector = DIR_VECTORS[ state.dir ]
    next_coord = Coordinate( state.coord.x + vector.dx, state.coord.y + vector.dy )
    if next_coord in maze.tiles :
        neighbours.append( State( next_coord, state.dir ) )
    return neighbours

def heuristic_full( state: State, maze: Maze, verbose: bool = False ) -> int :
    # we define the heuristic as the "minimum" cost to reach the maze end,
    # as if there were no walls beetween the state and the end of the maze
    # and, taking the orientation into account, we estimate the nb of turns
    return heuristic_distance( state, maze, verbose ) + heuristic_turns( state, maze, verbose )

def heuristic_distance( state: State, maze: Maze, verbose: bool = False ) -> int :
    # we define the heuristic as the "minimum" cost to reach the maze end,
    # as if there were no walls beetween the state and the end of the maze
    # and without taking turns into account
    delta_x, delta_y = maze.end.x - state.coord.x, maze.end.y - state.coord.y
    distance = abs( delta_x ) + abs( delta_y )
    return distance * COST_STEP

def heuristic_turns( state: State, maze: Maze, verbose: bool = False ) -> int :
    # the number of turns to reach the target
    # if there were no walls beetween the state and the end of the maze
    # the actual distance to the target is ignored
    if state.coord == maze.end :
        # we reached the end !
        return 0
    delta_x, delta_y = maze.end.x - state.coord.x, maze.end.y - state.coord.y
    vector = DIR_VECTORS[ state.dir ]
    scalar_product = vector.dx * delta_x + vector.dy * delta_y
    if ( delta_x != 0 and delta_y != 0 ) :
        # both delta are non zero
        nb_turns = 1 if scalar_product > 0 else 2
    else :
        # one delta (and only one) is zero
        # i.e. coordinates are on the same line or row as the end of the maze
        nb_turns = 0 if scalar_product > 0 else 1 if scalar_product == 0 else 2
    return nb_turns * COST_TURN

def heuristic_zero( state: State, maze: Maze, verbose: bool = False ) -> int :
    # always 0
    # turns the A* algorithm into a Dijkstra algorithm
    return 0

def get_move_cost( a: State, b: State, verbose: bool = False ) -> int :
    # we assume a and b are neighbour positions
    if a.coord == b.coord :
        # if same coordinates, direction is different and we move only by (+/-)90°
        return COST_TURN
    else :
        # if different coordinates, direction is the same and we move only by 1 tile
        return COST_STEP

def make_node( state: State, maze: Maze, from_node: Node = None,
              heuristic: Callable[ [State, Maze, bool], int ] = heuristic_full,
              verbose: bool = False ) -> Node :
    heuristic_to_end = heuristic( state, maze, verbose )
    from_set = set()
    if from_node is not None :
        from_set.add( from_node.state )
        cost_from_start = from_node.cost_from_start + get_move_cost( from_node.state, state, verbose )
    else :
        # starting node
        # from_set is empty set
        cost_from_start = 0
    estimated_cost = cost_from_start + heuristic_to_end
    return Node( estimated_cost, heuristic_to_end, cost_from_start, from_set, state )

def merge_nodes( node_a: Node, node_b: Node, verbose: bool = False ) :
    # every values are equal except from_set
    from_set = node_a.from_set.union( node_b.from_set )
    if verbose :
        print( f"Merging nodes for @{node_a.state}: from_set = {from_set}" )
    return Node(
        node_a.estimated_cost, node_a.heuristic_to_end, node_a.cost_from_start,
        from_set, node_a.state
    )

def add_open_node( open_set: NodeDict, state: State, maze: Maze, from_node: Node = None,
                  heuristic: Callable[ [State, Maze, bool], int ] = heuristic_full,
                  verbose: bool = False ) -> NodeDict :
    node = make_node( state, maze, from_node, heuristic, verbose )
    if state in open_set :
        if node.estimated_cost < open_set[ state ].estimated_cost :
            open_set[ state ] = node
        elif node.estimated_cost == open_set[ state ].estimated_cost :
            open_set[ state ] = merge_nodes( open_set[ state ], node, verbose )
    else :
        open_set[ state ] = node
    return open_set

def get_next_open_node( open_set: NodeDict ) -> tuple[ NodeDict, Node ] :
    next_open_node = min( open_set.values() )
    open_set.pop( next_open_node.state )
    return open_set, next_open_node

def a_star( maze: Maze, starting_state: State = None,
           heuristic: Callable[ [State, Maze, bool], int ] = heuristic_full,
           verbose: bool = False ) -> tuple[ list[ Coordinate ], int, NodeDict ] :
    # initialisation
    if starting_state is None :
        starting_state = maze.start
    open_set = NodeDict()
    open_set = add_open_node( open_set, starting_state, maze, None, heuristic, verbose )
    closed_set = NodeDict()
    # loop: main algorithm
    print( f"Searching for all shortest paths from @{starting_state.coord} to @{maze.end}" )
    cost_start_to_end = float('inf')
    end_nodes = []
    while len( open_set ) > 0 :
        open_set, current_node = get_next_open_node( open_set )
        closed_set[ current_node.state ] = current_node
        if current_node.estimated_cost > cost_start_to_end :
            # the current node, which has the minimum estimated cost
            # is more costly than the shortest path already found
            # (because it has not yet reached the end)
            # => stop the loop
            print( f"Stopping the search: {current_node}" )
            break
        for neighbour_state in get_neighbours( current_node.state, maze, verbose ) :
            neighbour_node = make_node( neighbour_state, maze, current_node, heuristic, verbose )
            if neighbour_node.estimated_cost <= cost_start_to_end :
                # this node is still a candidate to reach the end via a shortest path
                if neighbour_state.coord == maze.end :
                    # we reached the end and found _A_ shortest path
                    print( f"End reached @{neighbour_state.coord}, direction: {DIR_REPR[neighbour_state.dir]}" )
                    end_node = make_node( neighbour_state, maze, current_node, heuristic, verbose )
                    cost_start_to_end = end_node.cost_from_start
                    print( f"Cost to reach the end: {cost_start_to_end}" )
                    end_nodes.append( end_node )
                if neighbour_state not in closed_set :
                    # if the node was not already processed, we add it to the open set
                    open_set = add_open_node(
                        open_set, neighbour_state, maze, current_node, heuristic, verbose
                    )
                else :
                    # if the node is in the closed set, we see if the estimated cost is the same
                    neighbour_node = make_node(
                        neighbour_state, maze, current_node, heuristic, verbose
                    )
                    if neighbour_node.estimated_cost < closed_set[ neighbour_state ].estimated_cost :
                        print(
                            f"WARNING: {neighbour_node} sould not be found at this step:",
                            f"its estimated cost is less than the node already processed",
                            f"for the same state: {closed_set[ neighbour_state ]}"
                            f"\nHeuristic function {heuristic.__name__} may be not admissible"
                        )
                        closed_set[ neighbour_state ] = neighbour_node
                    elif neighbour_node.estimated_cost == closed_set[ neighbour_state ].estimated_cost :
                        closed_set[ neighbour_state ] = merge_nodes(
                            closed_set[ neighbour_state ], neighbour_node, verbose
                        )
    print( f"End of shortest path search" )
    visited = get_visited_tiles( end_nodes, closed_set )
    return visited, end_node.cost_from_start, closed_set

def get_visited_tiles( end_nodes: list[Node], closed_set: NodeDict,
                      verbose: bool = False ) -> set[Coordinate] :
    coords = set()
    print( f"{len(end_nodes)} end node(s) to trace back" )
    for i, node in enumerate( end_nodes ) :
        print( f"Extracting end node #{i}" )
        coords = coords | trace_back( node, closed_set, verbose )
    return coords

def trace_back( end_node: Node, closed_set: NodeDict,
               verbose: bool = False ) -> set[Coordinate] :
    coords = { end_node.state.coord }
    for predecessor_state in end_node.from_set :
        predecessor_node = closed_set[ predecessor_state ]
        coords = coords | trace_back( predecessor_node, closed_set, verbose )
    return coords

def do_problem( str_data, verbose = False ) :
    maze = parse_data( str_data, verbose )
    print_maze( maze, None, None, None, True )
    visited, cost, closed = a_star( maze, heuristic=heuristic_full, verbose=verbose )
    print_maze( maze, visited, cost, closed, False )
    print( f"END" )

def do_tests( i = None ) :
    str_data = get_file_content( get_test_file_path( i ) )
    do_problem( str_data, True )

def do_input() :
    str_data = get_file_content( get_input_file_path() )
    do_problem( str_data, False )

def main() :
    start = time.time()
    #do_tests(1)
    #do_tests(2)
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()

#!/usr/bin/env python3

import time
from collections import namedtuple
from collections import defaultdict

def get_test_file_path( i = None ) :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( file_path ) :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

Coordinate = namedtuple( "Coordinate", [ "x", "y" ] )
Maze = namedtuple( "Maze", [ "width", "height", "tiles", "start", "end" ] )

START_TILE = "S"
END_TILE = "E"
PATH_TILE = "."
WALL_TILE = "#"

def parse_data( str_data: str, verbose: bool = False ) :
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
                start = coord
            elif char == END_TILE :
                end = coord
    maze = Maze( width, height, tiles, start, end )
    return maze

def print_maze( maze: Maze, shortcut = None, verbose: bool = False ) :
    print()
    print( f"Maze {maze.width}x{maze.height}:" )
    if shortcut is None :
        tiles = maze.tiles
    else :
        tiles = maze.tiles.copy()
        # todo : read the shortcut information and apply it to the tiles
    for y in range( maze.height ) :
        line = ""
        for x in range( maze.width ) :
            coord = Coordinate( x, y )
            line += tiles.get( coord, WALL_TILE )
        print( line )
    print( f"Start @{maze.start}, End @{maze.end}" )
    if shortcut is not None :
        print( f"Shortcut: {shortcut}" )
    print()

def get_path( maze: Maze, verbose: bool = False ) :
    print( f"Computing path..." )
    path: list[Coordinate] = [ maze.start, ]
    while path[-1] != maze.end :
        neighbours = (
            Coordinate( path[-1].x - 1, path[-1].y ),
            Coordinate( path[-1].x + 1, path[-1].y ),
            Coordinate( path[-1].x, path[-1].y - 1 ),
            Coordinate( path[-1].x, path[-1].y + 1 ),
        )
        next = [ n for n in neighbours if n in maze.tiles and n not in path ]
        if len(next) == 0 :
            raise RuntimeError( f"No next tile found for tile @{path[-1]}" )
        if len(next) > 1 :
            raise RuntimeError( f"More than 1 next tile found for tile @{path[ -1 ]}: {next}" )
        path.append( next[0] )
    if verbose :
        print( f"Path found: {path}" )
    print( f"Path length: {len(path)}" )
    return path

def get_flying_distance( a: Coordinate, b: Coordinate ) :
    return abs( a.x - b.x ) + abs( a.y - b.y )

def get_neighbours( center: Coordinate, radius: int, possible: list[Coordinate] ) :
    neighbours = set()
    for dx in [ 0, radius ] :
        dy = radius - dx
        neighbours.add( Coordinate( center.x + dx, center.y + dy ) )
        neighbours.add( Coordinate( center.x - dx, center.y + dy ) )
        neighbours.add( Coordinate( center.x + dx, center.y - dy ) )
        neighbours.add( Coordinate( center.x - dx, center.y - dy ) )
    return [ n for n in neighbours if n in possible ]

def find_shortcuts( path: list[Coordinate], sc_cost: int, sc_min_gain: int, verbose: bool = False ) :
    shortcuts = []
    print( f"Searching for shortcuts saving at least {sc_min_gain} picoseconds..." )
    for sc_start_index, sc_start in enumerate( path ) :
        min_sc_end_index = sc_start_index + sc_cost + sc_min_gain
        candidates = get_neighbours( sc_start, sc_cost, path[min_sc_end_index:] )
        for sc_end in candidates :
            sc_end_index = path.index( sc_end )
            sc_gain = ( sc_end_index - sc_start_index ) - sc_cost
            if verbose :
                print( f"Shortcut found, saving {sc_gain} picoseconds: from @{sc_start} to @{sc_end}" )
            shortcuts.append( (sc_gain, sc_start, sc_end ) )
    if verbose :
        shortcuts.sort()
        sc_by_gain = defaultdict( list )
        for gain, *values in shortcuts:
            sc_by_gain[gain].append(values)
        for gain in sc_by_gain :
            print( f"- {len(sc_by_gain[gain])} shortcuts found saving {gain} picoseconds" )
    return shortcuts

def do_problem( str_data: str, sc_cost: int, sc_min_gain: int, verbose: bool = False ) :
    maze = parse_data( str_data, verbose )
    print_maze( maze, None, verbose )
    path = get_path( maze, verbose )
    shortcuts = find_shortcuts( path, sc_cost, sc_min_gain, verbose )
    print( f"{len(shortcuts)} shortcuts found saving at least {sc_min_gain} picoseconds" )
    print( f"END" )

def do_tests( i: int = None ) :
    str_data = get_file_content( get_test_file_path( i ) )
    do_problem( str_data, 2, 2, verbose = True )

def do_input() :
    str_data = get_file_content( get_input_file_path() )
    do_problem( str_data, 2, 100, verbose = False )

def main() :
    start = time.time()
    #do_tests(1)
    #do_tests(2)
    #do_tests(3)
    #do_tests(4)
    #do_tests(5)
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()

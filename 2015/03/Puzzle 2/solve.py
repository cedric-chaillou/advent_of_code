#!/usr/bin/env python3

import time
from dataclasses import dataclass

def get_test_file_path( i = None ) :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( file_path ) :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

@dataclass( frozen=True )
class Location :
    x: int
    y: int
    
    def move( self, char ) -> 'Location' :
        if char == '>' :
            return Location( self.x + 1, self.y )
        if char == '^' :
            return Location( self.x, self.y + 1 )
        if char == '<' :
            return Location( self.x - 1, self.y )
        if char == 'v' :
            return Location( self.x, self.y - 1 )
        raise RuntimeError( f"Unknown move: {char}" )

def parse_data( str_data: str, verbose: bool = False ) :
    return str_data.strip()

def do_moves( name: str, moves: str, start: Location, verbose: bool ) -> set :
    print( f"{name} moves {len(moves)} times and starts from {start}" )
    if verbose :
        print( f"{name} moves: {moves}" )
    houses = { start }
    current = start
    for m in moves :
        current = current.move( m )
        houses.add( current )
    print( f"{name} visited {len(houses)} different houses" )
    return houses

def do_problem( str_data: str, verbose = False ) :
    moves = parse_data( str_data, verbose )
    if verbose :
        print( f"Moves: {moves}" )
    santa_houses = do_moves( "Santa", moves[::2], Location( 0, 0 ), verbose )
    robo_houses = do_moves( "Robo-Santa", moves[1::2], Location( 0, 0 ), verbose )
    houses = santa_houses.union( robo_houses )
    print( f"In total, {len(houses)} different houses were visited at least once" )
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
    #do_tests(3)
    #do_tests(4)
    #do_tests(5)
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()

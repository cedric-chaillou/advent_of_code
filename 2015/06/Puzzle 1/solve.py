#!/usr/bin/env python3

import time
from dataclasses import dataclass
import re

def get_test_file_path( i: int = None ) -> str :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() -> str :
    return "input.txt"

def get_file_content( file_path: str ) -> str :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

@dataclass( frozen=True )
class Location :
    x: int
    y: int

@dataclass( frozen=True )
class Instruction :
    action: str
    from_x: int
    from_y: int
    to_x: int
    to_y: int

@dataclass
class Light :
    loc: Location
    on: bool = False
    
    def turn( self, on: bool ) :
        self.on = on

    def toggle( self ) :
        self.on = not self.on

    def count( self ) -> int :
        return 1 if self.on else 0


LINE_RE = re.compile( r"(?P<action>turn on|turn off|toggle) (?P<from_x>\d+),(?P<from_y>\d+) through (?P<to_x>\d+),(?P<to_y>\d+)" )
WIDTH = 1000
HEIGHT = 1000

def parse_data( str_data: str, verbose: bool = False ) :
    print( f"Initializing {WIDTH}x{HEIGHT} lights..." )
    lights: dict[Location, Light] = dict()
    for x in range( WIDTH ) :
        for y in range( HEIGHT ) :
            loc = Location(x,y)
            lights[ loc ] = Light( loc )
    print( f"Parsing instructions..." )
    instructions: list[Instruction] = []
    for line in str_data.strip().split( "\n" ) :
        match = LINE_RE.match( line )
        if match is not None :
            m_dict = match.groupdict()
            instr = Instruction( m_dict[ 'action' ]
                                , int( m_dict[ 'from_x' ] ), int( m_dict[ 'from_y' ] )
                                , int( m_dict[ 'to_x' ] ), int( m_dict[ 'to_y' ] ) )
            if verbose :
                print( f"{instr}" )
            instructions.append( instr )
    return lights, instructions

def do_instruction( instr: Instruction, lights: dict[Location, Light] ) -> dict[Location, Light] :
    for x in range( instr.from_x, instr.to_x + 1 ) :
        for y in range( instr.from_y, instr.to_y + 1 ) :
            if instr.action == "turn on" :
                lights[ Location( x, y ) ].turn( True )
            elif instr.action == "turn off" :
                lights[ Location( x, y ) ].turn( False )
            elif instr.action == "toggle" :
                lights[ Location( x, y ) ].toggle()
            else :
                raise RuntimeError( f"Unknown action '{instr.action}'" )
    return lights

def count_lights( lights: dict[Location, Light] ) -> int :
    print( f"Counting lights that are 'on'..." )
    count = 0
    for x in range( WIDTH ) :
        for y in range( HEIGHT ) :
            count += lights[ Location( x, y ) ].count()
    return count

def do_problem( str_data: str, verbose = False ) :
    lights, instructions = parse_data( str_data, verbose )
    print( f"Executing {len(instructions)} instructions..." )
    for instr in instructions :
        lights = do_instruction( instr, lights )
    result = count_lights( lights )
    print( f"{result} lights on" )
    print( f"END" )

def do_tests( i: int = None ) :
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

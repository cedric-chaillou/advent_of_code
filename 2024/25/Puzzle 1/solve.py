#!/usr/bin/env python3

import time
from dataclasses import dataclass
import re

def get_test_file_path( i = None ) :
    return "tests.txt" if i is None else f"tests_{i}.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( file_path ) :
    with open( file_path, 'r' ) as f :
        data = f.read()
    return data

@dataclass
class Lock :
    height: int
    pins: tuple[int]
    
    def __repr__(self):
        repr = [ f"Lock: {self.height} x {self.pins}" ]
        for y in range(self.height) :
            line = ""
            for pin_height in self.pins :
                line += "#" if y < pin_height else "."
            repr.append( line )
        repr.append( "\n" )
        return "\n".join( repr )

@dataclass
class Key :
    heights: tuple[int]
    
    def __repr__(self):
        repr = [ f"Key: {self.heights}" ]
        max_height = max(self.heights)+1
        for y in range(max_height) :
            line = ""
            for height in self.heights :
                line += "." if y < max_height - height else "#"
            repr.append( line )
        repr.append( "" )
        return "\n".join( repr )

def parse_data( str_data: str, verbose: bool = False ) :
    locks = []
    keys = []
    for part in str_data.strip().split( "\n\n" ) :
        height = 0
        pins = None
        for line in part.split( "\n" ) :
            height += 1
            if pins is None :
                pins = [ 0, ] * len( line )
            for i, char in enumerate( line ) :
                pins[i] += 1 if char == "#" else 0
        if part[0] == "#" :
            locks.append( Lock( height, tuple( pins ) ) )
        else :
            keys.append( Key( tuple( pins ) ) )
    return locks, keys

def fit( lock: Lock, key: Key, lock_id: int, key_id: int, verbose: bool ) :
    print( f"Testing lock #{lock_id} with key #{key_id}..." )
    for i, pin_height in enumerate( lock.pins, start=0 ) :
        if pin_height + key.heights[ i ] > lock.height :
            print( f"Lock & key overlap in pin #{i+1}" )
            return False
    print( f"Lock & key fit" )
    return True

def do_problem( str_data: str, verbose = False ) :
    locks, keys = parse_data( str_data, verbose )
    print( f"{len(locks)} locks & {len(keys)} keys" )
    if verbose :
        for lock in locks :
            print( lock )
        for key in keys :
            print( key )
    nb_fits = 0
    for i, lock in enumerate( locks, start=1 ) :
        for j, key in enumerate( keys, start=1 ) :
            if fit( lock, key, i, j, verbose ) :
                nb_fits += 1
    print( f"\nNb lock/key pair fits: {nb_fits}" )
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

#!/usr/bin/env python3

import time

def get_test_file_path() :
    return "tests.txt"

def get_input_file_path() :
    return "input.txt"

def get_file_content( _file_path, _as_lines = False ) :
    with open( _file_path, 'r' ) as f :
        if ( _as_lines ) :
            data = f.readlines()
        else :
            data = f.read()
    return data

def mix( a, b ) :
    return a ^ b

def prune( a ) :
    # 16777216 = 0x1000000 = 0xffffff + 1
    # donc a % 16777216 == a & 0xffffff
    return a & 0xffffff

def mul_bin( a, b ) :
    # a * 2^b
    return a << b

def mul_2048( a ) :
    return mul_bin( a, 11 )

def mul_64( a ) :
    return mul_bin( a, 6 )

def div_int_bin( a, b ) :
    # a / 2^b, rounded down
    return a >> b

def div_32( a ) :
    return div_int_bin( a, 5 )

def next_secret_number( secret_number ) :
    secret_number = prune( mix( mul_64( secret_number ), secret_number ) )
    secret_number = prune( mix( div_32( secret_number ), secret_number ) )
    secret_number = prune( mix( mul_2048( secret_number ), secret_number ) )
    return secret_number

def iter_secret_number( secret_number, nb_iter = 2000 ) :
    for i in range( nb_iter ) :
        secret_number = next_secret_number( secret_number )
    return secret_number

def prices_sequences( secret_number, nb_iter = 2000 ) :
    price = secret_number % 10
    diff = None
    seq = []
    all_seq = {}
    for i in range( nb_iter ) :
        secret_number = next_secret_number( secret_number )
        prev = price
        price = secret_number % 10
        diff = price - prev
        seq.append( diff )
        if len( seq ) > 4 :
            seq.pop( 0 )
        if len( seq ) == 4 :
            key = ",".join( [ str(n) for n in seq ] )
            if ( key not in all_seq ) :
                all_seq[ key ] = price
    return all_seq

def do_check( secret_number, nb_iter ) :
    price = secret_number % 10;
    diff = None
    for i in range( nb_iter ) :
        print( f"{i}: {secret_number} => price is {price} ({diff})" )
        secret_number = next_secret_number( secret_number )
        prev = price
        price = secret_number % 10;
        diff = price - prev
    print( f"{nb_iter}: {secret_number} => price is {price} ({diff})" )

def do_problem( str_datas ) :
    datas = [ int( s.strip() ) for s in str_datas ]
    print( f"Computing price sequences for {len( datas )} monkeys...")
    all_sequences = {}
    for i, secret_number in enumerate( datas ) :
        print( f"Computing for monkey #{i+1}, starting secret number: {secret_number}" )
        monkey_sequences = prices_sequences( secret_number )
        for key, price in monkey_sequences.items() :
            if ( key in all_sequences ) :
                all_sequences[ key ][0] += price # price in bananas
                all_sequences[ key ][1] += 1     # nb monkeys with this sequence
            else :
                all_sequences[ key ] = [ price, 1 ]
    print( f"Total number of sequences found: {len( all_sequences )}" )
    max_sequence = ""
    max_price = 0
    max_nb_monkeys = 0
    for seq, price, nb_monkeys in [ (k, v[0], v[1]) for k, v in all_sequences.items() ] :
        if price > max_price :
            max_sequence = seq
            max_price = price
            max_nb_monkeys = nb_monkeys
    print( f"Maximum number of bananas: {max_price}" )
    print( f"    for sequence <{max_sequence}>" )
    print( f"    found in {max_nb_monkeys} monkeys" )

def do_tests() :
    do_problem( get_file_content( get_test_file_path(), True ) )

def do_input() :
    do_problem( get_file_content( get_input_file_path(), True ) )

def main() :
    start = time.time()
    #do_check( 123, 10 )
    #do_tests()
    do_input()
    elapsed = time.time() - start
    print( f"Total execution time: {elapsed:.3f} s" )

main()

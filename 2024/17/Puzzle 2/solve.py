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

class Computer:
    def __init__( self, A: int, B: int, C: int, program: str ) :
        self.a: int = A
        self.b: int = B
        self.c: int = C
        self.__program: tuple[int] = tuple( int(s) for s in program.split( "," ) )
        self.__output: list[int] = []
        self.__curser: int = 0

    @property
    def program( self ) -> str:
        """The program string of instructions and operands, joined with commas"""
        return ",".join( str(i) for i in self.__program )

    @property
    def output( self ) -> str:
        """The output string produced by out instructions, joined with commas"""
        return ",".join( str(i) for i in self.__output )

    @property
    def is_running( self ) -> bool :
        """True if the program is still running, False otherwise"""
        # nota: we must always be able to read 2 values at the end of the program
        return self.__curser >= 0 and self.__curser < len( self.__program ) - 1

    @property
    def is_halted( self ) -> bool :
        """True if the program is halted, False otherwise"""
        return not self.is_running

    def print( self ) :
        print()
        print( "*** Computer ***" )
        print()
        print( f"Register A: {self.a}" )
        print( f"Register B: {self.b}" )
        print( f"Register C: {self.c}" )
        print()
        print( f"Program: {self.program}" )
        print()
        print( f"State: {'HALTED' if self.is_halted else 'RUNNING'}, curser @{self.__curser}" )
        print( f"Output: {self.output}" )
        print()

    def run_program( self, verbose = False ) -> str :
        """
        Run the program recorded in the computer and returns its output

        Args:
            verbose (bool, optional): prints additionnal messages, for debug purposes. Defaults to False.

        Returns:
            str: the output of the program
            (if the program outputs multiple values, they are separated by commas)
        """
        print( f"Starting program, starting curser @{self.__curser} ..." )
        while self.is_running :
            instruction, operand = self.read()
            if verbose :
                print( f"Reading: Instruction = {instruction}, Operand = {operand}" )
            self.execute( instruction, operand )
            if verbose :
                print( f"Curser @{self.__curser}, Output length: {len(self.__output)}" )
        print( f"Program halted with curser @{self.__curser}, Output length: {len(self.__output)}" )
        return self.output

    def read( self ) -> tuple[ int, int ]:
        """
        Reads the instruction and operand at the curser place in the program,
        then advance the curser to the next instruction

        Returns:
            tuple[ int, int ]: the instruction and its operand
        """
        if self.is_running :
            self.__curser += 2
            return ( self.__program[ self.__curser - 2 ], self.__program[ self.__curser - 1 ] )
        else :
            return ( None, None )

    def execute( self, instruction: int, operand: int ) -> None :
        """
        Execute the instruction from the program, with its operand

        Args:
            instruction (int): the instruction to execute
            operand (int): the operand to pass to the instruction as its argument
        """
        self.__get_method( instruction )( operand )

    def __get_method( self, instruction: int ) -> Callable[ [ 'Computer', int ], None ] :
        """
        Returns the method to call to execute the instruction
        
        Warning: the method will need to be called with "self" as its 1st argument

        Raises:
            ValueError: Error if the instruction is not an integer between 0 and 7

        Returns:
            ((Computer, int) -> None): the method to call to execute the instruction
        """
        methods = ( self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv )
        if instruction < 0 or instruction >= len( methods ) :
            raise ValueError( f"Invalid instruction value {instruction}" )
        return methods[ instruction ]

    def __combo( self, combo_operand: int ) -> int :
        """
        The value of a combo operand can be found as follows:
            - Combo operands 0 through 3 represent literal values 0 through 3.
            - Combo operand 4 represents the value of register A.
            - Combo operand 5 represents the value of register B.
            - Combo operand 6 represents the value of register C.

        Args:
            operand (int): _description_

        Raises:
            ValueError: Error if the operand is not an integer between 0 and 6
            (Combo operand 7 is reserved and will not appear in valid programs)

        Returns:
            int: the "literal" operand value to use as argument for the instruction
        """
        if combo_operand == 4 :
            return self.a
        elif combo_operand == 5 :
            return self.b
        elif combo_operand == 6 :
            return self.c
        elif combo_operand in ( 0, 1, 2, 3 ) :
            return combo_operand
        else :
            raise ValueError( f"Invalid value {combo_operand} for combo operand" )

    def __divide_a( self, literal_operand: int ) -> int :
        """
        Performs division.
            - The numerator is the value in the A register.
            - The denominator is found by raising 2 to the power of the "literal" operand.

        Args:
            literal_operand (int): "literal" operand

        Returns:
            int: the result of the division operation, truncated to an integer
        """
        return self.a >> literal_operand

    def __xor_b( self, literal_operand: int ) -> int :
        """
        Returns the result of a binary XOR between regster B and "literal" operand

        Args:
            literal_operand (int): "literal" operand

        Returns:
            int: the result of the binary XOR operation
        """
        return self.b ^ literal_operand

    def __mod_8( self, literal_operand: int ) -> int :
        """
        Calculates the value of its "literal" operand modulo 8 (thereby keeping only its lowest 3 bits)

        Args:
            literal_operand (int): "literal" operand

        Returns:
            int: the result of the 
        """
        return literal_operand & 7

    def adv( self, operand: int ) -> None :
        """
        Instruction (opcode 0)

        Performs division.
            - The numerator is the value in the A register.
            - The denominator is found by raising 2 to the power of the instruction's combo operand.
            - The result of the division operation is truncated to an integer
                and then written to the A register

        Args:
            operand (int): combo operand
        """
        self.a = self.__divide_a( self.__combo( operand ) )

    def bxl( self, operand: int ) -> None :
        """
        Instruction (opcode 1)

        Calculates the bitwise XOR of register B and the instruction's "literal" operand,
        then stores the result in register B

        Args:
            operand (int): "literal" operand
        """
        self.b = self.__xor_b( operand )

    def bst( self, operand: int ) -> None :
        """
        Instruction (opcode 2)

        Calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits),
        then writes that value to the B register

        Args:
            operand (int): combo operand
        """
        self.b = self.__mod_8( self.__combo( operand ) )

    def jnz( self, operand: int ) -> None :
        """
        Instruction (opcode 3)

        Does nothing if the A register is 0.

        However, if the A register is not zero:
        it jumps by setting the instruction pointer to the value of its literal operand

        If this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

        Args:
            operand (int): the next instruction new address
        """
        if self.a != 0 :
            self.__curser = operand

    def bxc( self, operand: int ) -> None :
        """
        Instruction (opcode 4)

        Calculates the bitwise XOR of register B and register C,
        then stores the result in register B.

        Args:
            operand (int): For legacy reasons, this instruction reads an operand but ignores it.
        """
        self.b = self.__xor_b( self.c )

    def out( self, operand: int ) -> None :
        """
        Instruction (opcode 5)

        Calculates the value of its combo operand modulo 8, then outputs that value

        Args:
            operand (int): combo operand
        """
        self.__output.append( self.__mod_8( self.__combo( operand ) ) )

    def bdv( self, operand: int ) -> None :
        """
        Instruction (opcode 6)

        Performs division.
            - The numerator is the value in the A register.
            - The denominator is found by raising 2 to the power of the instruction's combo operand.
            - The result of the division operation is truncated to an integer
                and then written to the B register

        Args:
            operand (int): combo operand
        """
        self.b = self.__divide_a( self.__combo( operand ) )

    def cdv( self, operand: int ) -> None :
        """
        Instruction (opcode 7)

        Performs division.
            - The numerator is the value in the A register.
            - The denominator is found by raising 2 to the power of the instruction's combo operand.
            - The result of the division operation is truncated to an integer
                and then written to the C register

        Args:
            operand (int): combo operand
        """
        self.c = self.__divide_a( self.__combo( operand ) )

REGISTER_RE = re.compile( r"Register (?P<name>\w+): (?P<value>\d+)" )
PROGRAM_RE = re.compile( r"Program: (?P<program>[0-7](?:,[0-7])*)" )

def get_combo_operand( operand ) :
    if operand < 0 or operand > 6 :
        raise ValueError( f"Invalid value {operand} for combo operand: must be between 0 and 6" )
    return '0123ABC'[ operand ]

CodeJump = namedtuple( "CodeJump", [ "from_address", "to_address", "insert_lines_before" ] )

def indent_code( code : list, jump: CodeJump, verbose: bool = False ) :
    new_code = []
    start_address = min( jump.from_address, jump.to_address )
    end_address = max( jump.to_address, jump.from_address )
    for address, group_lines in code :
        if verbose :
            print( f"@{address}: {group_lines}" )
        if address >= start_address and address <= end_address :
            for i, line in enumerate( group_lines ) :
                if verbose :
                    print( f"Line #{i}: {line}" )
                group_lines[ i ] = "    " + line
            if address == jump.to_address :
                print( f"Adding lines before start: {jump.insert_lines_before}" )
                group_lines = jump.insert_lines_before + group_lines
        new_code.append( ( address, group_lines ) )
    return new_code

def get_instruction_lines( address, instruction, operand, verbose = False ) :
    new_lines = []
    combo = get_combo_operand( operand )
    jump = None
    if instruction == 0 :
        # A = floor( A // power( 2, combo_operand ) )
        new_lines.append( f"A = A >> {combo}" )
        if verbose :
            new_lines.append( f"print( '@{address}: A = A >> {combo}\t\t\tA =', A, oct(A), bin(A) )" )
    elif instruction == 1 :
        # B = B xor literal_operand
        new_lines.append( f"B = B ^ {operand}" )
        if verbose :
            new_lines.append( f"print( '@{address}: B = B ^ {operand}\t\t\tB =', B, oct(B), bin(B) )" )
    elif instruction == 2 :
        # B = combo_operand modulo 8
        new_lines.append( f"B = {combo} & 7" )
        if verbose :
            new_lines.append( f"print( '@{address}: B = {combo} & 7\t\t\tB =', B, oct(B), bin(B) )" )
    elif instruction == 3 :
        # if A != 0, goto literal_operand
        if operand < address :
            # going backwards in the code: we do a while loop
            loop_start_code = []
            if verbose :
                loop_start_code.append( f"print( '-- Start of loop --\t\tfrom  @{address} to @{operand}' )" )
            loop_start_code.append( "while True :" )
            jump = CodeJump( address, operand, loop_start_code )
            # with an exit condition at the end
            if verbose :
                new_lines.append( f"print( '@{address}: loop test: A != 0 ?', A != 0, '\tA =', A, oct(A), bin(A) )" )
            new_lines.append( f"if A == 0 :" )
            if verbose :
                new_lines.append( f"    print( '-- End of loop --\t\tfrom  @{address} to @{operand}' )" )
            new_lines.append( f"    break" )
            if verbose :
                new_lines.append( f"else :" )
                new_lines.append( f"    print( '-- Loop --\t\t\tjump to @{operand}' )" )
        elif operand > address :
            # going forward in the code: we do a if condition
            jump = CodeJump( address, operand, [ f"if A != 0 :" ] )
        else :
            raise ValueError( f"Invalid operand {operand} for instruction {instruction} (jnz): cannot 'jump' to the current address {address} in the program" )
    elif instruction == 4 :
        # B = B xor C
        new_lines.append( f"B = B ^ C" )
        if verbose :
            new_lines.append( f"print( '@{address}: B = B ^ C\t\t\tB =', B, oct(B), bin(B) )" )
    elif instruction == 5 :
        # add to output: combo_operand modulo 8
        new_lines.append( f"out.append( {combo} & 7 )" )
        if verbose :
            new_lines.append( f"print( '@{address}: output: {combo} & 7\t\tall outputs =', out )" )
    elif instruction == 6 :
        # B = floor( A // power( 2, combo_operand ) )
        new_lines.append( f"B = A >> {combo}" )
        if verbose :
            new_lines.append( f"print( '@{address}: B = A >> {combo}\t\t\tB =', B, oct(B), bin(B) )" )
    elif instruction == 7 :
        # C = floor( A // power( 2, combo_operand ) )
        new_lines.append( f"C = A >> {combo}" )
        if verbose :
            new_lines.append( f"print( '@{address}: C = A >> {combo}\t\t\tC =', C, oct(C), bin(C) )" )
    else :
        raise ValueError( f"Invalid value {instruction} for instruction: must be between 0 and 7" )
    print( f"Block code #{address}:\n    {'\n    '.join( new_lines ) }" )
    if jump is not None :
        print( f"Adding {jump}" )
    return ( new_lines, jump )

def make_function( A, B, C, program, verbose = False ) :
    print( f"Generating function for program {program}" )
    print( f"with starting values A = {A}, B = {B}, C = {C}" )
    if verbose :
        print( f"and with verbose messages" )
    prog_list = [ int(s) for s in program.split(",") ]
    prog_code = []
    jumps = []
    for address in range( len(prog_list) // 2 ) :
        instruction = prog_list[ 2*address ]
        operand = prog_list[ 2*address + 1 ]
        new_lines, jump = get_instruction_lines( address, instruction, operand, verbose )
        prog_code.append( ( address, new_lines ) )
        if jump is not None :
            jumps.append( jump )
    for jump in jumps :
        prog_code = indent_code( prog_code, jump, verbose )
    function_run_code = [
        f"def run( A = {A}, B = {B}, C = {C} ) :",
        f"    out = []",
    ]
    if verbose :
        function_run_code.append( "    print( 'Starting values:' )" )
        function_run_code.append( "    print( '\tA =', A )" )
        function_run_code.append( "    print( '\tB =', B )" )
        function_run_code.append( "    print( '\tC =', C )" )
    for address, lines in prog_code :
        for line in lines :
            function_run_code.append( "    " + line )
    function_run_code.append( "    return ','.join( str(i) for i in out )" )
    function_run_code = '\n'.join(function_run_code)
    #print( f"*** Function body ***\n\n{function_run_code}\n\n" )
    #function_context = { "A": A, "B": B, "C": C }
    function_context = {}
    exec( function_run_code, function_context )
    print( f"Function context content: {function_context.keys()}" )
    return function_run_code, function_context

def parse_data( str_data: str, verbose: bool = False ) :
    setup = {}
    for i, line in enumerate( str_data.split( "\n" ) ) :
        if verbose :
            print( f"Line #{i}: {line}" )
        match = REGISTER_RE.match( line )
        if match is not None :
            name = match.groupdict()[ "name" ]
            value = int( match.groupdict()[ "value" ] )
            if verbose :
                print( f"Register {name}: {value}" )
            setup[ name ] = value
            continue
        match = PROGRAM_RE.match( line )
        if match is not None :
            program = match.groupdict()[ "program" ]
            if verbose :
                print( f"Program: {program}" )
            setup[ "program" ] = program
            continue
    return setup, program

def solve( program : list[int], silent_run: Callable[[int, int, int], str], verbose: bool = False ) -> int :
    # the start of the number generates the end of the output
    # we try to solve octal by octal, adding 1 octal at a time
    # the length of the value A written in octal, is the same as the expected output
    print( f"Solving for output==program: {program}")
    expected = program.split( "," )
    str_candidates = set( str(i) for i in range( 1, 8 ) )
    while len( str_candidates ) > 0 and len( min( str_candidates ) ) < len( expected ) :
        new_candidates = set()
        for i in range( 8 ) :
            for c in str_candidates :
                str_test = f"{c}{i}"
                test = int( str_test, 8 )
                output = silent_run( A = test )
                match = True
                for k, o in enumerate( reversed( output.split( "," ) ), start=1 ) :
                    if o != expected[ -k ] :
                        match = False
                        break
                if match :
                    new_candidates.add( str_test )
        str_candidates = new_candidates
        print( f"for {len( min( str_candidates ) )} octals, we have {len( str_candidates )} candidate solutions" )
    if len( str_candidates ) > 0 :
        return int( min( str_candidates ), 8 )
    else :
        return None

def do_problem( str_data: str, verbose = False ) :
    setup, program = parse_data( str_data, verbose )
    #setup[ "verbose" ] = True
    #code, verbose_context = make_function( **setup )
    setup[ "verbose" ] = False
    code, silent_context = make_function( **setup )
    print( "Function body :" )
    print( code )
    print()
    solution = solve( program, silent_context[ "run" ] )
    print()
    if solution is not None :
        print( f"Verification for solution A = {solution}" )
        #print()
        #output = verbose_context[ "run" ]( A = solution )
        output = silent_context[ "run" ]( A = solution )
        print()
        print( "Solution found:")
        print( f"program:\t{program}")
        print( f"output:\t\t{output}")
        print( f"A =\t\t{solution}")
        print( f"oct(A) =\t{oct(solution)}")
        print( f"bin(A) =\t{bin(solution)}")
        if output== program :
            print( f"MATCH!" )
        else :
            print( f"ERROR: THE SOLUTION IS NOT A SOLUTION" )
    else :
        print( f"NO SOLUTION FOUND..." )

def do_tests( i = None ) :
    str_data = get_file_content( get_test_file_path( i ) )
    do_problem( str_data, True )

def do_input() :
    str_data = get_file_content( get_input_file_path() )
    do_problem( str_data, True )

def main() :
    start = time.time()
    #test_computer()
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

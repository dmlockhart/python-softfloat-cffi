#=======================================================================
# outline_abi.py
#=======================================================================
#
# See: https://cffi.readthedocs.org/en/latest/cdef.html
#
# CFFI's ABI mode requires that a shared library be compiled separately,
# then imported using the CFFI dlopen() interface.
#
# To prepare the .so file, run:
#
# - gcc -fPIC -shared softfloat-c/*.c -o libsoftfloat.so
#
# Now softfloat is ready to import into Python using the code below.
#
# Note that in out-of-line usage, everything before and including the
# ffi.compile() statement should really be in a build script rather than
# called at run-time (it's included inline for demonstration purposes.)

import cffi
from softfloat import bits2float, float2bits

#-----------------------------------------------------------------------
# cffi import lib
#-----------------------------------------------------------------------

ffi = cffi.FFI()
ffi.set_source('softfloat._abi', None)
ffi.cdef('''
    typedef uint32_t float32_t;
    typedef uint64_t float64_t;
    typedef struct { uint64_t v; uint16_t x; } floatx80_t;
    typedef struct { uint64_t v[ 2 ]; } float128_t;

    int_fast8_t softfloat_exceptionFlags;
    float32_t f32_add( float32_t a, float32_t b );
''')
ffi.compile()

#-----------------------------------------------------------------------
# testing
#-----------------------------------------------------------------------

assert bits2float(0x3f800000) == 1.0

from softfloat._abi import ffi
lib = ffi.dlopen('./libsoftfloat.so')

def test_add( is_inexact, out, a, b ):
  a_bits = float2bits(a)
  b_bits = float2bits(b)
  print 'expected:', float2bits(out), out, lib.softfloat_exceptionFlags
  out_bits = lib.f32_add( a_bits, b_bits )
  print 'actual:  ', out_bits, bits2float( out_bits ), is_inexact
  assert float2bits(out) == out_bits
  assert is_inexact == lib.softfloat_exceptionFlags
  if out != bits2float( out_bits ):
    print "WARNING: bits match but float conversion doesn't!"
  print
  lib.softfloat_exceptionFlags = 0


test_add( 0,                3.5,        2.5, 1.0 )
test_add( 1,              -1234,    -1235.1, 1.1 )
test_add( 1,         3.14159265, 3.14159265, 0.00000001 )
test_add( 0,                3.5,        2.5, 1.0 )
test_add( 1,              -1234,    -1235.1, 1.1 )


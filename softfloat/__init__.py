import struct

#---------------------------------------------------------------------
# bits2float
#---------------------------------------------------------------------
def bits2float( bits ):
  raw_data  = struct.pack( "I", bits )
  conv_data = struct.unpack( "f", raw_data )
  return conv_data[0]

#---------------------------------------------------------------------
# float2bits
#---------------------------------------------------------------------
def float2bits( flt ):
  raw_data  = struct.pack( "f", flt )
  conv_data = struct.unpack( "I", raw_data )
  return conv_data[0]

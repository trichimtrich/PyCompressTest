__author__ = 'chb'

from ctypes import *

cdef extern from"malloc.h":
    extern void free(void* buf)

cdef extern from"wrapQLZ.h":
    extern size_t CompressQuickLZ(char* InBuf,size_t InSize,char** OutBuf)
    extern size_t UncompressQuickLZ(char* InBuf,size_t InSize,char** OutBuf)

def compress(bytes input):
    cdef size_t insize = len(input)
    cdef char* dst=NULL
    outsize= CompressQuickLZ(<char *>input,insize,&dst)
    retval=dst[0:outsize]
    free(dst)
    return retval

def decompress(bytes input):
    cdef size_t insize = len(input)
    cdef char* dst=NULL
    outsize= UncompressQuickLZ(<char *>input,insize,&dst)
    retval=dst[0:outsize]
    free(dst)
    return retval

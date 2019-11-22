#include "quicklz.h"

static size_t CompressQuickLZ(char* InBuf,size_t InSize,char** OutBuf){
    qlz_state_compress state_compress;
    memset(&state_compress,0,sizeof(qlz_state_compress));
    *OutBuf =(char*)malloc(InSize+400);
    size_t OutSize = qlz_compress(InBuf,*OutBuf,InSize,&state_compress);
    if(OutSize==0){
        free(OutBuf);
        return 0;
    }
    return OutSize;
}

static size_t UncompressQuickLZ(char* InBuf,size_t InSize,char** OutBuf){
    qlz_state_decompress state_decompress;
    memset(&state_decompress,0,sizeof(qlz_state_decompress));
    size_t OutSize=qlz_size_decompressed(InBuf);
    *OutBuf =(char*)malloc(OutSize);
    OutSize= qlz_decompress(InBuf,*OutBuf,&state_decompress);
    if(OutSize==0){
        free(OutBuf);
        return 0;
    }
    return OutSize;
}
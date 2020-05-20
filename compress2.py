print("Nibba this is new")
# import time
import sys,os,_heapq,functools,base64,struct,time
from array import array
op=sys.stdout
sys.stdout=open("./input4.bin","wb")
def convert_LZ77(data):
    def longestpresent(word,pos):
        k=1
        while(data[pos:pos+k] in data[0:pos] and pos+k<=len(data)):
            word=data[pos:pos+k]
            k+=1
        return word
    def findlongestpredecessor(word,pos):
        global compressed
        res=0
        word=longestpresent(word,pos)
        res=data.find(word,0,pos)
        if(res==-1 or len(word)<=3):
            compressed=compressed+word
        else:
            compressed=compressed+"{"+str(len(word))+","+str(pos-res)+"}"
        if(res!=-1):
            return len(word)
        return -1
    def iterate():
        global compressed
        i=0
        while(i<len(data)):
            do=findlongestpredecessor(data[i],i)
            if(do!=-1):
                i+=do
            else:
                i+=1
    iterate()

class Tree:
    __slots__=["left","right","val","c"]
    def __init__(self,val,c):
        self.val=val
        self.c=c
        self.left=self.right=None
    def value(self):
        return (self.val,self.c)

def construct(tree):
    while(len(tree)>1):
        left=_heapq.heappop(tree)
        right=_heapq.heappop(tree)
        root=(left[0]+right[0],left[1]+right[1],Tree(left[0]+right[0],left[1]+right[1]))
        root[2].left=left[2]
        root[2].right=right[2]
        _heapq.heappush(tree,root)
    return tree

def Print(root,code,codes):
    global lines
    if(root.left==None and root.right==None):
        codes[root.c]=code
        # lines=int(lines.replace(str(root.c),code))

        return 
    Print(root.left,code+'0',codes)
    Print(root.right,code+'1',codes)

def encode(compressed,codes):
    document=''.join(list(map(lambda x:codes[x],compressed)))
    return document
    time.sleep(0.3)
    # document=compressed
    # document=document.replace('0',chr(254))
    # document=document.replace('1',chr(255))
    # for char in codes:
    #     if(char!='1' and char!='0'):
    #         document=document.replace(char,codes[char])
    # document=document.replace(chr(254),codes['0'])
    # document=document.replace(chr(255),codes['1'])
    # return document


#Write the encoding information(character:huff-code) to the beginning of the output file
def code_write(codes):
    to_write=""                                        #Contains concatenation of codes of all characters(00010100....)
    for char in codes:
        sys.stdout.write(bytes(char,encoding="utf-8")) #Write the character encoding of char in uf-8 format to the binary file
        sys.stdout.write(bytes([len(codes[char])]))    #Write the length of the code of the character to the file
        to_write+=codes[char]
    sys.stdout.write(bytes("\n",encoding="utf-8"))
    sys.stdout.write(bytes([0]))
    # sys.stdout.write(bytes("\n",encoding="utf-8"))
    i=0
    bin_array=array("B")                               #Array to store the codes encoded as integers who binary representation is {to_write}
    while(i<len(to_write)):
        bin_array.append(int(to_write[i:i+8],2))
        i+=8
    sys.stdout.write(bytes([len(bin_array)]))          #Write length of the bin_array
    sys.stdout.write(bytes("\n",encoding="utf-8"))     
    sys.stdout.write(bytes(bin_array))                 #Write the bin_array to the file
    sys.stdout.write(bytes("\n",encoding="utf-8"))
    op1=sys.stdout
    sys.stdout=op
    # print(bin_array,len(bin_array),len(to_write[i-8:]),"Nextstage")
    # to_write_size=bin(len(to_write))[2:]
    sys.stdout=op1
    sys.stdout.write(bytes([len(to_write[i-8:])]))           #Write the length of concatenation of codes
    sys.stdout.write(bytes("\n",encoding="utf-8"))


        
def file_write(document,bin_array):
    i=0
    while(i<len(document)):
        bin_array.append(int(document[i:i+8],2))
        # print(bin_array,document[i:i+8])
        i+=8
    sys.stdout.write(bytes(bin_array))
    op1=sys.stdout
    sys.stdout=op
    # print(bin_array)
    print(i%8,"I",len(document[i-8:]))
    sys.stdout=op1
    sys.stdout.write(bytes([len(document[i-8:])]))
    # return document
# def bin_convert_code(codes):
#     result=''.join()

def write_large_length(length):
    # binary=bin(length)
    # bin_array=array("B")
    # i=0
    # while(i<len(binary)):
    sys.stdout.write(length.to_write(2,"little"))
    



start=time.time()
with open("/home/krishna/Documents/ZipFileCompressor/opt_check.txt","r") as f:
    lines=f.read()
    to_compress=lines
    # to_compress='\n'.join(lines)
# with open("/home/krishna/Documents/ZipFileCompressor/download.jpeg","rb") as image:
#     to_compress=base64.b64decode(image.read())

# to_compress=str(to_compress)
# print(to_compress)
compressed=""
convert_LZ77(to_compress)
res=list(set(compressed))
f=list(map(lambda x: (compressed.count(x),x),res))
# f=list(map(lambda x: (compressed.count(x),x),list(set(to_compress))))
tree=list(map(lambda x: (x[0],x[1],Tree(x[0],x[1])),f))
_heapq.heapify(tree)
root=construct(tree)
codes=dict()
# print(type(root[0][2].left.value()))
lines=compressed
# print(lines)
Print(root[0][2],'',codes)
# print(lines)
# print(repr(compressed))
bin_array=array("B")
document=encode(compressed,codes)
# document=lines
# print(document)
s=1000
# sys.stdout.write(s.to_bytes(2,'little'))
# sys.stdout.write(bytes('1',encoding="ascii"))
# sys.stdout.write(bytes('\n',encoding="ascii"))
code_write(codes)
file_write(document,bin_array)
# sys.stdout.write(bytes)
# write_large_length(len(document))
sys.stdout=op
# print(codes)
# print(s.to_bytes(2,'big'))
# print(bin(1024))
# print(bytes([1]))
# print(int("\n"))
# bin_convert_code(codes)
# print(document[:100])
print(document==lines,"Yes da nibba they work gud")
print(bytes("{",encoding="utf-8"))
print(list(bytes([250]))[0])
print(list(bytes([0])),list(b'0xe2'))
print(bytes([0]).decode("utf-8"))
s="C"
print("\n",len(document),len(to_compress),len(compressed))
print("The time taken to compress the file: %s",{time.time()-start})

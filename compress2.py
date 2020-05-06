import sys,os,_heapq,functools,base64,struct
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
    if(root.left==None and root.right==None):
        codes[root.c]=code
        return 
    Print(root.left,code+'0',codes)
    Print(root.right,code+'1',codes)

def encode(compressed,codes):
    document=''.join(list(map(lambda x:codes[x],compressed)))
    return document

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
    print(bin_array,len(bin_array),len(to_write[i-8:]),"Nextstage")
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
    




with open("/home/krishna/Documents/ZipFileCompressor/world192.txt","r") as f:
    lines=f.readlines()
    to_compress='\n'.join(lines)
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
Print(root[0][2],'',codes)
# print(repr(compressed))
bin_array=array("B")
document=encode(compressed,codes)
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
print(bytes("{",encoding="utf-8"))
print(list(bytes([250]))[0])
print(list(bytes([0])),list(b'0xe2'))
print(bytes([0]).decode("utf-8"))
s="C"
print("\n",len(document),len(to_compress),len(compressed))
print(codes)
with open("/home/krishna/Documents/ZipFileCompressor/input4.bin","rb") as f:
    charcters=[]                              #Stores list of charatcers and their code lengths"[char,codelength]"
    data=''                                   
    #Read the charcters and their code length until consecutive '\n' is encountered in the file
    while(data!="\n"):
        t=[]
        data1=f.read(1).decode('utf-8')
        # print(repr(data1))
        try:
            t.append(data1)
            # print(data)
        except:
            print(data1,"Errorrrrr")
            break
        # data2=f.read(1)
        try:
            data2=f.read(1)
            t.append(list(data2)[0])
            if(list(data2)[0]==0):
                print(list(data2))
                break
            # if(data2.decode("utf-8")=="\n"):
            #     print(data2,data2.decode("utf-8"))
            #     print("Break")
            #     break
        except:
                print(data2,"break")
                break
        print(t,end=" , ")
        charcters.append(t)                 #list that contains the character and its codeword length
    print(charcters)
    #Reading the code words
    char_code=dict()
    data=''
    i=0
    data=f.read(2)
    # print(data)
    size=list(data)[0]                     #Size of array of encoded integers to read
    # print(size)
    data=f.read(size+1)
    # print(list(data))
    arr=list(data)[:-1]                    #Array of encoded numbers concatenation of whose binary representation 
    print(arr)
    decoded=''                             #String to store the concatenation of binary rep of character codes([1,2,3..]->(0001001110..))
    for i in arr[:-1]:
        binary=bin(i)[2:]
        zeroes=''.join(['0' for i in range(8-len(binary))])   #Concatenate any additional zeroes lost in 80bit rep. of the number
        decoded+=zeroes+binary

    #Read the length of the encoded character code string
    data=f.read(2)
    code_size=list(data)[0]
    binary=bin(arr[-1])[2:]
    # print(binary)
    zeroes=''.join(['0' for i in range(code_size-len(binary))])
    decoded+=zeroes+binary
    # print(decoded)                                            #Decoded-String that contains the codeword
    # print(data)
    # print(charcters)

    #Read the encoded document content
    data=f.read()
    decoded=''                                                #Decodedstring :- concatenation of huff-code rep of the enite document contents
    # print(bin_array==list(data)[:-1])
    # print(list(data)[0],"Encoded i")
    arr_document=list(data)[:-1]                              #Array of int numbers concatenation of whose binary rep. enitire document
    # print(arr_document)
    doc_length=list(data)[-1]                                 #The residual difference between the encoded document length and the whole document length
    for i in arr_document[:-1]:
        binary=bin(i)[2:]
        zeroes=''.join(['0' for i in range(8-len(binary))])
        decoded+=zeroes+binary
        # print(i,zeroes+binary)
    print()
    print(len(decoded),len(document))
    # doc_length=arr_document[-1]
    binary=bin(arr_document[-1])[2:]
    zeroes=''.join(['0' for i in range(doc_length-len(binary))])
    print(len(document)-len(decoded),"DIFF",doc_length)
    decoded+=zeroes+binary
    # print(bin_array==arr_document)
    # print(bin_array[-1],arr[-1],document[-3:-1])
    # print(decoded[-10:-1],document[-10:-1])
    print(decoded==document)
    # s=1000000
    # print(s.to_bytes(2,"little"))
    # print(codes)
    # print(compressed)




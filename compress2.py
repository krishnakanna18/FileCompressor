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

def code_write(codes):
    # op1=sys.stdout
    # sys.stdout=op
    # # print(codes)
    # for char in codes:
    #     # try:
    #     print(char,codes[char])
    # sys.stdout=op1
    to_write=""
    for char in codes:
        sys.stdout.write(bytes(char,encoding="utf-8"))
        sys.stdout.write(bytes([len(codes[char])]))
        to_write+=codes[char]
    sys.stdout.write(bytes("\n",encoding="utf-8"))
    i=0
    bin_array=array("B")
    while(i<len(to_write)):
        bin_array.append(int(to_write[i:i+8],2))
        i+=8
    sys.stdout.write(bytes([len(bin_array)]))
    sys.stdout.write(bytes("\n",encoding="utf-8"))
    sys.stdout.write(bytes(bin_array))
    sys.stdout.write(bytes("\n",encoding="utf-8"))
    sys.stdout.write(bytes([len(to_write)]))
    sys.stdout.write(bytes("\n",encoding="utf-8"))


        
def file_write(document,bin_array):
    i=0
    while(i<len(document)):
        bin_array.append(int(document[i:i+8],2))
        # print(bin_array,document[i:i+8])
        i+=8
    sys.stdout.write(bytes(bin_array))
    # return document
# def bin_convert_code(codes):
#     result=''.join()


with open("/home/krishna/Documents/ZipFileCompressor/test-data.txt","r") as f:
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
sys.stdout=op
# print(codes)
# print(s.to_bytes(2,'big'))
# print(bin(1024))
# print(bytes([1]))
# print(int("\n"))
# bin_convert_code(codes)
# print(document[:100])
print(bytes("{",encoding="utf-8"))
print("\n",len(document),len(to_compress),len(compressed))
with open("/home/krishna/Documents/ZipFileCompressor/input4.bin","rb") as f:
    # print(f.read(1))
    # print(f.read(1).decode('utf-8'))
    # data=''
    # while(data!="\n"):
    #     data=f.read(1).decode('utf-8')
    #     print(data,"a")
    #     print("got")
    # while(list(f.read(1))[0]!=10):
    #     print(f.read(1))
    
    #Reading the characters and their code sizes
    charcters=[]
    data=''
    while(data!="\n"):
        t=[]
        data=f.read(1).decode('utf-8')
        # print(data)
        if(data=="\n"):
            break
        try:
            t.append(data)
        except:
            print(data,"Erro")
            break
        data=f.read(1)
        try:
            t.append(list(data)[0])
        except:
            print(data,"Eroor")
            print(list(data))
            break
        charcters.append(t) #list that contains the character and its codeword length
    
    #Reading the code words
    char_code=dict()
    data=''
    i=0
    #Reading the size of code array
    while(data!="\n"):
        data=f.read(1)
        if(data.decode('utf-8')=="\n"):
            break
    size=list(data)[0]
    data=f.read(size)
    print(list(data))
    arr=list(data)
    decoded=''
    for i in arr[:-2]:
        binary=bin(i)[2:]
        zeroes=''.join(['0' for i in range(8-len(binary))])
        decoded+=zeroes+binary
    #Reading the size of code string
    data=''
    while(data!="\n"):
        data=f.read(1)
        if(data.decode('utf-8')=="\n"):
            break
    code_size=list(data)[0]
    binary=bin(arr[-2])[2:]
    print(binary)
    zeroes=''.join(['0' for i in range(code_size-len(decoded)-len(binary))])
    decoded+=zeroes+binary
    print(decoded) # decoded-String that contains the codeword
    # print(data)
    print(charcters)
    data=f.read()
    decoded=''
    # print(bin_array==list(data))
    # print(list(data)[0],"Encoded i")
    arr=list(data)
    for i in arr[:-1]:
        # print(i,bin(i)[2:])
        # print(bin(i))
        binary=bin(i)[2:]
        zeroes=''.join(['0' for i in range(8-len(binary))])
        decoded+=zeroes+binary
        # print(i,zeroes+binary)
    print()
    # print(len(decoded),len(document))
    binary=bin(arr[-1])[2:]
    zeroes=''.join(['0' for i in range(len(document)-len(decoded)-len(binary))])
    decoded+=zeroes+binary
    # print(bin_array[-10:-1],arr[-10:-1])
    # print(bin_array[-1],arr[-1],document[-3:-1])
    # print(decoded[-10:-1],document[-10:-1])
    print(decoded==document)
    print(codes)
    # print(compressed)




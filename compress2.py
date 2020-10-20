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

# Construct the coding scheme tree
def construct(tree):
    while(len(tree)>1):
        left=_heapq.heappop(tree)
        right=_heapq.heappop(tree)
        root=(left[0]+right[0],left[1]+right[1],Tree(left[0]+right[0],left[1]+right[1]))
        root[2].left=left[2]
        root[2].right=right[2]
        _heapq.heappush(tree,root)
    return tree


# Construct the code for the tree
def find_code(root,code,codes):
    global lines
    if(root.left==None and root.right==None):
        codes[root.c]=code
        return 
    find_code(root.left,code+'0',codes)
    find_code(root.right,code+'1',codes)


# Encode the characters in compressed corresponding to codes
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
    sys.stdout.write(bytes([len(document[i-8:])]))
    # return document

def write_large_length(length):
    # binary=bin(length)
    # bin_array=array("B")
    # i=0
    # while(i<len(binary)):
    sys.stdout.write(length.to_write(2,"little"))
    



start=time.time()
with open("/home/krishna/Documents/ZipFileCompressor/input2.txt","r") as f:
    lines=f.read()
    to_compress=lines
    
compressed=to_compress
f=list(map(lambda x: (compressed.count(x),x),list(set(to_compress))))
tree=list(map(lambda x: (x[0],x[1],Tree(x[0],x[1])),f))
_heapq.heapify(tree)
root=construct(tree)
codes=dict()
lines=compressed
# print(lines)
find_code(root[0][2],'',codes)
bin_array=array("B")
document=encode(compressed,codes)
s=1000
# Write the codes onto the file
code_write(codes)
# Write the document onto the file
file_write(document,bin_array)

sys.stdout=op
print("The time taken to compress the file: %s",{time.time()-start})

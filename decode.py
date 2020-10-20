
def mapcode_to_char(codewords,characters):
    char_map=dict()
    i=0
    for char,count in characters:
        char_map[char]=codewords[i:i+count]
        i+=count
    # print(char_map==compress2.codes,"Oh yes")
    return char_map

def retrieveodoc(decoded,char_map,code_map):

    def findfirstcode(i):
        k=0
        while(decoded[i:i+k] not in code_map):
            k+=1
            continue
        document=code_map[decoded[i:i+k]]
        return (document,i+k)

    document=''
    i=0
    while(i<len(decoded)):
        res=findfirstcode(i)
        document+=res[0]
        i=res[1]

    with open("opfile.txt","w") as f:
        f.write(document)

    
with open("/home/krishna/Documents/ZipFileCompressor/input4.bin","rb") as f:
    characters=[]                              #Stores list of charatcers and their code lengths"[char,codelength]"
    data=''                                   
    #Read the characters and their code length until consecutive '\n' is encountered in the file
    while(data!="\n"):
        t=[]
        data1=f.read(1).decode('utf-8')
        try:
            t.append(data1)
        except:
            print(data1,"Errorrrrr")
            break
        try:
            data2=f.read(1)
            t.append(list(data2)[0])
            if(list(data2)[0]==0):
                # print(list(data2))
                break
        except:
                print(data2,"break")
                break
        characters.append(t)                 #list that contains the character and its codeword length
    # print(characters,"The characters and their huffman code")
    #Reading the code words
    char_code=dict()
    data=''
    i=0
    data=f.read(2)
    # print(data)
    size=list(data)[0]                     #Size of array of encoded integers to read
    data=f.read(size+1)
    arr=list(data)[:-1]                    #Array of encoded numbers concatenation of whose binary representation 
    decoded=''                             #String to store the concatenation of binary rep of character codes([1,2,3..]->(0001001110..))
    for i in arr[:-1]:
        binary=bin(i)[2:]
        zeroes=''.join(['0' for i in range(8-len(binary))])   #Concatenate any additional zeroes lost in 8bit rep. of the number
        decoded+=zeroes+binary

    #Read the length of the encoded character code string
    data=f.read(2)
    code_size=list(data)[0]
    binary=bin(arr[-1])[2:]
    # print(binary)
    zeroes=''.join(['0' for i in range(code_size-len(binary))])
    decoded+=zeroes+binary
    codewords=decoded[:]
    char_map=mapcode_to_char(codewords,characters)
    code_map={v:k for k,v in char_map.items()}
   

    #Read the encoded document content
    data=f.read()
    decoded=''                                                #Decodedstring :- concatenation of huff-code rep of the enite document contents
    arr_document=list(data)[:-1]                              #Array of int numbers concatenation of whose binary rep. enitire document
    doc_length=list(data)[-1]                                 #The residual difference between the encoded document length and the whole document length
    for i in arr_document[:-1]:
        binary=bin(i)[2:]
        zeroes=''.join(['0' for i in range(8-len(binary))])
        decoded+=zeroes+binary
        # print(i,zeroes+binary)
    binary=bin(arr_document[-1])[2:]
    zeroes=''.join(['0' for i in range(doc_length-len(binary))])
    decoded+=zeroes+binary
    document=retrieveodoc(decoded,char_map,code_map)
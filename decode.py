import compress2
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
    # print(charcters)
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
    # print(arr)
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
    # print(len(decoded),len(document))
    # doc_length=arr_document[-1]
    binary=bin(arr_document[-1])[2:]
    zeroes=''.join(['0' for i in range(doc_length-len(binary))])
    # print(len(document)-len(decoded),"DIFF",doc_length)
    decoded+=zeroes+binary
    # print(bin_array==arr_document)
    # print(bin_array[-1],arr[-1],document[-3:-1])
    # print(decoded[-10:-1],document[-10:-1])
    print(decoded==compress2.document)
    # s=1000000
    # print(s.to_bytes(2,"little"))
    # print(codes)
    # print(compressed)
    print(len(decoded))
#!/usr/bin/env python
# coding: utf-8

# <h1><center>INNOVATIVE ASSIGNMENT</center></h1>
# <h2>TOPIC :- HUFFMAN ENCODING</h2>

# <b>Course Name and Code :- </b>Design and Analysis of Algorithm (2CS503)<br>
# <b>Roll No and Name :-</b> 21BCE504 (Shashank Chaudhary)<br><hr>

# <h2> What is Huffman Encoding? </h2><br>
# Huffman coding is a lossless data compression algorithm. The idea is to assign variable-length codes to input characters, lengths of the assigned codes are based on the frequencies of corresponding characters. The most frequent character gets the smallest code and the least frequent character gets the largest code.<br>
# <br>
# --> There are two major parts used in Huffman Encoding :- <br>
# 1) Build a Huffman Tree from Input Characters <br>
# 2) Traverse a Huffman Tree and assign codes to characters <br> <hr>

# <h2>Steps for Building Huffman Tree</h2><br>
# Input is an array of unique characters along with their frequency of occurrences and output is Huffman Tree.<br>
# 1. Create a leaf node for each unique character and build a min heap of all leaf nodes (Min Heap is used as a priority queue. The value of frequency field is used to compare two nodes in min heap. Initially, the least frequent character is at root)<br>
# 2. Extract two nodes with the minimum frequency from the min heap.<br>
# 3. Create a new internal node with a frequency equal to the sum of the two nodes frequencies. Make the first extracted node as its left child and the other extracted node as its right child. Add this node to the min heap.<br>
# 4. Repeat steps#2 and #3 until the heap contains only one node. The remaining node is the root node and the tree is complete.<br><hr>
# 

# <h2>EXAMPLE:</h2><br>
# 
# ![image.png](attachment:image.png)

# <h4>Step-1 :- </h4>Build a min heap that contains 6 nodes where each node represents root of a tree with single node.<br>
# <h4>Step-2 :- </h4>Extract two minimum frequency nodes from min heap. Add a new internal node with frequency 5 + 9 = 14.<br>
# 
# ![image.png](attachment:image.png)
# 
# Now min heap contains 5 nodes where 4 nodes are roots of trees with single element each, and one heap node is root of tree with 3 elements.
# 
# ![image-2.png](attachment:image-2.png)
# 
# <h4>Step-3 :- </h4>Extract two minimum frequency nodes from heap. Add a new internal node with frequency 12 + 13 = 25.
# 
# ![image-3.png](attachment:image-3.png)
# 
# Now min heap contains 4 nodes where 2 nodes are roots of trees with single element each, and two heap nodes are root of tree with more than one nodes.
# 
# ![image-4.png](attachment:image-4.png)
# 
# <h4>Step-4 :- </h4>Extract two minimum frequency nodes. Add a new internal node with frequency 14 + 16 = 30.
# 
# ![image-5.png](attachment:image-5.png)
# 
# Now min heap contains 3 nodes.
# 
# ![image-6.png](attachment:image-6.png)
# 
# <h4>Step-5 :- </h4>Extract two minimum frequency nodes. Add a new internal node with frequency 25 + 30 = 55.
# 
# ![image-7.png](attachment:image-7.png)
# 
# Now min heap contains 2 nodes.
# 
# ![image-8.png](attachment:image-8.png)
# 
# <h4>Step-6 :- </h4>Extract two minimum frequency nodes. Add a new internal node with frequency 45 + 55 = 100.
# 
# ![image-9.png](attachment:image-9.png)
# 
# Now min heap contains only one node.
# 
# ![image-10.png](attachment:image-10.png)
# 
# <h2>Since the heap contains only one node, the algorithm stops here.</h2><hr>

# <h3>Steps for Extracting Code from Huffman Tree.</h3>
# Traverse the tree formed starting from the root. Maintain an auxiliary array. While moving to the left child, write 0 to the array. While moving to the right child, write 1 to the array. Print the array when a leaf node is encountered.
# 
# ![image.png](attachment:image.png)
# 
# <h4>Codes are as follows : </h4>
# 
# ![image-2.png](attachment:image-2.png)

# In[7]:


import heapq
import os


# In[8]:


class BinaryTree:
    def __init__(self,value,frequency):
        self.value = value
        self.frequency = frequency
        self.left = None
        self.right = None
    
    def __lt__(self,other):
        return self.frequency < other.frequency
    
    def __eq__(self,other):
        return self.frequency == other.frequency


# In[9]:


class Huffmancode:
    def __init__ (self,path):
        self.path = path
        self.__heap = []
        self.__code = {}
        self.__revCode = {}
    
    def __frequency_from_text(self,text):
        frequency_dict = {}
        for char in text:
            if char not in frequency_dict:
                frequency_dict[char] = 1
            else:
                frequency_dict[char] += 1
        return frequency_dict
    
    def __BuildHeap(self,frequency_dict):
        for key in frequency_dict:
            frequency = frequency_dict[key]
            binaryTreeNode = BinaryTree(key,frequency)
            heapq.heappush(self.__heap, binaryTreeNode)
            
    def __BuildBinaryTree(self):
        while len(self.__heap)>1:
            binaryTreeNode1 = heapq.heappop(self.__heap)
            binaryTreeNode2 = heapq.heappop(self.__heap)
            sum_of_frequency = binaryTreeNode1.frequency + binaryTreeNode2.frequency
            newNode = BinaryTree(None,sum_of_frequency)
            newNode.left = binaryTreeNode1
            newNode.right = binaryTreeNode2
            heapq.heappush(self.__heap,newNode)
        return 
    
    def __BuildTreeCodeHelper(self,root,currBits):
        if root is None:
            return
        if root.value is not None:
            self.__code[root.value] = currBits
            self.__revCode[currBits] = root.value
            return
        self.__BuildTreeCodeHelper(root.left,currBits+'0')
        self.__BuildTreeCodeHelper(root.right,currBits+'1')
    
    def __BuildTreeCode(self):
        root = heapq.heappop(self.__heap)
        self.__BuildTreeCodeHelper(root,'')
    
    def __BuildEncodedText(self,text):
        encodedText = ''
        for char in text:
            encodedText += self.__code[char]
        return encodedText
    
    def __BuildPaddedText(self,encodedText):
        paddingValue = 8-len(encodedText)%8
        for i in range(paddingValue):
            encodedText += '0'
        paddedInfo = "{0:08b}".format(paddingValue)
        paddedText = paddedInfo + encodedText
        return paddedText
    
    def __BuildBytesArray(self,paddedText):
        array = []
        for i in range(0,len(paddedText),8):
            byte = paddedText[i:i+8]
            array.append(int(byte,2))
        return array
    
    def Compression(self):
        print("COMPRESSION STARTED...")
        fileName,fileExtension = os.path.splitext(self.path)
        outputPath = fileName + '.bin'
        with open(self.path,'r+',encoding='utf-8') as file, open(outputPath,'wb') as output:
            text = file.read()
            text = text.rstrip()
            frequency_dict = self.__frequency_from_text(text)
            print(frequency_dict)
            buildHeap = self.__BuildHeap(frequency_dict)
            self.__BuildBinaryTree()
            self.__BuildTreeCode()
            encodedText = self.__BuildEncodedText(text)
            paddedText = self.__BuildPaddedText(encodedText)
            bytesArray = self.__BuildBytesArray(paddedText)
            finalBytes = bytes(bytesArray)
            output.write(finalBytes)
        print("FILE COMPRESSED SUCCESSFULLY!!!")
        return outputPath
    
    def __RemovePadding(self,text):
        paddedInfo = text[:8]
        paddingValue = int(paddedInfo,2)
        text = text[8:]
        text = text[:-1*paddingValue]
        return text
    
    def __DecodedText(self,text):
        currentBits = ''
        decodedText = ''
        for char in text:
            currentBits += char
            if currentBits in self.__revCode:
                decodedText += self.__revCode[currentBits]
                currentBits = ''
        return decodedText
    
    def Decompress(self,inputPath):
        fileName,fileExtension = os.path.splitext(inputPath)
        outputPath = fileName+'_decomposed'+'.txt'
        with open(inputPath,'rb') as file,open(outputPath,'w') as output:
            bitString = ''
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8,'0')
                bitString += bits
                byte = file.read(1)
            textAfterRemovingPadding = self.__RemovePadding(bitString)
            actualText = self.__DecodedText(textAfterRemovingPadding)
            output.write(actualText)
        return outputPath


# In[10]:


path = input("ENTER THE PATH OF YOUR FILE TO COMPRESS : ")
ob1 = Huffmancode(path)
compressedFile = ob1.Compression()
ob1.Decompress(compressedFile)


# <h2>Time Complexity :- </h2>O(nlogn)
# <h2>Space Complexity :- </h2>O(K) for tree and O(N) for Decoded Text<hr>

# <h2>Applications :- </h2><br>
# 1. They are used for transmitting fax and tax.<br>
# 2. They are used by conventional compression formats like PKZIP,GZIP etc.<br>
# 3. Multimedia codecs like JPEG, PNG, and MP3 use Huffman Encoding.<br>
# <br>
# It is useful in cases where there is a series of frequently occuring characters.

# In[ ]:





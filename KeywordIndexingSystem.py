#Defined a TrieNode Class which contains the pointers to the next present character 
#If the current TrieNode is a terminal character, it also stores the document indices in a set

class TrieNode:
    __links=[]          #contains index of next character
    __indices=set()     #contains document indices

    def __init__(self):         #initialises links to -1 for all characters
        self.__links=[-1]*26 
        self.__indices=set()

    def containsKey(self,ch: chr) -> bool:          #returns true if next character is present
        return self.__links[ord(ch)-ord('a')]!=-1

    def setKey(self,ch: chr,index: int):            #sets index of next character
        self.__links[ord(ch)-ord('a')]=index

    def getKey(self,ch: chr) -> int:                #retrieves index of next character
        return self.__links[ord(ch)-ord('a')]
    
    def insertIndex(self,index: int):               #inserts document index in set
        self.__indices.add(index)
    
    def getIndices(self) -> set:                    #returns document indices set
        return self.__indices
    
    def debug(self):
        print(id(self.__indices))
    
#Defined the Trie Data Structure which stores all present keywords efficiently
class Trie:
    __nodes=[]

    def __init__(self):                     #initialises nodes with an empty TrieNode
        self.__nodes.append(TrieNode())

    def insertWord(self,word: str,index: int):  #inserts word into the Trie
        curr=0
        for ch in word:
            if(not self.__nodes[curr].containsKey(ch)):
                self.__nodes.append(TrieNode())
                self.__nodes[curr].setKey(ch,len(self.__nodes)-1)
            curr=self.__nodes[curr].getKey(ch)
        self.__nodes[curr].insertIndex(index+1)

    def findWord(self,word: str) -> set:    #returns document indices where keyword is present
        curr=0
        for ch in word:
            if(not self.__nodes[curr].containsKey(ch)):
                return {}
            curr=self.__nodes[curr].getKey(ch)
        return self.__nodes[curr].getIndices()
    
    def debugger(self):
        for node in self.__nodes:
            node.debug()
    

#   Main Code

obj=Trie()
num_of_documents=int(input("Enter the number of documents you wish to index\n"))
for i in range(0,num_of_documents):
    s=input()
    s+=' '
    word=""
    for ch in s:
        if('a'<=ch<='z' or 'A'<=ch<='Z'):
            word+=ch
        else:
            if(len(word)>0):
                obj.insertWord(word.lower(),i)
                word=""

while(True):
    keyword=input("\nEnter the keyword you wish to search\n")
    if(keyword==""):
        break
    print("keyword is present in document(s) with indice(s) ",obj.findWord(keyword.lower()),"\n")
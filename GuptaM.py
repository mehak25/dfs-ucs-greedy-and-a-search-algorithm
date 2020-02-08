import sys
import numpy as np
from prettytable import PrettyTable


#get input from user
input=input("Please enter input sequence: ")
seq=""


#implement search tree
class Node(object):
    def __init__(self, data,children,parent,cost,priority,heuristic,flip):
        self.data = data
        self.children = []
        self.parent=parent
        self.cost=cost
        self.priority=priority
        self.heuristic=heuristic
        self.flip=flip

    def add_child(self, obj):
        self.children.append(obj)

    def __cmp__(self,other):
        return self.data > other.data

#PriorityQueue Implementation
class PriorityQueue(object):
    def __init__(self):
        self.queue = list()

    def size(self):
        return len(self.queue)

    def empty(self):
        return len(self.queue) == []
    
    def insert(self, node):
        # if queue is empty
        if self.size() == 0:
          # add the new node
          self.queue.append(node)
        else:
          # traverse the queue to find the right place for new node
          for x in range(0, self.size()):
            # if the priority of new node is greater
            if node.priority > self.queue[x].priority:
                # if at the end of queue
                if x == (self.size()-1):
                    # add new node at the end
                    self.queue.insert(x+1, node)
                else:
                    continue
            #if priority is same, tie-break with sequence ids
            elif node.priority == self.queue[x].priority:
                #tie-breaking with putting larger node value last
                if node.data < self.queue[x].data:
                    # if at the end of queue
                    if x == (self.size()-1):
                        # add new node at the end
                        self.queue.insert(x+1, node)
                    else:
                        continue
                else:
                    self.queue.insert(x, node)
                    return True
            else:
              self.queue.insert(x, node)
              return True
      
    def delete(self):
        # remove the first node from the queue
        return self.queue.pop(0)
        

    def show(self):
        y = PrettyTable()
        y.field_names = ["FLip Sequence","Node Sequence", "Priority Value(f)", "Cost of Path(g)","Heuristic(h)"]
        for x in self.queue:
            y.add_row([x.flip,x.data, str(x.priority), x.cost,x.heuristic])
        print(y)
          
#print sequence of all nodes selected during the process
def printCandidates():
    y = PrettyTable()
    y.field_names = ["FLip Sequence","Node Sequence", "Priority Value(f)", "Cost of Path(g)","Heuristic(h)"]
    for x in candidates:
        y.add_row([x.flip,x.data, str(x.priority), x.cost,x.heuristic])
    print(y)
    
#goal test to see if we reached goal node and return the total commulative cost            
def goalTest(parent):
    if(parent is None):
        print("-----------------------------------------------------")
        print("Search Failed!!!")
        return False
    elif(parent.data=='4321'):
        print("-----------------------------------------------------")
        print("Goal Reached!!!")
        print("Total cost of path is "+ str(parent.cost))
        print("----------Below is the sequence of all candidates selected in each step------------")
        printCandidates()
        return True
    else:
        return False
    
#find candidate for expansion based on search strategy
def findCandidate(fringe,visited):   
        print("-------------Candidate choosen for expansion from fringe--------------")
        x = PrettyTable()
        cand=fringe.delete()
        #pop the items from queue until you find node that is not visited
        while(cand.data in visited):
            cand=fringe.delete()
        x.field_names = ["FLip Sequence","Node Sequence", "Priority Value(f)", "Cost of Path(g)","Heuristic(h)"]
        x.add_row([cand.flip,cand.data, str(cand.priority), cand.cost,cand.heuristic])
        print("Candidate Sequence choosen")
        print(x)
        #make the selected candidate new parent
        parent=cand
        candidates.append(parent)
        return parent,fringe

#calculate heuristic
def calculateHeuristic(child):
    heuristic=0
    #find the largest pancake out of order
    if(child.data.index('4') != 0):
        heuristic=4
    elif(child.data.index('3') != 1):
        heuristic=3
    elif(child.data.index('2') != 2):
        heuristic=2
    return heuristic

#update fringe with priority as per the a* strategy - priority in queue is heuristic + commulative cost
def aStar(fringe,children,visited,flips,parent):
    if(len(children)!=0):
        #update fringe
        for child,flip in zip(children,flips):
            if(child.data not in visited):# do not add element on fringe if that is already visited
                heuristic=calculateHeuristic(child) #find heuristic
                child.heuristic=heuristic #update heuristic
                child.priority=heuristic+child.cost #heuristic + commulative cost is priority
                fringe.insert(child)

        #findCandidate
        if not fringe.empty():
            #print updated fringe
            print("-----------------------Updated Fringe Data-------------------------")
            print(fringe.show())

            #find candidate
            parent,fringe=findCandidate(fringe,visited)
            #add candiadte to visited list
            visited.append(parent.data)
            return parent,fringe,visited
        #if goal is not reached and fringe is empty than return
        else:
            return None,None

#update fringe with priority as per the greedy strategy - priority in queue is heuristic
def greedy(fringe,children,visited,flips,parent):
    if(len(children)!=0):
        #update fringe
        for child,flip in zip(children,flips):
            if(child.data not in visited):# do not add element on fringe if that is already visited
                heuristic=calculateHeuristic(child) #find heuristic
                child.heuristic=heuristic #update heuristic
                child.priority=heuristic #heuristic is priority
                fringe.insert(child) #add element to fringe

        #findCandidate from fringe
        if not fringe.empty():
            #print updated fringe
            print("-----------------------Updated Fringe Data-------------------------")
            print(fringe.show())

            #find candidate
            parent,fringe=findCandidate(fringe,visited)
            #add candiadte to visited list
            visited.append(parent.data)
            return parent,fringe,visited
        #if goal is not reached and fringe is empty than return
        else:
            return None,None

#update fringe with priority as per the ucs strategy - priority is commulative cost
def ucs(fringe,children,visited,flips,parent):
    if(len(children)!=0):
        #update fringe
        for child,flip in zip(children,flips):
            if(child.data not in visited):# do not add element on fringe if that is already visited
                heuristic=calculateHeuristic(child) #find heuristic
                child.heuristic=heuristic #update heuristic
                child.priority=child.cost #commulative cost is priority in ucs strategy
                fringe.insert(child) #add element to fringe

        #findCandidate
        if not fringe.empty():
            #print updated fringe
            print("-----------------------Updated Fringe Data excluding nodes already visited-------------------------")
            print(fringe.show())

            #find candidate from fringe
            parent,fringe=findCandidate(fringe,visited)
            
            #add candiadte to visited list
            visited.append(parent.data)
            return parent,fringe,visited
        #if goal is not reached and fringe is empty than return
        else:
            return None,None,visited
        
#update fringe with priority as per the dfs strategy - priority is negative of depth of the node
def dfs(fringe,children,visited,flips,parent):
    if(len(children)!=0):
        #update fringe
        for child,flip in zip(children,flips):
            if(child.data not in visited):# do not add element on fringe if that is already visited
                child.priority=parent.priority-1 #priority for elements in fringe is negative of depth
                heuristic=calculateHeuristic(child) #find heuristic
                child.heuristic=heuristic #update heuristic
                fringe.insert(child) #add element to fringe

        #findCandidate from fringe
        if not fringe.empty():
            #print updated fringe
            print("-----------------------Updated Fringe Data-------------------------")
            print(fringe.show())
            
            #find candidate
            parent,fringe=findCandidate(fringe,visited)
            
            #add candiadte to visited list
            visited.append(parent.data)
            return parent,fringe,visited
        #if goal is not reached and fringe is empty than return NULL
        else:
            return None,None,visited

#find new nodes to be added on fringe
def findChildNodes(parent):
    children=[]
    flips=[]
    seq=parent.data
    #Flip pancakes from last pancake
    child1=seq[4::-1]
    flip1='|'+seq[:]
    #Flip pancakes from second pancake from bottom
    child2=seq[0] + seq[4:0:-1]
    flip2=seq[:1]+'|'+seq[1:]
    #Flip pancakes from 3 pancake from bottom
    child3=seq[0:2] + seq[4:1:-1]
    flip3=seq[:2]+'|'+seq[2:]
    #create nodes with commulative cost and initiate priority and heuristic with 0
    c1=Node(child1,None,parent,parent.cost+4,0,0,flip1)
    c2=Node(child2,None,parent,parent.cost+3,0,0,flip2)
    c3=Node(child3,None,parent,parent.cost+2,0,0,flip3)
    #make a list of all child nodes
    children.append(c1)
    children.append(c2)
    children.append(c3)
    #add flip sequence representations
    flips.append(flip1)
    flips.append(flip2)
    flips.append(flip3)
    #add child nodes to graph search tree
    parent.add_child(c1)
    parent.add_child(c2)
    parent.add_child(c3)
    return children,flips
        

#General Search implementation
def search(fringe,parent,visited,counter):
    #loop until you reach goal state
    while not goalTest(parent):
        counter=counter+1
        print("******************************* STEP "+ str(counter) +" *******************************")
        #expand parent node and find its children
        children,flips=findChildNodes(parent)
        #call the function for the algorithm
        if(algo=="d"):
            parent,fringe,visited=dfs(fringe,children,visited,flips,parent)
        elif(algo=="u"):
            parent,fringe,visited=ucs(fringe,children,visited,flips,parent)
        elif(algo=="g"):
            parent,fringe,visited=greedy(fringe,children,visited,flips,parent)
        elif(algo=="a"):
            parent,fringe,visited=aStar(fringe,children,visited,flips,parent)
       
    
#Initialize all variables
def initialize(input):
    global counter
    counter=0
    print("---------Initial Variable-------------")
    global seq
    seq=input[0:4]
    print("Given Sequence = " + seq)
    #create root node
    parent=Node(seq,None,None,0,0,0,None)
    global algo
    algo =input[4]
    print("Algorithm = " + algo)
    fringe=PriorityQueue()
    #fringe.insert(parent)
    global candidates
    candidates=[]
    candidates.append(parent)
    visited=[]
    visited.append(parent.data)
    search(fringe,parent,visited,counter)


#Validate Input and call Search
def validateInput():
    if(len(input)==5):
        if(input.find('1') != -1 & input.find('2') != -1 &
           input.find('3') != -1 & input.find('4') != -1):
            if(input[4]=="d" or input[4]=="u" or input[4]=="g" or input[4]=="a"):
                initialize(input)
            else:
                print ("Invalid Input") 
        else:
            print ("Invalid Input")
    else:
        print ("Invalid Input") 

#Main
validateInput()   
    

    

#import numpy as np

class Matrix:
    __mat=[]
    __n=0
    __m=0
    def __init__(self,n: int,m: int,val=0):
        self.__n=n
        self.__m=m
        self.__mat=[[val for _ in range(m)] for i in range(n)]

    def __len__(self):
        return self.__n
    
    def __getitem__(self,i: int):
        return self.__mat[i]

    def __add__(self,other):
        res=Matrix(len(self),len(self[0]))
        for i in range(len(self)):
            for j in range(len(self[i])):
                res[i][j]=self[i][j]+other[i][j]
        return res

    def __sub__(self,other):
        res=Matrix(len(self),len(self[0]))
        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                res[i][j]=self[i][j]-other[i][j]
        return res
    
    def __mul__(self,other):
        n=len(self)
        m=len(other)
        res=Matrix(n,m)
        for i in range(n):
            for j in range(m):
                for k in range(m):
                    res[i][j]+=self[i][k]*other[k][j]
        return res

    def __pow__(self,t: int):
        n=len(self)
        res=Matrix(n,n)
        for i in range(n):
            res[i][i]=1
        while(t):
            if(t&1):
                res=res*self
            self=self*self
            t=int(t/2)
        return res
    
    def t(self):
        transpose=Matrix(self.__m,self.__n)
        for i in range(self.__n):
            for j in range(self.__m):
                transpose[j][i]=self[i][j]
        return transpose
    
    def getMat(self):
        return self.__mat

#   Calculates page rank after every iteration, updating for each edge (Slow)
#   Time Complexity: O(max_iterations*number_of_outgoing_edges)
def PageRankIterative(adj_matrix: list,d=0.85, max_iterations=100,tol=1e-6) -> list:
    adj_list=[]
    n=len(adj_matrix)
    for i in range(n):
        adj_list.append([])
        for j in range(n):
            if(adj_matrix[i][j]):
                adj_list[i].append(j)
    current_rank=[1/n for _ in range(n)]
    for _ in range(0,max_iterations):
        new_rank=[(1-d)/n]*n
        for i in range(n):
            for j in adj_list[i]:
                new_rank[j]+=d*(current_rank[i]/len(adj_list[i]))
        max_diff=max((abs(new_rank[page]-current_rank[page])) for page in range(0,n))
        if(max_diff<tol):
            break
        current_rank=new_rank
    return current_rank

#   Calculates page rank using transition probability matrix (More Efficient)
#   Time Complexity: O(log(max_iterations)*(n^3))
def PageRank(adj_matrix: list,d=0.85, max_iterations=100,tol=1e-6) -> Matrix:
    n=len(adj_matrix)
    current_rank=Matrix(1,n,1/n)
    transition_probability_matrix=Matrix(n,n,(1-d)/n)
    for i in range(n):
        num_neighbors=sum(adj_matrix[i])
        for j in range(0,n):
            if(adj_matrix[i][j]):
                transition_probability_matrix[i][j]+=d/num_neighbors    
    #return np.matmul(current_rank,np.linalg.matrix_power(transition_probability_matrix,max_iterations))
    res=current_rank*(transition_probability_matrix**max_iterations)
    return res.getMat()[0]

def HITS(adj_matrix: list,d=0.85, max_iterations=100,tol=1e-6):
    n=len(adj_matrix)
    A=Matrix(n,n)
    for i in range(n):
        for j in range(n):
            A[i][j]=adj_matrix[i][j]
    auth_weight=(Matrix(1,n,1)*((A.t()*A)**max_iterations))[0]
    hub_weight=(Matrix(1,n,1)*((A*A.t())**max_iterations))[0]
    norm_auth_weight=[i/sum(auth_weight) for i in auth_weight]
    norm_hub_weight=[i/sum(hub_weight) for i in hub_weight]
    return norm_auth_weight,norm_hub_weight

n=int(input("Enter the number of pages\n"))
print(n)
adj_matrix=[]
for i in range(0,n):
    adj_matrix.append([])
    s=input()
    s=s.split()
    for j in s:
        adj_matrix[i].append(j=='1')
for row in adj_matrix:
    print(row)

d=float(input("\nEnter Damping Factor\n"))
print(d)
max_iterations=int(input("Enter the max number of iterations\n"))
print(max_iterations)
tol=float(input("Enter the tolerance threshold\n"))
print(tol)
page_rank=PageRank(adj_matrix,d,max_iterations,tol)
auth_weight,hub_weight=HITS(adj_matrix,d,max_iterations,tol)
print(page_rank)
print(auth_weight)
print(hub_weight)
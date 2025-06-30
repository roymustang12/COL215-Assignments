import time
start_time = time.time()
# gates=[]

# while(True):
#     try:
#         gate=[]
#         a,b,c=input().split()
#         b=int(b)
#         c=int(c)
#         gate.append(a)
#         gate.append(b)
#         gate.append(c)
#         gates.append(gate)
        
#     except: 
#         break
# # print(*gates)
# Define a function to read the gate dimensions from a file
def read_gate_details(filename):
    gates = []  # List to store details of all gates
    
    # Open the file for reading
    with open(filename, 'r') as file:
        for line in file:
            # Strip any leading/trailing whitespace and split the line into components
            parts = line.strip().split()
            
            if len(parts) == 3:
                name = parts[0]
                try:
                    # Convert width and height to integers
                    width = int(parts[1])
                    height = int(parts[2])
                    
                    # Append the details as a tuple to the list
                    gates.append((name, width, height))
                    
                except ValueError:
                    print(f"Invalid width or height value in line: {line.strip()}")
            else:
                print(f"Invalid line format: {line.strip()}")
                    
    return gates

# Define the path to your input file
input_file = 'input.txt'

# Read and print gate details
gates= read_gate_details(input_file)
# for idx, (name, width, height) in enumerate(gates):
#     print(f"Gate {idx + 1}: Name = {name}, Width = {width}, Height = {height}")
gates.sort(key=lambda x :x[1])
kk=gates.pop()
gates.insert(0,kk)
wi=50
general=[]
for __ in gates:
    general.append(__[1])
general.sort()
ii=general[-1]
general.pop()
general.insert(0,ii)
for i  in range(1,len(general)):
    general[i]=general[i]+general[i-1]
# print(*general)

class Node:
    def __init__(self, st, width, height):
        self.st = st
        self.width = width
        self.height = height
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, st, width, height):
        new_node = Node(st, width, height)
        if self.head is None:
            self.head = new_node
        else:
            last_node = self.head
            while last_node.next:
                last_node = last_node.next
            last_node.next = new_node

    def display(self):
        current_node = self.head
        hgt=0
        while current_node:
            if hgt<current_node.height:
                hgt=current_node.height
            # print(current_node.st,current_node.width,current_node.height)
            current_node = current_node.next
        return hgt
fl=wi
area=0
for _ in gates:
    area=area+(_[1]*_[2])
    
def sky(gates,wi):
    skyline=LinkedList()
    skyline.append(0,wi,0)
    for _ in gates:
        a=_[1]
        b=_[2]
        aa=skyline.head
        fin=skyline.head
        fin2=fin
        prev=fin
        ww=0
        ll=0
        maxh=1000000
        cc=aa
        while aa:
            ww=0
            if (wi-aa.st)<a:
                cc=aa
                aa=aa.next
                continue
            hh=aa.height
            ab=aa
            while ab:
                # bb=bb.next
                ww+=ab.width
                hh=max(hh,ab.height)
                if ww>=a:
                    # ll=ww
                    break
                ab=ab.next
            if hh<maxh:
                ll=ww
                maxh=hh
                fin=aa
                fin2=ab
                prev=cc
            cc=aa
            aa=aa.next
        # print(fin.st,fin.width)
        # print(fin2.st)
        # print(fin.st)
        # print(prev.st)
        if (fin.st+a==wi):
            if fin!=prev:
                aaa=Node(fin.st,a,maxh+b)
                # bbb=Node(aaa.st+aaa.width,ll-aaa.width,fin2.height)
                prev.next=aaa
                # aaa.next=bbb
                # bbb.next=fin2.next
                # skyline.display()
            
            else:
                aaa=Node(fin.st,a,maxh+b)
                # bbb=Node(aaa.st+aaa.width,ll-aaa.width,fin2.height)
                # aaa.next=bbb
                # bbb.next=fin2.next
                
                skyline.head=aaa
                # skyline.display()
        else:
            if fin!=prev:
                aaa=Node(fin.st,a,maxh+b)
                bbb=Node(aaa.st+aaa.width,ll-aaa.width,fin2.height)
                prev.next=aaa
                aaa.next=bbb
                bbb.next=fin2.next
                # skyline.display()
                
            else:
                aaa=Node(fin.st,a,maxh+b)
                bbb=Node(aaa.st+aaa.width,ll-aaa.width,fin2.height)
                aaa.next=bbb
                bbb.next=fin2.next
                
                skyline.head=aaa
                # skyline.display()
    return (skyline.display()*wi)
def skyf(gates,wi):
    ans=[]
    skyline=LinkedList()
    skyline.append(0,wi,0)
    for _ in gates:
        a=_[1]
        b=_[2]
        aa=skyline.head
        fin=skyline.head
        fin2=fin
        prev=fin
        ww=0
        ll=0
        maxh=1000000
        cc=aa
        while aa:
            ww=0
            if (wi-aa.st)<a:
                cc=aa
                aa=aa.next
                continue
            hh=aa.height
            ab=aa
            while ab:
                # bb=bb.next
                ww+=ab.width
                hh=max(hh,ab.height)
                if ww>=a:
                    # ll=ww
                    break
                ab=ab.next
            if hh<maxh:
                ll=ww
                maxh=hh
                fin=aa
                fin2=ab
                prev=cc
            cc=aa
            aa=aa.next
        # print(fin.st,fin.width)
        # print(fin2.st)
        # print(fin.st)
        # print(prev.st)
        if (fin.st+a==wi):
            if fin!=prev:
                jj=[]
                jj.append(_[0])
                jj.append(fin.st)
                jj.append(maxh)
                ans.append(jj)
                aaa=Node(fin.st,a,maxh+b)
                # bbb=Node(aaa.st+aaa.width,ll-aaa.width,fin2.height)
                prev.next=aaa
                # aaa.next=bbb
                # bbb.next=fin2.next
                # skyline.display()
            
            else:
                jj=[]
                jj.append(_[0])
                jj.append(fin.st)
                jj.append(maxh)
                ans.append(jj)
                aaa=Node(fin.st,a,maxh+b)
                # bbb=Node(aaa.st+aaa.width,ll-aaa.width,fin2.height)
                # aaa.next=bbb
                # bbb.next=fin2.next
                
                skyline.head=aaa
                # skyline.display()
        else:
            if fin!=prev:
                jj=[]
                jj.append(_[0])
                jj.append(fin.st)
                jj.append(maxh)
                ans.append(jj)
                aaa=Node(fin.st,a,maxh+b)
                bbb=Node(aaa.st+aaa.width,ll-aaa.width,fin2.height)
                prev.next=aaa
                aaa.next=bbb
                bbb.next=fin2.next
                # skyline.display()
                
            else:
                jj=[]
                jj.append(_[0])
                jj.append(fin.st)
                jj.append(maxh)
                ans.append(jj)
                aaa=Node(fin.st,a,maxh+b)
                bbb=Node(aaa.st+aaa.width,ll-aaa.width,fin2.height)
                aaa.next=bbb
                bbb.next=fin2.next
                
                skyline.head=aaa
                # skyline.display()
    return ans
# def skyf(gates,wi):
#     ans=[]
#     skyline=LinkedList()
#     skyline.append(0,wi,0)
    
#     for _ in gates:
#         a=_[1]
#         b=_[2]
#         aa=skyline.head
#         fin=skyline.head
#         fin2=fin
#         prev=fin
#         ww=0
#         ll=0
#         maxh=1000000
#         cc=aa
#         while aa:
#             ww=0
#             if (wi-aa.st)<a:
#                 cc=aa
#                 aa=aa.next
#                 continue
#             hh=aa.height
#             ab=aa
#             while ab:
#                 # bb=bb.next
#                 ww+=ab.width
#                 hh=max(hh,ab.height)
#                 if ww>=a:
#                     ll=ww
#                     break
#                 ab=ab.next
#             if hh<maxh:
#                 maxh=hh
#                 fin=aa
#                 fin2=ab
#                 prev=cc
#             cc=aa
#             aa=aa.next
#         # print(fin.st,fin.width)
#         # print(fin2.st)
#         # print(fin.st)
#         # print(prev.st)
#             # jj=[]
#             # jj.append(_[0])
#             # jj.append(fin.st)
#             # jj.append(maxh)
#             # ans.append(jj)
#         if (fin.st+a==wi):
#             if fin!=prev:
#                 jj=[]
#                 jj.append(_[0])
#                 jj.append(fin.st)
#                 jj.append(maxh)
#                 ans.append(jj)
#                 aaa=Node(fin.st,a,maxh+b)
#                 # bbb=Node(aaa.st+aaa.width,ll-aaa.width,fin2.height)
#                 prev.next=aaa
#                 # aaa.next=bbb
#                 # bbb.next=fin2.next
#                 # skyline.display()
            
#             else:
#                 jj=[]
#                 jj.append(_[0])
#                 jj.append(fin.st)
#                 jj.append(maxh)
#                 ans.append(jj)
#                 aaa=Node(fin.st,a,maxh+b)
#                 # bbb=Node(aaa.st+aaa.width,ll-aaa.width,fin2.height)
#                 # aaa.next=bbb
#                 # bbb.next=fin2.next
                
#                 skyline.head=aaa
#                 # skyline.display()
#         else:
#             if fin!=prev:
#                 jj=[]
#                 jj.append(_[0])
#                 jj.append(fin.st)
#                 jj.append(maxh)
#                 ans.append(jj)
#                 aaa=Node(fin.st,a,maxh+b)
#                 bbb=Node(aaa.st+aaa.width,ll-aaa.width,fin2.height)
#                 prev.next=aaa
#                 aaa.next=bbb
#                 bbb.next=fin2.next
#                 # skyline.display()
                
#             else:
#                 jj=[]
#                 jj.append(_[0])
#                 jj.append(fin.st)
#                 jj.append(maxh)
#                 ans.append(jj)
#                 aaa=Node(fin.st,a,maxh+b)
#                 bbb=Node(aaa.st+aaa.width,ll-aaa.width,fin2.height)
#                 aaa.next=bbb
#                 bbb.next=fin2.next
                
#                 skyline.head=aaa
#                 # skyline.display()
#     return ans
oo=sky(gates,general[0])
uu=general[0]

for u in general:
    # print(u)
    op=sky(gates,u)
    if op<oo:
        oo=op
        uu=u
print(uu,oo//uu)
ans=skyf(gates,uu)

print(*ans)
print(area)
print(time.time()-start_time)


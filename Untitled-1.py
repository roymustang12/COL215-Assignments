import time
start_time = time.time()
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
gates.sort(key=lambda x :-x[2])
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
# print(*gates)
def shelf(wi,gates):
    hh=gates[0]
    ht=hh[2]
    ll=0
    for _ in gates:
        ll=ll+_[1]
        if(ll>wi):
            ll=_[1]
            ht=ht+_[2]
    return wi*ht
area=0
for _ in gates:
    area=area+(_[1]*_[2])
print(area)
mini =ii
# print(mini)
# print(general[-1])
ff=shelf(ii,gates)
# print(shelf(2000,gates))
for _ in range(ii,general[-2]):
    
    aa=(shelf(_,gates))
    if aa<ff:
        mini=_
        ff=aa
        # print(_,aa)

print(shelf(mini,gates))
def shelfl(wi,gates):
    ans=[]
    hh=gates[0]
    
    ht=hh[2]
    mm=ht
    ll=0
    for _ in gates:
        ll=ll+_[1]
        if(ll>wi):
            ll=_[1]
            ht=ht+_[2]
            mm=_[2]
            jj=[]
            jj.append(_[0])
            jj.append(ll-_[1])
            jj.append(ht-mm)
            ans.append(jj)
        else:
            jj=[]
            jj.append(_[0])
            jj.append(ll-_[1])
            jj.append(ht-mm)
            ans.append(jj)
            
    return ans
ans=shelfl(mini,gates)
print(*ans)
print(time.time()-start_time)

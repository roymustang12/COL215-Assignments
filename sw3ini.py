
import random
import math
def read_input(file_path):
    """Read the circuit input from a file."""
    gates = {}
    wires = []
    wire_delay_per_unit = 0

    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('g'):
                parts = line.split()
                gate_name = parts[0]
                width = int(parts[1])
                height = int(parts[2])
                delay = int(parts[3])
                gates[gate_name] = {'width': width, 'height': height, 'delay': delay, 'pins': []}
            elif line.startswith('pins'):
                parts = line.split()
                gate_name = parts[1]
                pin_coords = [(int(parts[i]), int(parts[i + 1])) for i in range(2, len(parts), 2)]
                gates[gate_name]['pins'] = pin_coords
            elif line.startswith('wire_delay'):
                wire_delay_per_unit = int(line.split()[1])
            elif line.startswith('wire'):
                wires.append((line.split()[1], line.split()[2]))

    return gates, wires, wire_delay_per_unit

def find_primary_inputs_outputs(gates, wires):
    """Identify primary input and output pins."""
    connected_inputs = set(dest for _, dest in wires)
    connected_outputs = set(src for src, _ in wires)

    primary_inputs = []
    primary_outputs = []

    # Iterate over each gate and its pins
    for gate, info in gates.items():
        for pin_index, (x, y) in enumerate(info['pins'], start=1):  # Start pin index from 1
            pin = f"{gate}.p{pin_index}"

            # If the pin is on the left side (x == 0) and not a destination, it's a primary input
            if x == 0 and pin not in connected_inputs:
                primary_inputs.append(pin)

            # If the pin is on the right side (x == width) and not a source, it's a primary output
            # if x == info['width'] and pin not in connected_outputs:
            #     primary_outputs.append(pin)
    for gate, info in gates.items():
        for pin_index, (x, y) in enumerate(info['pins'], start=1):  # Start pin index from 1
            pin = f"{gate}.p{pin_index}"

            # If the pin is on the left side (x == 0) and not a destination, it's a primary input
            # if x == 0 and pin not in connected_inputs:
            #     primary_inputs.append(pin)

            # If the pin is on the right side (x == width) and not a source, it's a primary output
            if x == info['width'] and pin not in connected_outputs:
                primary_outputs.append(pin)

    # print("Primary Inputs:", primary_inputs)  # Debugging
    # print("Primary Outputs:", primary_outputs)  # Debugging

    return primary_inputs, primary_outputs
# def map_gate_to_inputs(gates,wires):
#     gate_to_input={}
#     connected_inputs = set(src for src, _ in wires)
#     for pin in connected_inputs:
def map_gate_to_output_pins(gates):
    """Build a map from each gate to its list of output pins (pins on the right side)."""
    gate_to_output_pins = {}

    for gate_name, gate_info in gates.items():
        width = gate_info['width']
        output_pins = []
        
        # Loop through the pins of the gate
        for pin_index, (x, y) in enumerate(gate_info['pins'], start=1):
            # If the pin is on the right side (x == width), it's considered an output pin
            if x == width:
                output_pin = f"{gate_name}.p{pin_index}"
                output_pins.append(output_pin)
        
        # Add the gate and its output pins to the map
        gate_to_output_pins[gate_name] = output_pins

    # print("Gate to Output Pins Map:", gate_to_output_pins)  # Debugging output
    return gate_to_output_pins



# def find_all_paths(primary_inputs, primary_outputs, wires):
#     """Find all paths from primary inputs to primary outputs."""
#     all_paths = []

#     def dfs(current_pin, path):
#         """DFS to explore all paths."""
#         path.append(current_pin)

#         if current_pin in primary_outputs:
#             all_paths.append(list(path))
#         else:
#             for src, dest in wires:
#                 if src == current_pin and dest not in path:
#                     dfs(dest, path)

#         path.pop()  # Backtrack

#     for input_pin in primary_inputs:
#         dfs(input_pin, [])

#     return all_paths
def build_pin_to_dest_map(wires):
    """Build a map of each pin to the list of pins it connects to."""
    pin_to_dest = {}

    for src, dest in wires:
        if src not in pin_to_dest:
            pin_to_dest[src] = []  # Initialize the list if the pin is not in the map
        pin_to_dest[src].append(dest)

    # print("Pin-to-Destination Map:", pin_to_dest)  # Debugging
    return pin_to_dest

def build_pin_to_gate_map(gates):
    """Build a map of each pin to its corresponding gate."""
    pin_to_gate = {}

    for gate_name, gate_info in gates.items():
        for pin_index, _ in enumerate(gate_info['pins'], start=1):
            pin_name = f"{gate_name}.p{pin_index}"
            pin_to_gate[pin_name] = gate_name  # Map pin to gate

    # print("Pin to Gate Map:", pin_to_gate)  # Debugging output
    return pin_to_gate
def deepcopy(ll):
    l=[]
    for _ in ll:
        lll=[]
        for _i in _:
            lll.append(_i)
        l.append(lll)
    return l
def find_all_paths(primary_inputs, primary_outputs,pin_to_gate,pin_to_dest_map,gate_to_output_pins,pin_to_position_map):
    all_paths=[]
    dp={}
    def dfs(current_pin):
        if pin_to_position_map[current_pin][0]==0:
            if current_pin in dp:
                if not dp[current_pin]==None:
                    # print(current_pin,dp[current_pin])
                    found_path=(dp[current_pin])
                    return found_path
            # print(current_pin)
            ll=[]
            destination=gate_to_output_pins[pin_to_gate[current_pin]]
            for pin in destination:
                old=dfs(pin)
                for _ in old:
                    # _.append(pin)
                    _.append(current_pin)
                    ll.append(_)
            dp[current_pin]=deepcopy(ll)
            return ll

        else:
            if current_pin in dp:
                if not dp[current_pin]==None:
                    # print(current_pin,dp[current_pin])
                    found_path=(dp[current_pin])
                    return found_path
            ll=[]
            # print(current_pin)
            if current_pin in primary_outputs:
                return [[current_pin]]
            destination=pin_to_dest_map[current_pin]
            for pin in destination:
                old=dfs(pin)
                for _ in old:
                    # _.append(pin)
                    _.append(current_pin)
                    ll.append(_)
            dp[current_pin]=deepcopy(ll)
            return ll
    for input_pin in primary_inputs:
        all_paths.append(dfs(input_pin))
    # print("all paths:",all_paths)

    return all_paths


# def find_all_paths(primary_inputs, primary_outputs,pin_to_gate,pin_to_dest_map,gate_to_output_pins):
#     """Find all paths from primary inputs to primary outputs using DFS and pin-to-destination map."""
#     all_paths = []  # Store all the paths
#     dp={}

#     def dfs(current_pin):
#         """Recursive DFS to explore all paths from current_pin."""
#         ll=[]
#         # path.append(current_pin)  # Add current pin to the path

#         # If we reach a primary output, store the path
#         for pin in gate_to_output_pins[pin_to_gate[current_pin]]:
#             print(current_pin,pin)

#             if pin in primary_outputs:
#                 # if pin in dp:
#                 #     if not dp[pin]==None:
#                 #         print(pin,dp[pin])
#                 #         found_path=(dp[pin])
#                 #         return found_path
#                 dp[pin]=[[pin,current_pin]]
#                 return [[pin,current_pin]]  # Make a copy of the path
#             else:
#                 # If the current pin has any connections, follow them
#                 l=[]
#                 # if pin in dp:
#                 #     if not dp[pin]==None:
#                 #         print(pin,dp[pin])
#                 #         found_path=(dp[pin])
#                 #         return found_path
#                 if pin in pin_to_dest_map:
#                     for next_pin in pin_to_dest_map[pin]:
#                         # if next_pin not in path:  # Avoid cycles
#                         old=dfs(next_pin)
#                         for _ in old:
#                             _.append(pin)
#                             _.append(current_pin)
#                             l.append(_)
#                 listof_path_passing=[]
#                 for _ in l:
#                     ll=[]
#                     for _i in _:
#                         ll.append(_i)
#                     listof_path_passing.append(ll)
#                     # print(" vv",_)
#                 dp[pin]=listof_path_passing
                
#                 return l
        


#             # path.pop()  # Backtrack

#     # Start DFS from each primary input
#     for input_pin in primary_inputs:
#         all_paths.append(dfs(input_pin))
#     print("all paths:",all_paths)

#     return all_paths

def path_to_number_map(all_paths):
    no_to_path={}
    i=1
    for _ in all_paths:
        for _i in _ :
            no_to_path[i]=_i
            print(i,_i)
            i=i+1
    return no_to_path

def gate_to_path_no(no_to_path,pin_to_gate):
    gate_to_path={}
    for oo in no_to_path.keys():
        l=no_to_path[oo]
        for ooo in l:
            gate=pin_to_gate[ooo]
            if gate not in gate_to_path:
                gate_to_path[gate]=set()
            gate_to_path[gate].add(oo)
    # print(gate_to_path)
    return gate_to_path
def shift_positions_to_origin(positions,x):
    # Find the minimum x and y coordinates
    min_x = min(pos[0] for pos in positions.values())
    min_y = min(pos[1] for pos in positions.values())
    
    # Shift all gate positions
    shifted_positions = {}
    for gate, pos in positions.items():
        shifted_positions[gate] = (pos[0] - min_x+x, pos[1] - min_y)
    
    return shifted_positions
def bounding_box(positions, gates):
    min_x = min(pos[0] for pos in positions.values())
    min_y = min(pos[1] for pos in positions.values())
    max_x = max(pos[0] + gates[gate]['width'] for gate, pos in positions.items())
    max_y = max(pos[1] + gates[gate]['height'] for gate, pos in positions.items())
    return max_x - min_x, max_y - min_y
def initialize_positions_new(gates):
    n = len(gates)
    sqrt_n = math.ceil(math.sqrt(n))
    gate_name_lists=[]
    gate_no=[]
    gate_name_list=list(gates.keys())
    for _ in range(len(gate_name_list)):
        if gate_name_list[_] in gate_to_path:
            gate_name_lists.append(gate_name_list[_])
        else:
            gate_no.append(gate_name_list[_])
    gate_name_lists.sort(key= lambda x:len(gate_to_path[x]))
    gate_name_list=gate_no+gate_name_lists
    max_height=0
    max_width=0
    for _ in range (len(gate_name_list)):
        max_height=max(max_height,gates[gate_name_list[_]]["height"]+4)
        max_width=max(max_width,gates[gate_name_list[_]]["width"]+4)
        # print(len(gate_to_wire[gate_name_list[_]]),gate_name_list[_])
    gate_name_list.reverse()
    
    positions = {}
    distance1=0
    distance2=max_height
    if n<100:
        a=20
    else:
        a=0
    gate_index = 0
    for i in range(sqrt_n):
        for j in range(sqrt_n):
            if gate_index < n:
                gate_name = gate_name_list[gate_index]
                x = distance1
                
                y = i*distance2
                positions[gate_name] = (x, y)
                gate_index += 1
                distance1+=gates[gate_name]["width"]+a
                if n<100:
                  distance1+=max_width+a
        distance1=0
        if i !=0:
            for j in range(sqrt_n):
                if gate_index < n:
                    gate_name = gate_name_list[gate_index]
                    x = distance1
                    
                    y = (-1)*i*distance2
                    positions[gate_name] = (x, y)
                    gate_index += 1
                    distance1+=gates[gate_name]["width"]+a
                    if n<300:
                        distance1+=max_width+a
                    # distance1+=max_width+a
            distance1=0
    
    return positions

def initialize_positions(gates):
    n = len(gates)
    sqrt_n = math.ceil(math.sqrt(n))
    positions = {}
    # distance1=100
    # distance2=100
    gate_name_list=list(gates.keys())
    max_height=0
    max_width=0
    for _ in range (len(gate_name_list)):
        max_height=max(max_height,gates[gate_name_list[_]]["height"])
        max_width=max(max_width,gates[gate_name_list[_]]["width"])
    gate_index = 0
    distance1=10*max_width
    distance2=10*max_height
    xx=0
    yy=0
    for i in range(sqrt_n):
        xx=0
        for j in range(sqrt_n):
            if gate_index < n:
                gate_name = list(gates.keys())[gate_index]
                x = xx
                y = yy
                positions[gate_name] = (x, y)
                gate_index += 1
                xx+=distance1
        yy+=distance2
                
    
    return positions

def overlap(gate1, pos1, gate2, pos2, gates):
    x1_min, y1_min = pos1
    x1_max, y1_max = x1_min + gates[gate1]['width'], y1_min + gates[gate1]['height']
    
    x2_min, y2_min = pos2
    x2_max, y2_max = x2_min + gates[gate2]['width'], y2_min + gates[gate2]['height']
    
    # Check if there is no overlap
    if x1_max <= x2_min or x1_min >= x2_max or y1_max <= y2_min or y1_min >= y2_max:
        return False
    return True

# Function to check if a new gate position overlaps with any existing gate
def is_overlapping(new_gate, new_position, positions, gates):
    for existing_gate, existing_position in positions.items():
        if new_gate != existing_gate and overlap(new_gate, new_position, existing_gate, existing_position, gates):
            return True
    return False

def perturb_position(position, gate, gates,max_width,max_height):
    delta_x = random.randint(-max_width, max_width)
    delta_y = random.randint(-max_height, max_height)
    
    new_x = position[0] + delta_x
    new_y = position[1] + delta_y
    return (new_x, new_y)
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
def create_pin_to_position_map(gates):
    """Create a map from each pin to its position relative to its gate."""
    pin_to_position = {}

    # Iterate over each gate and its pins
    for gate_name, gate_info in gates.items():
        pins = gate_info['pins']

        # Iterate over each pin with an index starting from 1 (as required)
        for pin_index, (x, y) in enumerate(pins, start=1):
            pin_name = f"{gate_name}.p{pin_index}"  # Create pin name (e.g., "g1.p1")
            pin_to_position[pin_name] = (x, y)  # Store the relative position

    # print("Pin-to-Position Map:", pin_to_position)  # Debugging
    return pin_to_position
def path_delay(l,pin_to_gate,positions,gates,pin_to_position_map,wire_delay_per_unit):
    n=len(l)
    i=0
    delay=0
    while i<n-1:
        if pin_to_gate[l[i]]==pin_to_gate[l[i+1]]:
            delay = delay+gates[pin_to_gate[l[i]]]['delay']
            i=i+1
        else :
            pin_1=l[i]
            gate_1=pin_to_gate[l[i]]
            pin_2=l[i+1]
            gate_2=pin_to_gate[l[i+1]]
            pin1_coord = (positions[gate_1][0] + pin_to_position_map[pin_1][0], 
                      positions[gate_1][1] + pin_to_position_map[pin_1][1])
            pin2_coord=(positions[gate_2][0] + pin_to_position_map[pin_2][0], 
                      positions[gate_2][1] + pin_to_position_map[pin_2][1])
            length=manhattan_distance(pin1_coord,pin2_coord)
            delay=delay+length*wire_delay_per_unit
            i=i+1
    # print(delay)
    return delay
def map_path_to_delay(no_to_path,positions,gates,pin_to_position_map,wire_delay_per_unit,pin_to_gate):
    path_to_delay={}
    for _ in no_to_path.keys():
        path_to_delay[_]=path_delay(no_to_path[_],pin_to_gate,positions,gates,pin_to_position_map,wire_delay_per_unit)
    # print(path_to_delay)
    return path_to_delay
def cost(path_to_delay):
    max_path_delay=0
    max_path_no=0
    for _ in path_to_delay.keys():
        if path_to_delay[_]>max_path_delay:
            max_path_delay=path_to_delay[_]
            max_path_no=_
    return max_path_delay,max_path_no

def simulated_anneling(gates, wires,wire_delay_per_unit, initial_temp, final_temp, cooling_rate,primary_inputs, primary_outputs,pin_to_dest_map,gate_to_output_pins,no_to_path):
    gate_name_list=list(gates.keys())
    max_height=0
    max_width=0
    for _ in range (len(gate_name_list)):
        max_height=max(max_height,gates[gate_name_list[_]]["height"])
        max_width=max(max_width,gates[gate_name_list[_]]["width"])
    gate_list=list(gates.keys())
    current_temp=initial_temp
    best_position = positions.copy()
    itr=0
    while itr<10000:
        itr=itr+1
        max_path_delay,max_path_no=cost(path_to_delay)
        path=no_to_path[max_path_no]
        # pin=random.choice(path)
        # # # print(pin,"vishal")
        # gate=pin_to_gate[pin]
        gate=random.choice(gate_list)
        old_pos=positions[gate]
        new_pos=perturb_position(old_pos,gate,gates,max_width,max_height)
        positions[gate]=new_pos
        if not is_overlapping(gate, new_pos, positions, gates):
            lt={}
            list_of_gate_path=gate_to_path[gate]
            for _ in list_of_gate_path:
                lt[_]=path_to_delay[_]
                new_delay=path_delay(no_to_path[_],pin_to_gate,positions,gates,pin_to_position_map,wire_delay_per_unit)
                path_to_delay[_]=new_delay
            new_max_path_delay,new_max_path_no=cost(path_to_delay)
            delta=new_max_path_delay-max_path_delay
            # print(delta,new_max_path_delay,max_path_delay,max_path_no,new_max_path_no)
            
            if  delta <=0 or random.uniform(0, 1) < math.exp(min(max(-10,(-delta / current_temp)),10)):
                if delta<=0 :
                    best_position=positions.copy()
                

            else:
                for _ in list_of_gate_path:
                    path_to_delay[_]=lt[_]
                positions[gate]=old_pos

        else:
            positions[gate]=old_pos
        current_temp *= cooling_rate
    x,path_no=cost(path_to_delay)
    return best_position,no_to_path[path_no]

            

def save_opt(positions,gates,critical_path,answer,file_name):
    with open(file_name,'w') as f :
        x,y = bounding_box(positions,gates)
        f.write(f'bounding_box {x} {y}\n')
        f.write(f'critical_path {' '.join(critical_path[::-1])}\n')
        f.write(f'critical_path_delay {answer}\n')
        for i,(x,y) in positions.items() :
            f.write(f'{i} {x} {y}\n')

    



# def save_output(file_path, all_paths):
#     """Save the paths to an output file."""
#     with open(file_path, 'w') as f:
#         f.write("All Paths:\n")
#         for path in all_paths:
#             f.write(" -> ".join(path) + "\n")

# def main():
#     # Read input from the file
    

file_path = "input.txt"  # Replace with your input file path
gates, wires, wire_delay_per_unit = read_input(file_path)
# print(gates)

# Find primary input and output pins
primary_inputs, primary_outputs = find_primary_inputs_outputs(gates, wires)
pin_to_gate=build_pin_to_gate_map(gates)
pin_to_dest_map=build_pin_to_dest_map(wires)
gate_to_output_pins=map_gate_to_output_pins(gates)


# Find all paths from primary inputs to primary outputs
pin_to_position_map=create_pin_to_position_map(gates)
# all_paths = find_all_paths(primary_inputs, primary_outputs,pin_to_gate,pin_to_dest_map,gate_to_output_pins)
all_paths=find_all_paths(primary_inputs, primary_outputs,pin_to_gate,pin_to_dest_map,gate_to_output_pins,pin_to_position_map)
no_to_path=path_to_number_map(all_paths)

gate_to_path=gate_to_path_no(no_to_path,pin_to_gate)

positions=initialize_positions(gates)
path_to_delay=map_path_to_delay(no_to_path,positions,gates,pin_to_position_map,wire_delay_per_unit,pin_to_gate)
initial_temp, final_temp, cooling_rate=1000,0.01,0.999
# path_delay(no_to_path[1],pin_to_gate,positions,gates,pin_to_position_map,wire_delay_per_unit)
best_position,criticalpath=simulated_anneling(gates, wires,wire_delay_per_unit, initial_temp, final_temp, cooling_rate,primary_inputs, primary_outputs,pin_to_dest_map,gate_to_output_pins,no_to_path)
# x,path_no=cost(path_to_delay)
# Save the paths to an output file
# save_output("output.txt", all_paths)
best_position=shift_positions_to_origin(best_position,0)
ans=path_delay(criticalpath,pin_to_gate,best_position,gates,pin_to_position_map,wire_delay_per_unit)
print(best_position)

print(ans)
print(path_to_delay)
save_opt(best_position,gates,criticalpath,ans,'output.txt')
# Print the results
# print("Primary Inputs:", primary_inputs)
# print("Primary Outputs:", primary_outputs)
# print("All Paths have been saved to output.txt")

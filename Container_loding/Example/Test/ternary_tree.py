from constants import RotationType, Axis
from auxiliary_methods import intersect, set_to_decimal

DEFAULT_NUMBER_OF_DECIMALS = 3
START_POSITION = [0, 0, 0]
UNFITTED_ITEMS = []
USED_VOLUME = 0
FILE = open("result.txt", "w")
FILE_html = open("result_html.txt", "w")
# X Y Z W D H
FILE.write("30 20 40\n")
FILE_html.write("30 20 40\n")

# Python program to for tree traversals 
  
# A class that represents an individual node in a 
# Binary Tree 
class Node: 
    def __init__(self, width, height, depth) : 
        # Leaf
        self.left = None
        self.center = None
        self.right = None

        # Node data
        self.position = START_POSITION
        self.width = width
        self.height = height
        self.depth = depth

        # Box data
        self.box = None

    def format_numbers(self, number_of_decimals):
        self.width = set_to_decimal(self.width, number_of_decimals)
        self.height = set_to_decimal(self.height, number_of_decimals)
        self.depth = set_to_decimal(self.depth, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def get_volume(self):
        return self.width * self.height * self.depth

    def put_item(self, box):
        fit = False
        # valid_box_position = box.position
        # box.position = self.position

        # Loop ตามการหมุนของกล่องเพื่อหาด้านที่ fit กับพื้นที่
        # เริ่มจากกล่องในมุมแบบเดิมก่อน แล้วถ้าใสไม่ได้ค่อยเปลี่ยนแนวกล่อง
        for i in range(0, len(RotationType.ALL)):
            box.rotation_type = i
            dimension = box.get_dimension()

            print("W: {}, H: {}, D: {}".format(dimension[0],dimension[1],dimension[2]))

            box_w = dimension[0]
            box_h = dimension[1]
            box_d = dimension[2]

            # ถ้าขนาดของกล่องเทียบกับพื้นที่แล้วใส่ไม่ได้จะข้ามไปเพื่อหมุนกล่อง
            if (
                self.width < box_w or
                self.height < box_h or
                self.depth < box_d
            ):
                continue
            # กล่องใส่ในพื้นที่ได้
            fit = True

            # เก็บกล่องไปที่ node ปัจจุบัน
            if fit:
                self.box = box
                global USED_VOLUME
                USED_VOLUME += box.get_volume()
                # ตรวจสอบพื้นที่ว่างด้านบนกล่อง (ด้าน height)
                if(self.height - box_h > 0):
                    print("self.left => self.height - box_h: {}".format(self.height - box_h))
                    # เพิ่ม node สำหรับพื้นทที่ว่างด้านบนกล่อง
                    new_width = box_w #width
                    new_height = self.height - box_h
                    new_depth = box_d #depth
                    print("new_width: {}".format(new_width))
                    print("new_height: {}".format(new_height))
                    print("new_depth: {}".format(new_depth))
                    self.left = Node(new_width,new_height,new_depth)
                    # (width)
                    x = self.position[0]
                    y = self.position[1] + box_h
                    z = self.position[2]
                    self.left.position = [x,y,z]                    
                    print("get_volume(): {}".format(self.left.get_volume()))
                
                # ตรวจสอบพื้นที่ว่างด้านกว้าง (ด้าน width)
                if(self.width - box_w > 0):
                    print("self.center => self.width- box_w: {}".format(self.width- box_w))
                    # เพิ่ม node สำหรับพื้นทที่ว่างด้านกว้าง
                    new_width = self.width - box_w
                    new_height = self.height
                    new_depth = box_d #depth
                    print("new_width: {}".format(new_width))
                    print("new_height: {}".format(new_height))
                    print("new_depth: {}".format(new_depth))
                    self.center = Node(new_width,new_height,new_depth)
                    x = self.position[0] + box_w
                    y = self.position[1]
                    z = self.position[2]
                    self.center.position = [x,y,z]  
                    print("get_volume(): {}".format(self.center.get_volume()))
                
                # ตรวจสอบพื้นที่ว่างด้านยาว (ด้าน depth)
                if(self.depth - box_d > 0):
                    print("self.right => self.depth - box_d: {}".format(self.depth - box_d))
                    # เพิ่ม node สำหรับพื้นทที่ว่างด้านยาว
                    new_width = self.width
                    new_height = self.height
                    new_depth = self.depth - box_d
                    print("new_width: {}".format(new_width))
                    print("new_height: {}".format(new_height))
                    print("new_depth: {}".format(new_depth))
                    self.right = Node(new_width,new_height,new_depth)
                    x = self.position[0]
                    y = self.position[1]
                    z = self.position[2] + box_d
                    self.right.position = [x,y,z] 
                    print("get_volume(): {}".format(self.right.get_volume()))

            # if not fit:
            #     box.position = valid_box_position
            print(self.get_box_dimension_and_position())
            FILE.write("0 {}\n".format(self.get_box_dimension_and_position()))
            FILE_html.write("{}\n".format(self.get_box_dimension()))
            return fit

        # if not fit:
        #     box.position = valid_box_position

        return fit

    def get_box_dimension_and_position(self):
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        return "{} {} {} {}".format(self.box.get_data(),int(x),int(y),int(z))

    def get_box_dimension(self):
        dim1, dim2, dim3 = self.box.get_data_2()
        x1 = self.position[0] # width
        y1 = self.position[2] # depth
        z1 = self.position[1] # height

        x2 = self.position[0] + dim1
        y2 = self.position[2] + dim3
        z2 = self.position[1] + dim2
        temp = "data.push(new Box("
        temp += "[{},{},{},{},{},{},{},{}],\n".format(x1,x1,x2,x2,x1,x1,x2,x2)
        temp += "[{},{},{},{},{},{},{},{}],\n".format(y1,y2,y1,y2,y1,y2,y1,y2)
        temp += "[{},{},{},{},{},{},{},{}],\n".format(z1,z1,z1,z1,z2,z2,z2,z2)
        temp += ").data)\n"

        return temp

class Box:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.rotation_type = 0
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS
    
    def format_numbers(self, number_of_decimals):
        self.width = set_to_decimal(self.width, number_of_decimals)
        self.height = set_to_decimal(self.height, number_of_decimals)
        self.depth = set_to_decimal(self.depth, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def get_data(self):
        dim = self.get_dimension()
        return "{} {} {}".format(int(dim[0]),int(dim[1]),int(dim[2]))
    
    def get_data_2(self):
        dim = self.get_dimension()
        return int(dim[0]),int(dim[1]),int(dim[2])


    def get_volume(self):
        return set_to_decimal(
            self.width * self.height * self.depth, self.number_of_decimals
        )

    def get_dimension(self):
        if self.rotation_type == RotationType.RT_WHD:
            dimension = [self.width, self.height, self.depth]
        elif self.rotation_type == RotationType.RT_HWD:
            dimension = [self.height, self.width, self.depth]
        elif self.rotation_type == RotationType.RT_HDW:
            dimension = [self.height, self.depth, self.width]
        elif self.rotation_type == RotationType.RT_DHW:
            dimension = [self.depth, self.height, self.width]
        elif self.rotation_type == RotationType.RT_DWH:
            dimension = [self.depth, self.width, self.height]
        elif self.rotation_type == RotationType.RT_WDH:
            dimension = [self.width, self.depth, self.height]
        else:
            dimension = []

        return dimension
  
class Packer:
    def __init__(self):
        self.root_nodes = []
        self.boxes = []
        self.total_boxes = 0

    def add_root_node(self, node):
        return self.root_nodes.append(node)
    
    def add_box(self, box):
        self.total_boxes = len(self.boxes) + 1
        return self.boxes.append(box)

    def pack_to_node(self, node, box):
        fitted = True
        # ใส่กล่องให้ Node
        if not node.box:            
            response = node.put_item(box)
            # print("response: {}".format(response))
            global UNFITTED_ITEMS
            if not response:
                # UNFITTED_ITEMS.append(box)
                return not fitted
            else:
                return fitted
        # เปลี่ยน Node เพื่อหาที่ใส่กล่อง
        if node.left:
            print("left")
            if self.pack_to_node(node.left, box):
                return fitted
        
        if node.center:
            print("center")
            if self.pack_to_node(node.center, box):
                return fitted
        
        if node.right:
            print("right")
            if self.pack_to_node(node.right, box):
                return fitted
        return not fitted


    def pack(self, bigger_first=False,number_of_decimals=DEFAULT_NUMBER_OF_DECIMALS):
        for node in self.root_nodes:
            node.format_numbers(number_of_decimals)

        for box in self.boxes:
            box.format_numbers(number_of_decimals)

        self.root_nodes.sort(
            key=lambda node: node.get_volume(), reverse=bigger_first
        )
        self.boxes.sort(
            key=lambda box: box.get_volume(), reverse=bigger_first
        )
        
        global UNFITTED_ITEMS
        for node in self.root_nodes:
            for box in self.boxes:
                fited = self.pack_to_node(node, box)
                if(not fited):
                    print("Not fited: {}\n".format(fited))
                    UNFITTED_ITEMS.append(box)
                    print(len(UNFITTED_ITEMS))

    # A function to do preorder tree traversal 
def printPreorder(root,file): 
    print("root: {}".format(root))
    if root: 

        # First print the data of node 
        # print("{} {}".format(root.box.get_data(),root.position))
        print("Box : {}".format(root.get_box_dimension_and_position()))
        file.write("0 {}\n".format(root.get_box_dimension_and_position()))
        # print("position:{} \n".format(root.position))

        printPreorder(root.left,file) 
        printPreorder(root.center,file) 
        printPreorder(root.right,file) 

packer = Packer()

packer.add_root_node(Node(30, 20, 40))

packer.add_box(Box(10, 13, 5))
packer.add_box(Box(20, 13, 5))
packer.add_box(Box(10, 13, 5))
packer.add_box(Box(10, 13, 5))
packer.add_box(Box(10, 13, 5))

packer.add_box(Box(10, 13, 5))
packer.add_box(Box(10, 13, 5))
packer.add_box(Box(5, 7, 8))
packer.add_box(Box(7, 8, 5))
packer.add_box(Box(3, 1, 5))

packer.add_box(Box(2, 1, 2))
packer.add_box(Box(2, 1, 2))
packer.add_box(Box(15, 5, 6))
packer.add_box(Box(4, 8, 2))
packer.add_box(Box(20, 20, 20))

packer.add_box(Box(2, 1, 2))
packer.add_box(Box(2, 1, 2))
packer.add_box(Box(15, 5, 6))
packer.add_box(Box(4, 8, 2))
# packer.add_box(Box(20, 20, 20))

packer.add_box(Box(2, 1, 2))
packer.add_box(Box(2, 1, 2))
packer.add_box(Box(2, 1, 2))
packer.add_box(Box(3, 1, 5))
packer.add_box(Box(3, 1, 5))

packer.add_box(Box(5, 7, 8))
packer.add_box(Box(7, 8, 5))
packer.add_box(Box(3, 1, 5))
packer.add_box(Box(2, 1, 2))
packer.add_box(Box(2, 1, 2))

packer.add_box(Box(2, 1, 2))
packer.add_box(Box(2, 1, 2))
packer.add_box(Box(2, 1, 2))
packer.add_box(Box(3, 1, 5))
packer.add_box(Box(3, 1, 5))

packer.add_box(Box(5, 7, 8))
packer.add_box(Box(7, 8, 5))
packer.add_box(Box(3, 1, 5))
packer.add_box(Box(2, 1, 2))
packer.add_box(Box(2, 1, 2))

packer.add_box(Box(5, 7, 8))
packer.add_box(Box(7, 8, 5))
packer.add_box(Box(3, 1, 5))
packer.add_box(Box(2, 1, 2))
packer.add_box(Box(2, 1, 2))

packer.add_box(Box(2, 1, 2))
packer.add_box(Box(2, 1, 2))
packer.add_box(Box(2, 1, 2))
packer.add_box(Box(3, 1, 5))
packer.add_box(Box(3, 1, 5))

packer.add_box(Box(5, 7, 8))
packer.add_box(Box(7, 8, 5))
packer.add_box(Box(3, 1, 5))
packer.add_box(Box(2, 1, 2))
packer.add_box(Box(2, 1, 2))


packer.pack(bigger_first=True)

# printPreorder(packer.root_nodes[0],f)
FILE.close()
FILE_html.close()
print("used: {}".format(USED_VOLUME))
print("UNFITTED_ITEMS: {}".format(len(UNFITTED_ITEMS))) 
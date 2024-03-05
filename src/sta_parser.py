'''
for bench mark

references: 
https://www.geeksforgeeks.org/command-line-arguments-in-python/
'''
class Node:
    def __init__(self):
        self.name = ""
        self.outname = ""
        self.Cload = 0.0
        self.inputs = [] #list of handles to the fanin nodes of this node
        self.outputs =[] #list of handles to the fanout nodes of this node
        self.Tau_in = [] # array/list of input slews (for all inputs to the gate), to be used for STA
        self.inp_arrival = [] # array/list of input arrival times for input transitions (ignore rise or fall)
        self.outp_arrival = [] # array/list of output arrival times,outp_arrival = inp_arrival + cell_delay
        self.max_out_arrival = 0.0 # arrival time at the output of thisgate using max on (inp_arrival +cell_delay)
        self.Tau_out = 0.0 # Resulting output slew
        self.faninstr = ''
        self.fanoutstr = ''

    def fanin(self, x, outname_node):                   #To add fanin string for the output and adding fanin nodes to the inputs array
        self.inputs.append(x)
        if self.faninstr[len(self.faninstr)-1] == ':':
            self.faninstr = self.faninstr + ' ' + outname_node +'-' + x
        else:
            self.faninstr = self.faninstr + ', ' + outname_node +'-' + x 
    
    def outname_node(self):
        return self.outname

    def fanout(self, x, outname_node):              #To add fanout string for the output and adding fanout nodes to the outputs array
        self.outputs.append(x)
        if self.fanoutstr[len(self.fanoutstr)-1] == ':':
            self.fanoutstr = self.fanoutstr + ' ' + outname_node + '-' + x
        else:
            self.fanoutstr = self.fanoutstr + ', ' + outname_node + '-' + x

    def naming(self, x, y):                 #Initalizing the name,gate_name, fanin string and fanout string 
        self.name = x
        self.outname = y
        self.faninstr = y + '-' + x + ':'
        self.fanoutstr = y + '-' + x + ':'

    def print_name(self):                   #function for checking the nodes data
        print(self.name,' ',self.outname)
        print('fanin')
        print(*self.inputs)
        print('fanout')
        print(*self.outputs)
        
        print(self.faninstr)
        print(self.fanoutstr)
        print("\n")
        #print(type(self.name))

    def name_check(self, x):                #function to check the name with a given string x
        return self.name == x
    
    def is_output(self):                #function to check if the node is output. This is done by checking the output and verifying if it has itself as the output
        if len(self.inputs)==0:
            return False
        return self.inputs[0]==self.name

    def fanout_print(self,str,file):        #function to print the fanout string
        if self.fanoutstr[0:6] == 'OUTPUT':
            a= str+self.fanoutstr[6:len(self.fanoutstr)]
            file.write(f"{a}\n")
        else:
            file.write(self.fanoutstr + "\n")

    def fanin_print(self,str,file):         #function to print the fanin string
        if self.faninstr[0:6] == 'OUTPUT':
            a= str+self.faninstr[6:len(self.faninstr)]
            file.write(f"{a}\n")
        else:
            file.write(self.faninstr + "\n")


class LUT:
    def __init__(self):
        self.Allgate_name = '' #all cells defined in the LUT
        self.All_delays =[] #2D numpy array delay LUTs for each cell
        self.All_slews = []#2D numpy array to store output slew LUTs foreach cell
        self.Cload_vals = [] #1D numpy array corresponds to the 2nd index in the LUT
        self.Tau_in_vals = [] #1D numpy array corresponds to the 1st index in the LUT
        
        #def assign_arrays(self, NLDM_file):
            # define the arrays to be used during STA call later
            # also helps to simply assign the arrays so that a call to thisfunction will fetch the arrays,
            # and you can easily print out the details of this NLDM
            # ...
    def assign_data(self,x):                            # function to load data of a lut which is compacted into a single string
        self.Allgate_name = re.search('[0-9a-zA-Z_]+\)',x).group(0)     #getting the name of the gate with trailing )
        self.Allgate_name = self.Allgate_name[0:len(self.Allgate_name)-1]   #removing the trailing )
        cell_Delay_string = re.search('cell_delay\([\da-zA-Z_){(".,;]+\}',x).group(0)   #extracting the cell delay block    
        output_slew_string = re.search('output_slew\([\da-zA-Z_){(".,;]+\}',x).group(0) #extracting the output slew block
        index_1_list = re.search('[0-9,.][0-9,.]+',re.search('index_1 *\( *"[\d,.]+"\)',cell_Delay_string).group(0)).group(0).split(sep=',')    #getting a string list of index1 from the cell delay string
        index_2_list = re.search('[0-9,.][0-9,.]+',re.search('index_2 *\( *"[\d,.]+"\)',cell_Delay_string).group(0)).group(0).split(sep=',')    #getting a string list of index2 from the cell delay string
        self.Tau_in_vals = index_1_list #assigning the values of index1
        self.Cload_vals = index_2_list  #assigning the values of index2
        cell_delay_values = re.search('["0-9.,]+',re.search('values[("0-9.,)]+',cell_Delay_string).group(0)).group(0).replace('","','";"').split(sep=';')   #getting a list of string which contains row of values of cell delay
        output_slew_values = re.search('["0-9.,]+',re.search('values[("0-9.,)]+',output_slew_string).group(0)).group(0).replace('","','";"').split(sep=';') #getting a list of string which contains row of values of output_slew
        cell_delay_values_2dlist = []
        output_slew_values_2dlist = []
        for x in cell_delay_values:     #splitting the string into a list of values in a row for cell delay values
            a=x.replace('"','').split(sep=',')
            cell_delay_values_2dlist.append(a)
        for x in output_slew_values:    #splitting the string into a list of values in a row for slew values
            a=x.replace('"','').split(sep=',')
            output_slew_values_2dlist.append(a)
        self.All_delays = cell_delay_values_2dlist
        self.All_slews = output_slew_values_2dlist

    def display(self):      #display the values for self check
        print(self.Allgate_name)
        print(self.All_delays) #2D numpy array delay LUTs for each cell
        print(self.All_slews)#2D numpy array to store output slew LUTs foreach cell
        print(self.Cload_vals)#1D numpy array corresponds to the 2nd index in the LUT
        print(self.Tau_in_vals) #1D numpy array corresponds to the 1st index in the LUT
        print("\n\n\n")

    def display_delays(self):   #display the values when delays is askked
        
        with open("delay_LUT.txt","a") as op_file:
            op_file.write(f"cell:  {self.Allgate_name}\n")
        #print('cell: ',self.Allgate_name)
        index1 = ''
        for x in self.Tau_in_vals:
            if index1 != '':
                index1 = index1 + ',' + x
            else:
                index1 = index1 + x
        index1 = index1 + ';'
        with open("delay_LUT.txt","a") as op_file:
            op_file.write(f"input slews:  {index1}\n")
        #print('input slews: ', index1)
        index2 = ''
        for x in self.Tau_in_vals:
            if index2 != '':
                index2 = index2 + ',' + x
            else:
                index2 = index2 + x
        index2 = index2 + ';'
        with open("delay_LUT.txt","a") as op_file:
            op_file.write(f"load cap:  {index2}\n")
            op_file.write('delays:\n')
        for x in self.All_delays:
            a=''
            for y in x:
                if a != '':
                    a = a + ',' + y
                else:
                    a = a + y
            a = a + ';\n'
            with open("delay_LUT.txt","a") as op_file:
                op_file.write(a)
        with open("delay_LUT.txt","a") as op_file:
                op_file.write("\n\n")
        

    def display_slews(self):            #display the values of when slew is asked
        with open("slew_LUT.txt","a") as op_file:
            op_file.write(f"cell:  {self.Allgate_name}\n")
        #print('cell: ',self.Allgate_name)
        index1 = ''
        for x in self.Tau_in_vals:
            if index1 != '':
                index1 = index1 + ',' + x
            else:
                index1 = index1 + x
        index1 = index1 + ';'
        with open("slew_LUT.txt","a") as op_file:
            op_file.write(f"input slews:  {index1}\n")
        #print('input slews: ', index1)
        index2 = ''
        for x in self.Tau_in_vals:
            if index2 != '':
                index2 = index2 + ',' + x
            else:
                index2 = index2 + x
        index2 = index2 + ';'
        with open("slew_LUT.txt","a") as op_file:
            op_file.write(f"load cap:  {index2}\n")
            op_file.write('slews:\n')
        #print('load cap: ',index2)
        #print('slews:')
        for x in self.All_slews:
            a=''
            for y in x:
                if a != '':
                    a = a + ',' + y
                else:
                    a = a + y
            a = a + ';\n'
            with open("slew_LUT.txt","a") as op_file:
                op_file.write(a)
        with open("slew_LUT.txt","a") as op_file:
                op_file.write("\n\n")
        


import re
import sys

A=sys.argv              #reading the arguments in the command line
option='read_NLDM'
file_name=''
read_NLDM_option = ''
if len(A)==3:
    option=A[1].replace('-','')
    file_name=A[2]
else:
    option=A[2].replace('-','')
    file_name=A[3]
    read_NLDM_option=A[1].replace('-','')

#print(A)

if option == 'read_ckt':
    input_count=0
    output_count=0
    gate_dict={}
    with open(file_name,"r") as f:                      #opening the file
        content=f.read()
        content = re.sub("\n","",re.sub("#.*\n","\n",content))          #removing the comments and endline gaps
        lines = re.split('\)',content)              #splitting the lines using the )

    #print(len(lines))
    ckt = []
    dictionary = {}
    dict_len = 0
    for x in lines:                         #creating a node for each element which has been placed in the file
        y=x.replace(' ','').replace('=',' ').replace('(',' ').replace(',',' ')      #replacimg the string seperators using spaces
        A=y.split(sep=' ')                  #splitting the string so that each valid element is sent to each value of list

        if A[0]=='INPUT':
            c=Node()
            c.naming(A[1], A[0])
            ckt.append(c)
            dictionary[A[1]]=dict_len           #adding the node names to a dictionry so that we can get the nodes needed to be added easily later on
            dict_len=dict_len+1
            input_count = input_count + 1       #for input node counts
        elif A[0]=='OUTPUT':
            c=Node()
            c.naming(A[1], A[0])
            c.fanout(A[1],A[0])
            ckt.append(c)
            dictionary[A[1]]=dict_len       #adding the node names to a dictionry so that we can get the nodes needed to be added easily later on
            dict_len=dict_len+1
            output_count = output_count + 1     #for output node counts
        else:
            if len(A)!=1:               #to ignore the last element in the list which has an endline character
                if A[0] not in list(dictionary):
                    c=Node()
                    c.naming(A[0],A[1])
                    ckt.append(c)
                    dictionary[A[0]]=dict_len
                    dict_len=dict_len+1


    for x in lines:             #to add fanins and fanouts to the nodes. This can be done in the previous loop itslef if the nodes are ordered structurally. The basic structure is same as previous loop
        y=x.replace(' ','').replace('=',' ').replace('(',' ').replace(',',' ')      
        A=y.split(sep=' ')
        if A[0] != 'INPUT' and A[0] != 'OUTPUT':
            if len(A)!=1:
                if ckt[dictionary[A[0]]].is_output():           #checking if the given node is a output node
                    ckt[dictionary[A[0]]].naming(A[0],A[1])
                    ckt[dictionary[A[0]]].fanout(A[0],'OUTPUT')     #adding itself as the output node
                    #print("check")
                    if A[1] in list(gate_dict):             #for finding out if a gate has already been found
                        gate_dict[A[1]] = gate_dict[A[1]] + 1
                    else:                                   #if not found entering a new entry with count 1
                        gate_dict[A[1]] = 1

                    for i in range(2,len(A)):               #for writing the fanin for the output node and fanouts for the input nodes
                        ckt[dictionary[A[0]]].fanin(A[i], ckt[dictionary[A[i]]].outname_node())
                        ckt[dictionary[A[i]]].fanout(A[0],A[1])
                    '''IN A the 0 has output node 1 has gate name and the next all are inputs'''
                else:                   #if the node in consideration is not an output node. The  loop structure is almost similar except where we donot add itself to its fanout
                    if A[1] in list(gate_dict):         
                        gate_dict[A[1]] = gate_dict[A[1]] + 1
                    else:
                        gate_dict[A[1]] = 1

                    for i in range(2,len(A)):
                        ckt[dictionary[A[0]]].fanin(A[i], ckt[dictionary[A[i]]].outname_node())
                        ckt[dictionary[A[i]]].fanout(A[0],A[1])
                
    '''The below code till else is for printing out the output in the required format or writing it to a seperate file'''

    with open("ckt_details.txt","w") as op_file:
        op_file.write(f"{input_count} primary inputs\n")
        op_file.write(f"{output_count} primary outputs\n")
    gate_count_str=''
    for x in list(gate_dict):
        if gate_count_str!='':
            gate_count_str = gate_count_str + '\n' + str(gate_dict[x]) + ' ' + x + " gates" 
        else:
            gate_count_str = gate_count_str + str(gate_dict[x]) + ' ' + x + " gates"

    with open("ckt_details.txt","a") as op_file:
        op_file.write(f"{gate_count_str}\n")
        op_file.write("Fanout...\n")

    for x in lines:
        y=x.replace(' ','').replace('=',' ').replace('(',' ').replace(',',' ')
        A=y.split(sep=' ')
        if len(A)!=1:
            if A[0]!='INPUT' and A[0]!='OUTPUT':
                with open("ckt_details.txt","a") as op_file:
                    ckt[dictionary[A[0]]].fanout_print(A[1],op_file)

    with open("ckt_details.txt","a") as op_file:
        op_file.write("Fanin...\n")
    for x in lines:
        y=x.replace(' ','').replace('=',' ').replace('(',' ').replace(',',' ')
        A=y.split(sep=' ')
        if len(A)!=1:        
            if A[0]!='INPUT' and A[0]!='OUTPUT':
                with open("ckt_details.txt","a") as op_file:
                    ckt[dictionary[A[0]]].fanin_print(A[1],op_file)






'''
under cell delay index1 are input slews index 2 are load cap and values are delays
match = re.search('output_slew\([\da-zA-Z_){(".,;]+\}',x)  for output slew
match = re.search('cell_delay\([\da-zA-Z_){(".,;]+\}',x) for cell_delay
match = re.search('index_1 *\( *"[\d,.]+"\)',x) for index_1
'''


if option=='read_nldm':

    with open(file_name,"r") as f:          #reading the file
        content =f.read()
        content =content.replace("\n","").replace("\t","").replace(" ","").replace("\\","")         ##replacing the endlines and tabs and spaces so that the string will be in one line
        content = re.sub("\/\*.*\*\/","",content)           ## removing the coments which are of the format /*.....*/.

        lines = re.split('cell *?\(',content)           ##splitting each celll based on the format given which is cell(
    #print(read_NLDM_option)
    A = []  
    for x in lines:
        if x[0:7] != 'library':         # the string part which starts with library when split in the explained format has the capacitances which is currently not required for phase 1 so ignored that part
            c=LUT()     #creating new LUT
            c.assign_data(x)    #filling the LUT object with its required data
            A.append(c)         #creating a list of LUT objects

    '''for x in A:
        x.display()
    '''
    if read_NLDM_option == 'delays':
        with open("delay_LUT.txt","w") as op_file:
            op_file.write("")
        for x in A:
            x.display_delays()  ##using display function to write the delay file
            #print('\n')

    elif read_NLDM_option == 'slews':
        with open("slew_LUT.txt","w") as op_file:
            op_file.write("")
        for x in A:
            x.display_slews()   ##using the display function to write the slew file
            #print('\n')

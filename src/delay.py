import re,sys
from sta_parser import circuit, LUT

C=circuit()
C.circuit_parsing('c17.bench')


lut_list=[]

with open('sample_NLDM.lib',"r") as f:          #reading the file
        content =f.read()
        content =content.replace("\n","").replace("\t","").replace(" ","").replace("\\","")         ##replacing the endlines and tabs and spaces so that the string will be in one line
        content = re.sub("\/\*.*\*\/","",content)           ## removing the coments which are of the format /*.....*/.

        lines = re.split('cell *?\(',content)           ##splitting each celll based on the format given which is cell(
 
for x in lines:
    if x[0:7] != 'library':         # the string part which starts with library when split in the explained format has the capacitances which is currently not required for phase 1 so ignored that part
        c=LUT()     #creating new LUT
        c.assign_data(x)    #filling the LUT object with its required data
        lut_list.append(c)         #creating a list of LUT objects

C.LUT_parsing('sample_NLDM.lib')
C.output_capacitance()
#C.circuit_to_file('ckt_details.txt')
C.circuit_delay()
print("circuit_delay done")
C.required_times()
C.slacks_find()
#print(C.req_arr_times)

count=0
for x in C.nodes:
     print("node",x.name)
     print("Outp_arrival",x.outp_arrival)
     print("input_arrivaal",x.inp_arrival)
     print("Inputs",x.inputs)
     print("Outputs",x.outputs)
     print("Required Arrival TIme",C.req_arr_times[count])
     print("slack" ,C.slacks[count])
     count=count+1
     print("\n\n\n")

print("Node 23")
print(C.nodes[6].outp_arrival)
print(C.nodes[6].inp_arrival)
print(C.nodes[6].inputs)
#C.required_times()

print("Node 22")
print(C.nodes[5].outp_arrival)
print(C.nodes[5].inp_arrival)
print(C.nodes[5].inputs)


print("Node 16")
print(C.nodes[8].outp_arrival)
print(C.nodes[8].inp_arrival)
print(C.nodes[8].inputs)

print("Node 19")
print(C.nodes[10].outp_arrival)
print(C.nodes[10].inp_arrival)
print(C.nodes[10].inputs)

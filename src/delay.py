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


##inputs
C.nodes[0].max_out_arrival= 0.00
C.nodes[0].Tau_out = 0.002
##add the out arrival to its 

C.nodes[1].max_out_arrival= 0.00
C.nodes[1].Tau_out = 0.002

C.nodes[2].max_out_arrival= 0.00
C.nodes[2].Tau_out = 0.002

C.nodes[3].max_out_arrival= 0.00
C.nodes[3].Tau_out = 0.002

C.nodes[4].max_out_arrival= 0.00
C.nodes[4].Tau_out = 0.002

##check node 
##loop for finding one node delay
C.nodes[7].outp_arrival.append(    C.nodes[C.dict[C.nodes[7].inputs[0]]].max_out_arrival + C.LUT_list[C.LUT_dict[C.nodes[7].outname]].findout_delay( C.nodes[C.dict[C.nodes[7].inputs[0]]].Tau_out, C.nodes[C.dict[C.nodes[7].inputs[0]]].Cload )  )

C.nodes[7].outp_arrival.append(    C.nodes[C.dict[C.nodes[7].inputs[1]]].max_out_arrival + C.LUT_list[C.LUT_dict[C.nodes[7].outname]].findout_delay( C.nodes[C.dict[C.nodes[7].inputs[1]]].Tau_out, C.nodes[C.dict[C.nodes[7].inputs[1]]].Cload )  )
##loop end for finding one node delay

##loop for finding one node delay
C.nodes[7].outp_arrival.append(    C.nodes[C.dict[C.nodes[7].inputs[0]]].max_out_arrival + C.LUT_list[C.LUT_dict[C.nodes[7].outname]].findout_delay( C.nodes[C.dict[C.nodes[7].inputs[0]]].Tau_out, C.nodes[C.dict[C.nodes[7].inputs[0]]].Cload )  )

C.nodes[7].outp_arrival.append(    C.nodes[C.dict[C.nodes[7].inputs[1]]].max_out_arrival + C.LUT_list[C.LUT_dict[C.nodes[7].outname]].findout_delay( C.nodes[C.dict[C.nodes[7].inputs[1]]].Tau_out, C.nodes[C.dict[C.nodes[7].inputs[1]]].Cload )  )
##loop end for finding one node delay

C.circuit_to_file('ckt_details.txt')

import re,sys
import argparse
from sta_parser import circuit, LUT

parser = argparse.ArgumentParser()

parser.add_argument("--read_ckt", type=str, help="File name of the circuit which neads to be analysed")
parser.add_argument("--read_nldm", type=str, help="The file name which contains all the values")

args = parser.parse_args()

read_ckt = args.read_ckt
read_nldm = args.read_nldm


C=circuit()
C.circuit_parsing(read_ckt)
C.LUT_parsing(read_nldm)
#C.LUT_delays_txt_file('delay_LUT.txt')
#C.LUT_slews_txt_file('slew_LUT.txt')
C.output_capacitance()
#C.circuit_to_file('ckt_details.txt')
C.circuit_delay()
C.required_times()
C.slacks_find()
print(C.path_find())
C.circuit_traversal('ckt_traversal.txt',read_ckt)
#print(C.req_arr_times)

#print(C.LUT_list[0].findout_delay(0.2,60))

'''
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
print(C.nodes[10].inputs)'''

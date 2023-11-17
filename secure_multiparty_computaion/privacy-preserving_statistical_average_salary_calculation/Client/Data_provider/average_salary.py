#!/usr/bin/python3

import sys

sys.path.append('.')

from Client.client import *
from Client.domains import *

n_computation_nodes = int(sys.argv[1])  #the number of SMPC node
computation_node_0_port_num = int(sys.argv[2])
ip = []
for i in range(n_computation_nodes):
    ip.append(sys.argv[3+i])


client_id = int(input("Please enter your ID:"))
salary = float(input("Please enter your salary:"))
gender = int(input("\n1.Male 2.Female 3.Other \nPlease choose your gender:"))

print("\n")
if gender not in [1, 2, 3]:
    raise ValueError("invalid gender type")

client = Client(ip, computation_node_0_port_num, client_id)

type = client.specification.get_int(4)

if type == ord('R'):
    domain = Z2(client.specification.get_int(4))
elif type == ord('p'):
    domain = Fp(client.specification.get_bigint())
else:
    raise Exception('invalid type')

multiple = 2 ** 16
client.send_private_inputs([domain(salary * multiple)])
client.send_private_inputs([domain(gender)])
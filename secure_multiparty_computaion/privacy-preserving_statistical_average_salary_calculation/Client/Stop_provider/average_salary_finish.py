#!/usr/bin/python3

import sys

sys.path.append('.')

from client import *
from domains import *

n_computation_nodes = int(sys.argv[1])
computation_node0_port_num = int(sys.argv[2])
ip = []
for i in range(n_computation_nodes):
    ip.append(sys.argv[3+i])


client_id = 0
salary = 0
gender = 0

client = Client(ip, computation_node0_port_num, client_id)

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

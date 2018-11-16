import re

"""define global msg dict"""
msg_dict = {}

"""return node dict"""
def node_info(file):
	dict = {}
	dbc_file = open(file, "r")
	for line in dbc_file:
		msgobj = re.match("BU_:\\s+(.*)", line)
		if msgobj:
			text = msgobj.group(1)
			str = text.split()
	for i in str:
		dict[i] = None
	dbc_file.close()
	return dict
	
def readdbc_init(file):

	"""read node info"""
	node_dict = node_info(file)
	global msg_dict
	"""init node"""
	temp_node_count_dict = {}

	for i in node_dict:
		node_dict[i] = {"tx_msg":{}, "rx_msg":{}}
		temp_node_count_dict[i] = 0
	dbc_file = open(file, "r")

	"""tx msg search and set init_msg_list"""
	count = 0
	for line in dbc_file:
		msgobj = re.match("BO_\\s+(\\w+)\\s+(\\w+):\\s+(\\w+)\\s+(\\w+)", line)#match tx msg
		if msgobj:
			node_dict[msgobj.group(4)]["tx_msg"].update({temp_node_count_dict[msgobj.group(4)]:int(msgobj.group(1))})
			msg_dict.update({int(msgobj.group(1)):{"msgname":msgobj.group(2), "dlc":msgobj.group(3), "signal":{}}})
			temp_node_count_dict[msgobj.group(4)] = temp_node_count_dict[msgobj.group(4)] + 1
			cur_msg = int(msgobj.group(1))
		"""match all signal"""
		signalobj = re.match('\\s+SG_\\s+(\\w+)\\s+:\\s+(\\d+)\\|(\\d+)@([01])([-\\+])\\s+\\((\\S+),(\\S+)\\)\\s+\\[(\\S+)\\|(\\S+)\\]\\s+"\\S*"\\s+(\\S+)', line)
		if signalobj:
			msg_dict[cur_msg]["signal"].update({signalobj.group(1):\
			{"startbit":signalobj.group(2), "siglen":signalobj.group(3),"endian":signalobj.group(4)\
			,"sign":signalobj.group(5),"accuracy":signalobj.group(6), "offset":signalobj.group(7),\
			"rxnode":signalobj.group(10)}})
			
		"""Add custom message and signal attributes"""
		"""@@      unfinish
		""" 
	"""search rx msg"""
	for i in msg_dict:#"""select msg"""
		for j in msg_dict[i]["signal"]:#select signal
			nodeobj = msg_dict[i]["signal"][j]["rxnode"].split(",")
			for m in range(0, len(nodeobj)):
				if nodeobj[m] in node_dict:#Determine if the receiving node exists
					temp_rx_msg_list = []
					for x,y in node_dict[nodeobj[m]]["rx_msg"].items():
						temp_rx_msg_list.append(y)
					if i not in temp_rx_msg_list:
						node_dict[nodeobj[m]]["rx_msg"].update({temp_node_count_dict[nodeobj[m]]:i})
						temp_node_count_dict[nodeobj[m]] = temp_node_count_dict[nodeobj[m]] + 1
					del temp_rx_msg_list
					
	"""msg sort small->large"""
	for i in node_dict:#select node
		temp_list = []
		temp_list_keys = []
		for j in node_dict[i]["tx_msg"]:#tx sort
			temp_list.append(node_dict[i]["tx_msg"][j])

		temp_list_keys = sorted(temp_list)
		for m in node_dict[i]["tx_msg"]:
			node_dict[i]["tx_msg"][m] = temp_list_keys[m]
		del temp_list
		del temp_list_keys
		
		rx_temp_list = []
		rx_temp_list_keys = []
		for j in node_dict[i]["rx_msg"]:#rx sort
			rx_temp_list.append(node_dict[i]["rx_msg"][j])

		rx_temp_list_keys = sorted(rx_temp_list)
		for m in node_dict[i]["rx_msg"]:
			node_dict[i]["rx_msg"][m] = rx_temp_list_keys[m - len(node_dict[i]["tx_msg"])]
	
		del rx_temp_list
		del rx_temp_list_keys
	del temp_node_count_dict
	dbc_file.close()	
	return node_dict

		
allnode = readdbc_init("HiFire_S106_INFOCAN_IVI_CAN_V1.5.dbc")
for j in allnode:
	print(j + ": " + str(allnode[j]))
for i in msg_dict:
	print(msg_dict[i]["msgname"])
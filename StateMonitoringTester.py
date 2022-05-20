import pika
import json
from SimCES_messaging import write_abstract_message, write_abstract_result
import datetime, time
from random import seed
from random import random

seed( time.time() )

connection = pika.BlockingConnection(
   pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
#channel.exchange_declare(exchange='simexe5', exchange_type='fanout')

simStartTime = datetime.datetime.utcnow()
t=0
x='simexe30'
x1='simexe31'

################################################################################# Start message 1
epoch=0

msg = {**write_abstract_message('Start', 'SimTest30', 'PlatformManager', 
		'SimulationManager'+str(epoch)), **write_abstract_result( epoch,[]  ) }

epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
msg["StartTime"]=epoch_time_beg.strftime('%d-%m-%YT%H:00:00Z')
msg["EndTime"]=epoch_time_end.strftime('%d-%m-%YT%H:00:00Z')
msg["Type"]="Start"
msg["SimulationId"]="SimTest30"
msg["SimulationSpecificExchange"]="simexe30"
msg["SimulationManager"] = {"MaxEpochCount": 2}


message = json.dumps( msg )
channel.basic_publish(exchange='procem-management11', routing_key='Start', body=message)
print(message)
time.sleep(1)


###################################################################################### Start message 2

msg = {**write_abstract_message('Start', 'SimTest31', 'PlatformManager', 
		'SimulationManager'+str(epoch)), **write_abstract_result( epoch, [] ) }

epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
msg["StartTime"]=epoch_time_beg.strftime('%d-%m-%YT%H:00:00Z')
msg["EndTime"]=epoch_time_end.strftime('%d-%m-%YT%H:00:00Z')
msg["Type"]="Start"
msg["SimulationId"]="SimTest31"
msg["SimulationSpecificExchange"]="simexe31"
msg["SimulationManager"] = {"MaxEpochCount": 2}



message = json.dumps( msg )
channel.basic_publish(exchange='procem-management11', routing_key='Start', body=message)
print(message)
time.sleep(1)
############################################################################ SimState message 1


msg = {**write_abstract_message('SimState', 'SimTest30', 'SimulationManager', 
		'SimulationManager1'+str(epoch)), **write_abstract_result( epoch, ['PlatformManager'+str(epoch)] ) }

epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
msg["StartTime"]=epoch_time_beg.strftime('%d-%m-%YT%H:00:00Z')
msg["EndTime"]=epoch_time_end.strftime('%d-%m-%YT%H:00:00Z')
msg["SimulationState"]="running"

message = json.dumps( msg )
channel.basic_publish(exchange='simexe30', routing_key='SimState', body=message)
print(message)
time.sleep(2)

############################################################################ SimState message 2

msg = {**write_abstract_message('SimState', 'SimTest31', 'SimulationManager', 
		'SimulationManager1'+str(epoch)), **write_abstract_result( epoch, ['PlatformManager'+str(epoch)] ) }

epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
msg["StartTime"]=epoch_time_beg.strftime('%d-%m-%YT%H:00:00Z')
msg["EndTime"]=epoch_time_end.strftime('%d-%m-%YT%H:00:00Z')
msg["SimulationState"]="running"

message = json.dumps( msg )
channel.basic_publish(exchange='simexe31', routing_key='SimState', body=message)
print(message)
time.sleep(2)

################################################################### Ready message from grid
msg = {**write_abstract_message('Status', 'SimTest30', 'Grid', 
		'Grid1'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }

epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
msg["Value"]="ready"

message = json.dumps( msg )
channel.basic_publish(exchange='simexe30', routing_key='Status.Ready', body=message)
print(message)
time.sleep(2)


msg = {**write_abstract_message('Status', 'SimTest31', 'Grid', 
		'Grid1'+str(epoch)), **write_abstract_result( epoch, [] ) }

epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
msg["Value"]="ready"

message = json.dumps( msg )
channel.basic_publish(exchange='simexe31', routing_key='Status.Ready', body=message)
print(message)
time.sleep(2)








####################################################################################################


for epoch in range(1,3):
	#
	# ########################################################################################Epoch msg 1
	#
	msg = {**write_abstract_message('Epoch', 'SimTest30', 'SimulationManager', 
		'SimulationManager'+str(epoch)), **write_abstract_result( epoch, [] ) }
		
	epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
	epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
	msg["StartTime"]=epoch_time_beg.strftime('%d-%m-%YT%H:00:00Z')
	msg["EndTime"]=epoch_time_end.strftime('%d-%m-%YT%H:00:00Z')
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='Epoch', body=message)
	print(message)
	time.sleep(t)
	

	###################################################################################Epoch message 2
	msg = {**write_abstract_message('Epoch', 'SimTest31', 'SimulationManager', 
		'SimulationManager'+str(epoch)), **write_abstract_result( epoch, [] ) }
		
	epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
	epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
	msg["StartTime"]=epoch_time_beg.strftime('%d-%m-%YT%H:00:00Z')
	msg["EndTime"]=epoch_time_end.strftime('%d-%m-%YT%H:00:00Z')
	
	message = json.dumps( msg )
	channel.basic_publish(exchange='simexe31', routing_key='Epoch', body=message)
	print(message)
	time.sleep(t)


	########################################################################################## Init.NIS.NetworkBusInfo 1
	msg = {**write_abstract_message('Init.NIS.NetworkBusInfo', 'SimTest30', 'Grid', 
		'BusInitialization'+str(epoch)), **write_abstract_result( epoch, ['Epoch'+str(epoch)] ) }
	msg["BusName"] = [
    "sourcebus",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11"
	]
	msg["BusType"] = [
    "root",
    "dummy",
    "dummy",
    "dummy",
    "dummy",
    "usage-point",
    "dummy",
    "usage-point",
    "dummy",
    "dummy",
    "usage-point",
    "usage-point"
  ]
	msg["BusVoltageBase"] = {"UnitOfMeasure": "kV",
    "Values": [
      20,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4
    ]}

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='Init.NIS.NetworkBusInfo', body=message)
	print(message)
	time.sleep(1)
########################################################################### Init.NIS.NetworkComponentInfo 1

	msg = {**write_abstract_message('Init.NIS.NetworkComponentInfo', 'SimTest30', 'Grid', 
		'BusInitialization'+str(epoch)), **write_abstract_result( epoch, ['Epoch'+str(epoch)] ) }
	msg["PowerBase"] = {
  "Value" : 50,
  "UnitOfMeasure" : "kV.A"
}
	msg["DeviceId"] = [ 
  "t1",
  "l1",
  "l2",
  "l3",
  "l4",
  "l5",
  "l6",
  "l7",
  "l8",
  "l9",
  "l10"
	]
	msg["SendingEndBus"] = [
  "sourcebus",
  "1",
  "2",
  "3",
  "4",
  "2",
  "6",
  "1",
  "8",
  "9",
  "8"
	]
	msg["ReceivingEndBus"] = [
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "10",
  "11"
	]
	msg["Resistance"] = {
  "UnitOfMeasure": "{pu}",
  "Values" : [
  0.072,
  0.056,
  0.084,
  0.054,
  0.064,
  0.249,
  0.143,
  0.016,
  0.074,
  0.077,
  0.001
  ]
}
	msg["Reactance"] = {
  "UnitOfMeasure": "{pu}",
  "Values" : [
  0.134,
  0.008,
  0.007,
  0.006,
  0.005,
  0.038,
  0.002,
  0.002,
  0.011,
  0.006,
  0
  ]
}
	msg["ShuntAdmittance"] = {
  "UnitOfMeasure": "{pu}",
  "Values" : [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
  ]
}
	msg["ShuntConductance"] = {
  "UnitOfMeasure": "{pu}",
  "Values" : [
  0.00256,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
  ]
}
	msg["RatedCurrent"] = {
  "UnitOfMeasure": "{pu}",
  "Values" : [
  1.739130435,
  1.12,
  0.72,
  1,
  0.72,
  1.12,
  0.624,
  1.12,
  1.12,
  0.72,
  0.8
  ]
}


	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='Init.NIS.NetworkComponentInfo', body=message)
	print(message)
	time.sleep(1)
########################################################################################## Init.NIS.NetworkBusInfo 2
	msg = {**write_abstract_message('Init.NIS.NetworkBusInfo', 'SimTest31', 'Grid', 
		'BusInitialization'+str(epoch)), **write_abstract_result( epoch, ['Epoch'+str(epoch)] ) }
	msg["BusName"] = [
    "sourcebus",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11"
	]
	msg["BusType"] = [
    "root",
    "dummy",
    "dummy",
    "dummy",
    "dummy",
    "usage-point",
    "dummy",
    "usage-point",
    "dummy",
    "dummy",
    "usage-point",
    "usage-point"
  ]
	msg["BusVoltageBase"] = {"UnitOfMeasure": "kV",
    "Values": [
      20,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4,
      0.4
    ]}

	message = json.dumps( msg )
	#channel.basic_publish(exchange='simexe31', routing_key='Init.NIS.NetworkBusInfo', body=message)
	print(message)
	time.sleep(1)
########################################################################### Init.NIS.NetworkComponentInfo 2

	msg = {**write_abstract_message('Init.NIS.NetworkComponentInfo', 'SimTest31', 'Grid', 
		'BusInitialization'+str(epoch)), **write_abstract_result( epoch, ['Epoch'+str(epoch)] ) }
	msg["PowerBase"] = {
  "Value" : 50,
  "UnitOfMeasure" : "kV.A"
}
	msg["DeviceId"] = [ 
  "t1",
  "l1",
  "l2",
  "l3",
  "l4",
  "l5",
  "l6",
  "l7",
  "l8",
  "l9",
  "l10"
	]
	msg["SendingEndBus"] = [
  "sourcebus",
  "1",
  "2",
  "3",
  "4",
  "2",
  "6",
  "1",
  "8",
  "9",
  "8"
	]
	msg["ReceivingEndBus"] = [
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "10",
  "11"
	]
	msg["Resistance"] = {
  "UnitOfMeasure": "{pu}",
  "Values" : [
  0.072,
  0.056,
  0.084,
  0.054,
  0.064,
  0.249,
  0.143,
  0.016,
  0.074,
  0.077,
  0.001
  ]
}
	msg["Reactance"] = {
  "UnitOfMeasure": "{pu}",
  "Values" : [
  0.134,
  0.008,
  0.007,
  0.006,
  0.005,
  0.038,
  0.002,
  0.002,
  0.011,
  0.006,
  0
  ]
}
	msg["ShuntAdmittance"] = {
  "UnitOfMeasure": "{pu}",
  "Values" : [
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
  ]
}
	msg["ShuntConductance"] = {
  "UnitOfMeasure": "{pu}",
  "Values" : [
  0.00256,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  0
  ]
}
	msg["RatedCurrent"] = {
  "UnitOfMeasure": "{pu}",
  "Values" : [
  1.739130435,
  1.12,
  0.72,
  1,
  0.72,
  1.12,
  0.624,
  1.12,
  1.12,
  0.72,
  0.8
  ]
}


	message = json.dumps( msg )
	channel.basic_publish(exchange='simexe31', routing_key='Init.NIS.NetworkComponentInfo', body=message)
	print(message)
	time.sleep(1)

############################################################################################### voltage value 1

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : 12.56,
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "sourcebus"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(1)
##################################################################################### voltage value 2
	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (12.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "sourcebus"
	msg["Node"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange='simexe31', routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)


	
	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "sourcebus"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "sourcebus"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "1"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "1"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "1"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus2-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "2"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus2-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "2"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus2-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "2"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus3-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "3"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus3-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "3"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus3-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "3"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus4-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "4"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus4-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "4"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus4-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "4"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus5-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "5"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus5-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "5"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus5-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "5"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus6-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "6"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus6-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "6"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus6-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "6"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus7-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "7"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus7-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "7"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus7-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "7"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus8-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "8"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus8-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "8"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus8-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "8"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus9-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "9"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus9-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "9"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus9-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "9"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus10-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "10"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus10-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "10"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus10-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "10"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus11-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "11"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)	

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus11-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "11"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest30', 'Grid', 
		'bus11-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "11"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	#############################################################################################################################################
	# Network state.Current msgs
	#


	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'transformer1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "t1"
	msg["Phase"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)


	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'transformer1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "t1"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'transformer1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = 't1'
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l1"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l1"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l1"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load2-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l2"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load2-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l2"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load2-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l2"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load3-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l3"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load3-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l3"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)
	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load3-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l3"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load4-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l4"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load4-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l4"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load4-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l4"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load5-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l5"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load5-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l5"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load5-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l5"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load6-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l6"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load6-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l6"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load6-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l6"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load7-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l7"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load7-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l7"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load7-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l7"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load8-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l8"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load8-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l8"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load8-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l8"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load9-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l9"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load9-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l9"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load9-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l9"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)	

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load10-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l10"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load10-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l10"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest30', 'Grid', 
		'load10-'+str(epoch)), **write_abstract_result( epoch, ['Resource'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l10"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)


################### Send ready message to the simulation manager



	msg = {**write_abstract_message('Status', 'SimTest30', 'Grid', 
		'Grid'+str(epoch)), **write_abstract_result( epoch, [] ) }

	epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
	epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
	msg["Value"]="ready"

	message = json.dumps( msg )
	channel.basic_publish(exchange=x, routing_key='Status.Ready', body=message)
	print(message)
	time.sleep(t)
#########################################################31######################################################################################################
	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "sourcebus"
	msg["Node"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "sourcebus"
	msg["Node"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "1"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "1"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "1"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "2"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "2"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "2"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "3"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "3"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "3"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "4"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "4"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "4"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "5"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "5"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "5"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "6"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "6"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "6"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "7"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "7"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "7"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "8"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "8"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "8"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "9"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "9"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "9"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "10"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "10"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "10"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "11"
	msg["Node"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)	

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "11"
	msg["Node"] = 2
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Voltage', 'SimTest31', 'Grid', 
		'gen1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["Magnitude"] = {
    "Value" : (11.56+0.45*random()+(epoch-1)*0.56),
    "UnitOfMeasure" : "kV"}
	msg["Angle"] = {
	"Value" : 119.5,
	"UnitOfMeasure" : "deg"}
	msg["Bus"] = "11"
	msg["Node"] = 3
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Voltage', body=message)
	print(message)
	time.sleep(t)

	#############################################################################################################################################
	# Network state.Current msgs
	#


	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "t1"
	msg["Phase"] = 1
	
	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)


	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "t1"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = 't1'
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l1"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l1"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l1"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l2"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l2"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l2"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l3"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l3"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)
	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l3"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l4"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l4"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l4"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l5"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l5"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l5"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l6"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l6"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l6"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l7"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l7"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l7"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l8"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l8"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l8"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l9"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l9"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l9"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)	

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l10"
	msg["Phase"] = 1

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l10"
	msg["Phase"] = 2

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)

	msg = {**write_abstract_message('NetworkState.Current', 'SimTest31', 'Grid', 
		'load1-'+str(epoch)), **write_abstract_result( epoch, ['SimulationManager'+str(epoch)] ) }
	msg["MagnitudeSendingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["MagnitudeReceivingEnd"] = { "Value": (80+9*epoch), "UnitOfMeasure": "A" }
	msg["AngleSendingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["AngleReceivingEnd"] = { "Value": 10.0, "UnitOfMeasure": "deg" }
	msg["DeviceId"] = "l10"
	msg["Phase"] = 3

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='NetworkState.Current', body=message)
	print(message)
	time.sleep(t)




	msg = {**write_abstract_message('Status', 'SimTest31', 'Grid', 
		'Grid'+str(epoch)), **write_abstract_result( epoch, [] ) }

	epoch_time_beg = simStartTime + datetime.timedelta(hours=epoch)
	epoch_time_end = simStartTime + datetime.timedelta(hours=epoch+1)
	msg["Value"]="ready"

	message = json.dumps( msg )
	channel.basic_publish(exchange=x1, routing_key='Status.Ready', body=message)
	print(message)
	time.sleep(t)









connection.close()

%                        StateMonitoring (SM) Application System
% In order to utilize the functionalities in the SM the user has to manually execute the AmqpConnector.
% The total application system includes the following programs:
% 1- AmqpConnector . (It listens to the Management exchange used by platform manager)
% Management exchange documentation: https://simcesplatform.github.io/core_exchange-mgmt/#management-exchange
% Platform manager documentation: https://simcesplatform.github.io/core_platformmanager/
% 2- ManagementCallback. (It initiates an instance of SM class)
% 3- StateMonitoring. (It operates the StateMonotoring functionalities in a simulation run)

% Two APIs are used here when listening to incoming messages:
% 1- the API is autonomuos in a sense that it receives incoming messages irrespective of SM's workload. The API is used to listen to the Management exchange. 
% Please visit https://kannisto.github.io/Cocop.AmqpMathToolConnector/
% 2- the API execution is dependant on the workload of SM. Once the SM is idle, a new message could come.
% Please visit https://github.com/simcesplatform/AmqpMathToolIntegration

global NumOfSimRun     % global variable for the whole Matlab environment specifying the number of simulation runs.
global Handles
global States
global Object
global SimulationId
SimulationId={};
Handles={};
States={};
NumOfSimRun=0;



amqpPropsM = eu.cocop.amqp2math.AmqpPropsManager('amqp.ain.rd.tut.fi','procem-management','procem-all','simu09LATION');
amqpPropsM.setSecure(true);
amqpPropsM.setPort(45671);
amqpPropsM.setExchangeDurable(true); 
amqpPropsM.setExchangeAutoDelete(false);
topicsIn = javaArray('java.lang.String',1);
topicsIn(1) = java.lang.String('Start'); 
amqpConnectorM = eu.cocop.amqp2math.AmqpConnector(amqpPropsM, topicsIn);
disp('Conected to the management exchange')

% Listener
notifier = amqpConnectorM.getNotifierForTopic('Start');
handleObj = handle(notifier, 'CallbackProperties');
set(notifier, 'ListenCallback', @(handleObj, ev)ManagementCallback(handleObj, ev));





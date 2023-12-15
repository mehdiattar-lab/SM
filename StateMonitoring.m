% Copyright 2023 Tampere University.
% This software was developed as a part of doctroal studies of Mehdi Attar, funded by Fortum and Neste Foundation.
% This source code is licensed under the MIT license. See LICENSE in the repository root directory.
% This software can only be deployed by SimCES platform. (https://simcesplatform.github.io/)
% Author: Mehdi Attar <mehdi.attar@tuni.fi>

classdef StateMonitoring < handle
    
    properties
        
        % Start message
        SimulationSpecificExchange
        SimulationId
        Grid
        SourceProcessId
        MaxVoltage
        MinVoltage
        UpperAmberBandVoltage
        LowerAmberBandVoltage
        OverloadingBaseline
        AmberLoadingBaseline
        
%         BusNames             % for testing
%         BranchNames          % for testing
        
        % Initialization (Epoch 1)
        NIS
        ExpectedNumberOfVoltageValues
        ExpectedNumberOfCurrentValues
        NumberofBuses
        NominalCurrent
        BranchResistance
        BranchReactance
        Susceptance
        
        % Epoch
        Epoch
        NumberOfReceivedVoltageValues
        NumberOfReceivedCurrentValues
        StartTime
        EndTime
        
        % Inbbound/outbound message counter
        InboundMessage
        MessageCounterInbound % Its value is continues between Epoches 
        MessageCounterOutbound % Its value is reset in the beginning of each Epoch
        
        % State
        State
        
        % Voltage
        VoltageStatus
        CurrentStatus
        VoltageReadinessFlag
        CurrentReadinessFlag
        StatusPublishingFlag   % 0 means not sent any result, 1 means either voltage or current, 2 means both
        GridReadinessFlag  % 0 means Grid is not ready yet, 1 means grid is ready, 2 means error happened in grid
        NISBusAnalysisFlag
        NISBranchAnalysisFlag
        
        % connector to simulation specific exchange (ProcemPlus lib)
        AmqpConnector
        
        % Result
        AbstractResult
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    methods
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Constructor
        
        function obj = StateMonitoring(SimulationSpecificExchange,SimulationId,SMName,MonitoredGridId,MaxVoltage,MinVoltage,UpperAmberBandVoltage,LowerAmberBandVoltage,OverloadingBaseline,AmberLoadingBaseline)  
            obj.SimulationSpecificExchange = SimulationSpecificExchange; % Start message
            obj.SimulationId = SimulationId;
            obj.SourceProcessId = SMName;
            obj.Grid = MonitoredGridId;
            obj.MaxVoltage=MaxVoltage;
            obj.MinVoltage=MinVoltage;
            obj.UpperAmberBandVoltage=UpperAmberBandVoltage;
            obj.LowerAmberBandVoltage=LowerAmberBandVoltage;
            obj.OverloadingBaseline=OverloadingBaseline;
            obj.AmberLoadingBaseline=AmberLoadingBaseline;

            obj.ExpectedNumberOfVoltageValues=0;    % Initialization (Epoch 1)
            obj.ExpectedNumberOfCurrentValues=0;

            obj.NumberOfReceivedVoltageValues=0;    % Epoch
            obj.NumberOfReceivedCurrentValues=0;

            obj.MessageCounterInbound=0;    % Inbound/outbound message counter
            obj.MessageCounterOutbound=0;

            obj.State='Free';   % State
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 1
        
        function Done=Main(obj)
            obj.Subscription;
            obj.GetMsg;
            if strcmp(obj.State,'Stopped')
                Done=true;
            end
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 2
        
        function Subscription(obj)
            AmqpProps = fi.procemplus.amqp2math.AmqpPropsManager('amqp.ain.rd.tut.fi',obj.SimulationSpecificExchange,'procem-all','simu09LATION'); % Based on what is specified in the Start message, SM listens to that exchange.
            AmqpProps.setSecure(true);
            AmqpProps.setPort(45671);   % Default AMQP port
            AmqpProps.setExchangeDurable(false);    % Uncomment this line if settings in the AMQP broker is activated
            AmqpProps.setExchangeAutoDelete(true);  % Uncomment this line if settings in the AMQP broker is activated
            
            topicsIn = javaArray('java.lang.String',8); % SM needs to at least listen to 8 different topics as mentioned below
            topicsIn(1) = java.lang.String('SimState'); % SM needs to SimState topic published by Simulation Manager
            topicsIn(2) = java.lang.String('Status.Ready'); % SM needs to listen to Status.Ready topic published by of Grid 
            topicsIn(3) = java.lang.String('Status.Error'); % SM needs to listen to Status.Error topic published by Grid
            topicsIn(4) = java.lang.String('Epoch');    % SM needs to listen to Epoch topic published by Simulation manager
%             topicsIn(5) = java.lang.String(strcat('NetworkState.',obj.Grid,'.Voltage.#')); % SM needs to listen to NetworkState.Voltage.# topic published by Grid. (# is wild card to receive all voltage data)
            topicsIn(5) =  java.lang.String('NetworkState.Voltage.#'); % 
            topicsIn(6) = java.lang.String('NetworkState.Current.#'); % SM needs to listen to NetworkState.Current.# topic published by Grid. (# is wild card to receive all voltage data)
            topicsIn(7) = java.lang.String('Init.NIS.NetworkBusInfo');  % SM needs to listen to Init.NIS.NetworkBusInfo topic published by Grid in the Epoch 1 
            topicsIn(8) = java.lang.String('Init.NIS.NetworkComponentInfo');    % SM needs to listen to Init.NIS.NetworkComponentInfo topic published by Grid in the Epoch 1

            obj.AmqpConnector = fi.procemplus.amqp2math.AmqpTopicConnectorSync(AmqpProps, topicsIn); % using procemplus API for RabbitMQ broker connection
            disp(['connected to the simulation specific exchange:' obj.SimulationSpecificExchange])
            disp(['SimulationId:' obj.SimulationId])
            clear topicsIn
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 3
        
        function Out=GetMsg(obj)
            while 1>0
                obj.State='Free';
                message = obj.AmqpConnector.getMessage();
                if ~isempty(message)
                    mystr = message.getBody();
                    str = char(mystr);  %    Making the input into a character array
                    obj.InboundMessage = jsondecode(str'); % decoding JSON data. please note that jsondecode for Matlab versions 2018 and later receives only row vectors.(that's why str is str')
                    clear message mystr str
                    obj.MessageCounterInbound=obj.MessageCounterInbound+1; % inbound message counter
                    obj.Listener;
                else
                    pause(1);   % in order not to over load Matlab
                end
                if strcmp(obj.State,'Stopped')
                   Out=true; 
                end
            end
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 4
        
        function Listener(obj)
            if strcmp(obj.State,'Free')
                obj.State='Busy';   % Trun the SM state to "Busy" to block arrival a new message
                if strcmp(obj.SimulationId,obj.InboundMessage.SimulationId) % making sure that incoming message belongs to the current simulation run.

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When SimulationManager publishes the SimState message

                    if strcmp(obj.InboundMessage.Type,'SimState')
                        if strcmp(obj.InboundMessage.SimulationState,'running')
                            obj.AbstractResult.Type='Status';
                            obj.AbstractResult.SimulationId=obj.SimulationId{1};
                            obj.AbstractResult.SourceProcessId=obj.SourceProcessId;
                            obj.MessageCounterOutbound=obj.MessageCounterOutbound+1;
                                s = strcat('StateMonitoring',num2str(obj.MessageCounterOutbound)); % Making the number of outbound messages string to create MessageId
                            obj.AbstractResult.MessageId=s;
                                t = datetime('now', 'TimeZone', 'UTC');
                                t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
                            obj.AbstractResult.Timestamp=t;
                            obj.AbstractResult.EpochNumber=0;
                            obj.Epoch=0;         % it sets the Epoch number in the object
                            obj.AbstractResult.TriggeringMessageIds={obj.InboundMessage.MessageId};
                            obj.AbstractResult.Value='ready';   % SM publishes a ready message
                            disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                            disp('SM reported "ready" message to Simulation Manager as response to SimState message')
                            disp(['SimulationId:' obj.SimulationId])
                            MyStringOut = java.lang.String(jsonencode(obj.AbstractResult));
                            MyBytesOut = MyStringOut.getBytes(java.nio.charset.Charset.forName('UTF-8'));
                            obj.AmqpConnector.sendMessage('Status.Ready', MyBytesOut); % The topic is "Status.Ready" that SM publishes to
                            clear t MyStringOut MyBytesOut
                            obj.AbstractResult=[];
                        elseif strcmp(obj.InboundMessage.SimulationState,'stopped')
                            obj.State='Stopped';    % Turn the SM state to stopped.
                        end
                    end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When Grid publishes the Status message for Epoches>0

                    if strcmp(obj.InboundMessage.Type,'Status')     
                       if obj.InboundMessage.EpochNumber~=0     % For Epoches > 0
                           if strcmp(obj.InboundMessage.SourceProcessId,obj.Grid)      % just analyse the status message that is published by Grid
                              obj.StatusReadinessGrid; % the SM is ready once the grid is ready,and the excpected voltages and currents have already arrived.
                           end
                       end
                   end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When SimulationManager publishes the Epoch message 

                    if strcmp(obj.InboundMessage.Type,'Epoch')
                        if obj.InboundMessage.EpochNumber>obj.Epoch % It only reacts to new Epoches
                            disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%') % for visualization purposes
                            disp(['Epoch number=' num2str(obj.InboundMessage.EpochNumber)])
                            disp(['Start Time=' obj.InboundMessage.StartTime])
                            disp(['End Time=' obj.InboundMessage.EndTime])
                            disp(['SimulationId:' obj.SimulationId])
                            disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                            obj.Epoch=obj.InboundMessage.EpochNumber;              % Making the Epoch number the Object's property
                            obj.StartTime=obj.InboundMessage.StartTime;
                            obj.EndTime=obj.InboundMessage.StartTime;
                            obj.NumberOfReceivedVoltageValues=0;    % Resetting the number of received voltage values during the previous Epoch
                            obj.NumberOfReceivedCurrentValues=0;    % Resetting the number of received current values during the previous Epoch
                            obj.MessageCounterOutbound=0;   % Resetting the number of outbound message for each Epoch
                            obj.VoltageReadinessFlag=0;
                            obj.CurrentReadinessFlag=0;
                            obj.StatusPublishingFlag=0;
                            obj.GridReadinessFlag=0;
                            obj.NISBusAnalysisFlag=0;
                            obj.NISBranchAnalysisFlag=0;
                        end
                    end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When Grid publishes Bus data message- NIS

                    if strcmp(obj.InboundMessage.Type,'Init.NIS.NetworkBusInfo')
                        obj.NISBusAnalysis;
                    end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When Grid publishes Branch data message- NIS

                    if strcmp(obj.InboundMessage.Type,'Init.NIS.NetworkComponentInfo')
                        obj.NISBranchAnalysis;
                    end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When Grid published the network's voltages

                    if strcmp(obj.InboundMessage.Type,'NetworkState.Voltage')
                        if obj.InboundMessage.EpochNumber==obj.Epoch
                            obj.VoltageAnalysis;
                        end   
                    end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% When Grid published the network's currents

                    if strcmp(obj.InboundMessage.Type,'NetworkState.Current')
                        if obj.InboundMessage.EpochNumber==obj.Epoch
                            obj.CurrentAnalysis;
                       end
                   end

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

                else                     % Sending a warning if the inbound message doesnot match the SimulationId
                    obj.State='Free';
                    obj.AbstractResult.Type='DMSNetworkStatus';
                    obj.AbstractResult.SimulationId=obj.SimulationId{1};
                    obj.AbstractResult.SourceProcessId=obj.SourceProcessId;
                    obj.MessageCounterOutbound=obj.MessageCounterOutbound+1;
                        s = strcat('StateMonitoring',num2str(obj.MessageCounterOutbound));
                    obj.AbstractResult.MessageId=s;
                    obj.AbstractResult.EpochNumber=obj.Epoch;
                    obj.AbstractResult.TriggeringMessageIds={obj.InboundMessage.MessageId};
                        t = datetime('now', 'TimeZone', 'UTC');
                        t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
                    obj.AbstractResult.Timestamp=t;
                    obj.AbstractResult.Warnings='warning.input';
                    MyStringOut = java.lang.String(jsonencode(obj.AbstractResult));
                    MyBytesOut = MyStringOut.getBytes(java.nio.charset.Charset.forName('UTF-8'));
                    obj.AmqpConnector.sendMessage('DMSNetworkStatus', MyBytesOut);
                    obj.AbstractResult=[];
                    clear MyStringOut MyBytesOut t s
                end
            end
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 5
        
        function NISBusAnalysis(obj)
            if obj.NISBusAnalysisFlag==0
                obj.NumberofBuses=numel(obj.InboundMessage.BusName);
                obj.ExpectedNumberOfVoltageValues=obj.NumberofBuses*3;
                NumberofBusColumn=14;
                obj.NIS.BusUnits=cell(obj.NumberofBuses,NumberofBusColumn); % The NISGrid1's structure is based on Power System Toolbox format. Please refer to that to know how data are organized in Bus and Branch matrixes.  
                obj.NIS.OriginalBusNames=cell(obj.NumberofBuses,1);

                %%%%% Bus name and number

                RootBusRow=find(strcmp(obj.InboundMessage.BusType(:,1),"root"));
                if RootBusRow>1    % bring the root bus to row number 1 
                    obj.InboundMessage.BusType([1 RootBusRow],1)=obj.InboundMessage.BusType([RootBusRow 1],1);
                    obj.InboundMessage.BusName([1 RootBusRow],1)=obj.InboundMessage.BusName([RootBusRow 1],1);
                    obj.InboundMessage.BusVoltageBase.Values([1 RootBusRow],1)=obj.InboundMessage.BusVoltageBase.Values([RootBusRow 1],1);
                end
                obj.NIS.OriginalBusNames=cellstr(obj.InboundMessage.BusName);
                obj.NIS.OriginalBusNamesString=string(obj.InboundMessage.BusName);
                obj.NIS.Bus(:,1)=(1:length(obj.InboundMessage.BusName));
%                 obj.BusNames=repelem(obj.NIS.OriginalBusNames(:,1),3);              % for testing

                %%%%% Bus Type- Enumeration

                for i=1:1:obj.NumberofBuses
                    if strcmp(obj.InboundMessage.BusType(i,1),'root')
                        obj.InboundMessage.BusType(i,1)=cellstr('3');
                    elseif strcmp(obj.InboundMessage.BusType(i,1),'dummy')
                        obj.InboundMessage.BusType(i,1)=cellstr('1');
                    elseif strcmp(obj.InboundMessage.BusType(i,1),'usage-point')
                        obj.InboundMessage.BusType(i,1)=cellstr('1');
                    end
                end

                 obj.NIS.Bus(:,2)=str2double(obj.InboundMessage.BusType);

                 %%%%% Unit of measure

                if strcmp(obj.InboundMessage.BusVoltageBase.UnitOfMeasure,'kV')
                    obj.NIS.BusUnits(:,10)=cellstr('kV');
                    elseif strcmp(obj.InboundMessage.BusVoltageBase.UnitOfMeasure,'V')
                        obj.NIS.BusUnits(:,10)=cellstr('V');
                end

                %%%%% Bus voltage base

                obj.NIS.Bus(:,10)=obj.InboundMessage.BusVoltageBase.Values;

                %%%%% Voltage min and max (p.u.)

                obj.NIS.Bus(:,12)=obj.MinVoltage;
                obj.NIS.Bus(:,13)=obj.MaxVoltage;
                disp('Network initialization of the Bus matrix is done')
                disp(['SimulationId:' obj.SimulationId])
                disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                obj.NISBusAnalysisFlag=1;
            end
            clear VARIABLES;
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 6
        
        function NISBranchAnalysis(obj)
            if obj.NISBranchAnalysisFlag==0
                obj.NIS.Sbase.Value=obj.InboundMessage.PowerBase.Value;
                obj.NIS.Sbase.UnitofMeasure=obj.InboundMessage.PowerBase.UnitOfMeasure;
                NumberofBranches=length(obj.InboundMessage.SendingEndBus);
                if NumberofBranches~=obj.NumberofBuses-1
                    disp("The distribution network is not radial") 
                end
                obj.ExpectedNumberOfCurrentValues=NumberofBranches*3;
                NumberOfBranchColumn=12;

                obj.NIS.Branch=zeros(NumberofBranches,NumberOfBranchColumn);
                obj.NIS.BranchUnits=cell(NumberofBranches,NumberOfBranchColumn);
                obj.NIS.DeviceId=cell(NumberofBranches,1);
                obj.NIS.OriginalNameofSendingEndBus=cell(NumberofBranches,1);
                obj.NIS.OriginalNameofReceivingEndBus=cell(NumberofBranches,1);

                SourceBusName=obj.NIS.OriginalBusNames(1);
                RootBusRow=find(string(obj.InboundMessage.SendingEndBus(:))==string(SourceBusName));
                if RootBusRow>1 % Assuring that the first line of the NIS.NetworkComponenetInfo starts with root bus (the change is needed because sensitivity analysis assumes that the first row contains the root bus)
                    obj.InboundMessage.DeviceId([1 RootBusRow],1)=obj.InboundMessage.DeviceId([RootBusRow 1],1);
                    obj.InboundMessage.SendingEndBus([1 RootBusRow],1)=obj.InboundMessage.SendingEndBus([RootBusRow 1],1);
                    obj.InboundMessage.ReceivingEndBus([1 RootBusRow],1)=obj.InboundMessage.ReceivingEndBus([RootBusRow 1],1);
                    obj.InboundMessage.Resistance.Values([1 RootBusRow],1)=obj.InboundMessage.Resistance.Values([RootBusRow 1],1);
                    obj.InboundMessage.Reactance.Values([1 RootBusRow],1)=obj.InboundMessage.Reactance.Values([RootBusRow 1],1);
                    obj.InboundMessage.ShuntAdmittance.Values([1 RootBusRow],1)=obj.InboundMessage.ShuntAdmittance.Values([RootBusRow 1],1);
                    obj.InboundMessage.ShuntConductance.Values([1 RootBusRow],1)=obj.InboundMessage.ShuntConductance.Values([RootBusRow 1],1);
                    obj.InboundMessage.RatedCurrent.Values([1 RootBusRow],1)=obj.InboundMessage.RatedCurrent.Values([RootBusRow 1],1);
                end
                obj.NIS.OriginalNameofSendingEndBus=cellstr(obj.InboundMessage.SendingEndBus);
                obj.NIS.OriginalNameofReceivingEndBus=cellstr(obj.InboundMessage.ReceivingEndBus);

                %%%%% 

                for i=1:NumberofBranches  % since buses are named when NetworkBusInfo is arrived, then the same bus names for branches are used.
                    A=string(obj.NIS.OriginalNameofSendingEndBus(i,1));
                    row=find(strcmp(string(obj.NIS.OriginalBusNames),A)); % function "find" only acts on string arrays
                    obj.NIS.Branch(i,1)=row;
                    B=string(obj.NIS.OriginalNameofReceivingEndBus(i,1));
                    row=find(strcmp(string(obj.NIS.OriginalBusNames),B));
                    obj.NIS.Branch(i,2)=row;
                end

                obj.NIS.Branch(:,3)=obj.InboundMessage.Resistance.Values;
                obj.NIS.BranchUnits(:,3)=cellstr(obj.InboundMessage.Resistance.UnitOfMeasure);

                obj.NIS.Branch(:,4)=obj.InboundMessage.Reactance.Values;
                obj.NIS.BranchUnits(:,4)=cellstr(obj.InboundMessage.Reactance.UnitOfMeasure);

                obj.NIS.Branch(:,5)=obj.InboundMessage.ShuntAdmittance.Values;
                obj.NIS.BranchUnits(:,5)=cellstr(obj.InboundMessage.ShuntAdmittance.UnitOfMeasure);

                obj.NIS.Branch(:,6)=obj.InboundMessage.ShuntConductance.Values;
                obj.NIS.BranchUnits(:,6)=cellstr(obj.InboundMessage.ShuntConductance.UnitOfMeasure);

                obj.NIS.Branch(:,12)=obj.InboundMessage.RatedCurrent.Values;
                obj.NIS.BranchUnits(:,12)=cellstr(obj.InboundMessage.RatedCurrent.UnitOfMeasure);
                obj.NIS.DeviceId=cellstr(obj.InboundMessage.DeviceId);
                obj.NIS.DeviceIdString=obj.InboundMessage.DeviceId;
%                 obj.BranchNames=repelem(obj.NIS.DeviceId,3);         % just for testing
                

                %%%%% Calculation of the base values of current

                if strcmp(string(obj.NIS.Sbase.UnitofMeasure),'kV.A')
                    if strcmp(string(obj.NIS.BusUnits(1,10)),'V')
                        for i=1:1:NumberofBranches
                            Ibase(i,1)=1000*(obj.NIS.Sbase.Value/(sqrt(3)*obj.NIS.Bus(i,10))); %Ibase
                            obj.NominalCurrent(i,1)=Ibase(i,1)*obj.NIS.Branch(i,12);
                            Zbase(i,1)=obj.NIS.Bus(i,10)/(sqrt(3)*Ibase(i,1)); %Zbase
                            obj.BranchResistance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,3);
                            obj.BranchReactance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,4); % Branch reactance in Ohm
                            obj.Susceptance(i,1)=(1./Zbase(i,1))*obj.NIS.Branch(i,4); % Susceptance in ohm
                        end
                    end
                end
                if strcmp(string(obj.NIS.Sbase.UnitofMeasure),'V.A')
                    if strcmp(string(obj.NIS.BusUnits(1,10)),'kV')
                         for i=1:1:NumberofBranches
                            Ibase(i,1)=0.001*(obj.NIS.Sbase.Value/(sqrt(3)*obj.NIS.Bus(i,10))); % Ibase
                            obj.NominalCurrent(i,1)=Ibase(i,1)*obj.NIS.Branch(i,12); % Ibase*ReatedCurrent
                            Zbase(i,1)=1000*(obj.NIS.Bus(i,10)/(sqrt(3)*Ibase(i,1))); %Zbase
                            obj.BranchResistance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,3);
                            obj.BranchReactance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,4); % Branch reactance in Ohm
                            obj.Susceptance(i,1)=(1./Zbase(i,1))*obj.NIS.Branch(i,4); % Susceptance in ohm
                         end
                    end
                end
                if strcmp(string(obj.NIS.Sbase.UnitofMeasure),'V.A')
                    if strcmp(string(obj.NIS.BusUnits(1,10)),'V')
                        for i=1:1:NumberofBranches
                            Ibase(i,1)=(obj.NIS.Sbase.Value/(sqrt(3)*obj.NIS.Bus(i,10)));  % Ibase
                            obj.NominalCurrent(i,1)=Ibase(i,1)*obj.NIS.Branch(i,12);
                            Zbase(i,1)=(obj.NIS.Bus(i,10)/(sqrt(3)*Ibase(i,1)));
                            obj.BranchResistance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,3);
                            obj.BranchReactance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,4); % Branch reactance in Ohm
                            obj.Susceptance(i,1)=(1./Zbase(i,1))*obj.NIS.Branch(i,4); % Susceptance in ohm
                        end
                    end
                end
                if strcmp(string(obj.NIS.Sbase.UnitofMeasure),'kV.A')
                    if strcmp(string(obj.NIS.BusUnits(1,10)),'kV')
                        for i=1:1:NumberofBranches % Sbase="kV.A", Vbase="kV"
                            Ibase(i,1)=(obj.NIS.Sbase.Value/(sqrt(3)*obj.NIS.Bus(i,10)));  % Ibase(A)=Sbase/sqrt(3)*BusVoltageBase
                            obj.NominalCurrent(i,1)=Ibase(i,1)*obj.NIS.Branch(i,12);  % NominalCurrent(A)=Ibase(A)*RatedCurrent(p.u.)
                            Zbase(i,1)=1000*(obj.NIS.Bus(i,10)/(sqrt(3)*Ibase(i,1))); %Zbase=1000(BusVoltageBase(kV)/sqrt(3)*Ibase(A))
                            obj.BranchResistance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,3); % Branch resistance in Ohm
                            obj.BranchReactance(i,1)=Zbase(i,1)*obj.NIS.Branch(i,4); % Branch reactance in Ohm
                            obj.Susceptance(i,1)=(1./Zbase(i,1))*obj.NIS.Branch(i,4); % Susceptance in ohm
                        end
                    end
                end
                clear Ibase Zbase NumberofBranches NumberOfBranchColumn    % Freeing up memory
                disp('Network initialization of the Branch matrix is done')
                disp(['SimulationId:' obj.SimulationId])
                disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                obj.NISBranchAnalysisFlag=1;
            end
            clear VARIABLES;
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 7
        
        function VoltageAnalysis(obj)
            if obj.InboundMessage.Node<4
                if (obj.VoltageReadinessFlag)<1
                    VoltageViolationFlag=0;
                    obj.NumberOfReceivedVoltageValues=obj.NumberOfReceivedVoltageValues+1;
                    Row = find(obj.NIS.OriginalBusNamesString == obj.InboundMessage.Bus); % finding the Row of the Bus
%                     BusName=obj.NIS.OriginalBusNames(Row,1);
                    
%                     rrr=find(string(obj.BusNames(:,1))==BusName,1); % just for testing
%                     obj.BusNames(rrr,1)=cellstr("00");                         % just for testing
                    
%                     Node=obj.InboundMessage.Node;
                    NominalVoltage=(obj.NIS.Bus(Row,10))/sqrt(3);
                    Vmin1=(obj.MinVoltage+obj.LowerAmberBandVoltage)*NominalVoltage; % kV
                    Vmax1=(obj.MaxVoltage-obj.UpperAmberBandVoltage)*NominalVoltage; % kV
                    Vmin2=obj.MinVoltage*NominalVoltage; % kV
                    Vmax2=obj.MaxVoltage*NominalVoltage; % kV

                    %%%%% Voltage level analysis

                    if (obj.InboundMessage.Magnitude.Value>Vmax1)
                        if (obj.InboundMessage.Magnitude.Value<Vmax2)
                            Status='close-to-limits';
                            Violation=0;
                        end
                    end
                    if obj.InboundMessage.Magnitude.Value>Vmax2 % Over-voltage
                        Status='unacceptable';
                        Violation=obj.InboundMessage.Magnitude.Value-Vmax2;
                    end
                    if obj.InboundMessage.Magnitude.Value<Vmin1
                        if obj.InboundMessage.Magnitude.Value>Vmin2
                            Status='close-to-limits'; 
                            Violation=0;
                        end
                    end
                    if obj.InboundMessage.Magnitude.Value<Vmin2 % Under-voltage
                        Status='unacceptable';
                        Violation=obj.InboundMessage.Magnitude.Value-Vmin2;
                    end

                    if VoltageViolationFlag==0
                        Status='acceptable';
                        Violation=0;
                    end

                    obj.VoltageStatus(obj.NumberOfReceivedVoltageValues).BusName=obj.NIS.OriginalBusNames(Row,1);
                    obj.VoltageStatus(obj.NumberOfReceivedVoltageValues).Node=obj.InboundMessage.Node;
                    obj.VoltageStatus(obj.NumberOfReceivedVoltageValues).Status=Status;
                    obj.VoltageStatus(obj.NumberOfReceivedVoltageValues).Violation=Violation;
                    clear Violation Status Vmin1 Vmax1 Vmin2 Vmax2 VoltageViolationFlag Row
                    
                    if obj.NumberOfReceivedVoltageValues==obj.ExpectedNumberOfVoltageValues
                        obj.VoltageReadinessFlag=1;
%                         RemainingBusNames=obj.BusNames  just for testing
                        disp('All voltages was received')
                        obj.Publisher
                    end
                end
            end
            clear VARIABLES;
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 8
        
        function CurrentAnalysis(obj)
            if (obj.CurrentReadinessFlag)<1
                CurrentViolationSendingFlag=0;
                CurrentViolationReceivingFlag=0;
                obj.NumberOfReceivedCurrentValues=obj.NumberOfReceivedCurrentValues+1;
                Row = find(obj.NIS.DeviceIdString == string(obj.InboundMessage.DeviceId)) ;
%                 DeviceId=obj.NIS.DeviceId(Row,1);
%                 Phase=obj.InboundMessage.Phase;
                
%                 wwww=find(strcmp(string(obj.BranchNames(:,1)),DeviceId),1);
%                 obj.BranchNames(wwww,1)=cellstr("0");           % just for testing
                

%                FromBus=obj.NIS.Branch(Row,1);
%                ToBus=obj.NIS.Branch(Row,2);
%                 NominalCurrent=obj.NominalCurrent(Row,1);  removed for memory
                Imax1=(obj.NominalCurrent(Row,1))*obj.AmberLoadingBaseline;
                Imax2=(obj.NominalCurrent(Row,1))*obj.OverloadingBaseline;

                %%%%% Current level analysis

                if (obj.InboundMessage.MagnitudeSendingEnd.Value>Imax1)
                    if (obj.InboundMessage.MagnitudeSendingEnd.Value<Imax2)
                        CurrentViolationSendingFlag=1;
                        StatusSendingEnd='close-to-limits';
                        ViolationSendingEnd=0;
                    end
                end
                if (obj.InboundMessage.MagnitudeReceivingEnd.Value>Imax1)
                    if (obj.InboundMessage.MagnitudeReceivingEnd.Value<Imax2)
                        CurrentViolationReceivingFlag=1;
                        StatusReceivingEnd='close-to-limits';
                        ViolationReceivingEnd=0;
                    end
                end
                if obj.InboundMessage.MagnitudeSendingEnd.Value>Imax2 % Over-loading
                    CurrentViolationSendingFlag=1;
                    StatusSendingEnd='unacceptable';
                    ViolationSendingEnd=obj.InboundMessage.MagnitudeSendingEnd.Value-Imax2;
                end
                if obj.InboundMessage.MagnitudeReceivingEnd.Value>Imax2 % Over-loading
                    CurrentViolationReceivingFlag=1;
                    StatusReceivingEnd='unacceptable';
                    ViolationReceivingEnd=obj.InboundMessage.MagnitudeReceivingEnd.Value-Imax2;
                end

                if CurrentViolationSendingFlag==0
                    StatusSendingEnd='Acceptable';
                    ViolationSendingEnd=0;
                end
                if CurrentViolationReceivingFlag==0
                    StatusReceivingEnd='Acceptable';
                    ViolationReceivingEnd=0;
                end
                obj.CurrentStatus(obj.NumberOfReceivedCurrentValues).DeviceId=obj.NIS.DeviceId(Row,1);
                obj.CurrentStatus(obj.NumberOfReceivedCurrentValues).Phase=obj.InboundMessage.Phase;
                obj.CurrentStatus(obj.NumberOfReceivedCurrentValues).StatusSendingEnd=StatusSendingEnd;
                obj.CurrentStatus(obj.NumberOfReceivedCurrentValues).StatusReceivingEnd=StatusReceivingEnd;
                obj.CurrentStatus(obj.NumberOfReceivedCurrentValues).ViolationSendingEnd=ViolationSendingEnd;
                obj.CurrentStatus(obj.NumberOfReceivedCurrentValues).ViolationReceivingEnd=ViolationReceivingEnd;
                clear Imax1 Imax2 Row StatusReceivingEnd ViolationReceivingEnd StatusSendingEnd ViolationSendingEnd

                if obj.ExpectedNumberOfCurrentValues==obj.NumberOfReceivedCurrentValues
                    obj.CurrentReadinessFlag=1;
%                     RemainingBranches=obj.BranchNames     % just for testing
                    disp('All currents were received')
                    obj.Publisher;
                end
            end
            clear VARIABLES;
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 9
        
        function StatusReadinessGrid(obj)
            obj.AbstractResult.Type='Status';
            obj.AbstractResult.SimulationId=obj.SimulationId{1};
            obj.AbstractResult.SourceProcessId=obj.SourceProcessId;
            obj.MessageCounterOutbound=obj.MessageCounterOutbound+1;
                s = strcat('StateMonitoring',num2str(obj.MessageCounterOutbound));
            obj.AbstractResult.MessageId=s;
            obj.AbstractResult.EpochNumber=obj.Epoch;
            obj.AbstractResult.TriggeringMessageIds={obj.InboundMessage.MessageId};

            %%%%%

            if strcmp(obj.InboundMessage.Value,'ready')
%                     if (obj.ExpectedNumberOfVoltageValues==obj.NumberOfReceivedVoltageValues)
%                         if (obj.ExpectedNumberOfCurrentValues==obj.NumberOfReceivedCurrentValues)  % If Grid is ready, Then SM is ready. 
                obj.AbstractResult.Value='ready';
                obj.GridReadinessFlag=1;
                disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                disp('Grid is ready')
%                 disp(['SimulationId:' obj.SimulationId])
%                         end
%                     end
            end
            if strcmp(obj.InboundMessage.Value,'error')
                obj.AbstractResult.Value='error';
                obj.GridReadinessFlag=2;
                obj.AbstractResult.Description='Grid reported Error';
                disp('SM reported "error" message to Simulation Manager because an error occured on Grid')
%                 disp(['SimulationId:' obj.SimulationId])
            end
%                 if strcmp(obj.InboundMessage.Value,'ready')
%                     if (obj.ExpectedNumberOfVoltageValues~=obj.NumberOfReceivedVoltageValues)
%                         if (obj.ExpectedNumberOfCurrentValues==obj.NumberOfReceivedCurrentValues)
%                             obj.AbstractResult.Value='error';
%                             obj.AbstractResult.Description='Voltage values werenot received completely';
%                             disp('SM reported "error" message to Simulation Manager because Voltage values were missing')
%                             disp(['SimulationId:' obj.SimulationId])
%                         end
%                     end
%                 end
%                 if (strcmp(obj.InboundMessage.Value,'ready'))
%                     if (obj.ExpectedNumberOfVoltageValues==obj.NumberOfReceivedVoltageValues)
%                         if (obj.ExpectedNumberOfCurrentValues~=obj.NumberOfReceivedCurrentValues)
%                             obj.AbstractResult.Value='error';
%                             obj.AbstractResult.Description='Current values werenot received completely';
%                             disp('SM reported "error" message to Simulation Manager because Current values were missing')
%                             disp(['SimulationId:' obj.SimulationId])
%                         end
%                     end
%                 end
%                 if (strcmp(obj.InboundMessage.Value,'ready'))
%                     if (obj.ExpectedNumberOfVoltageValues~=obj.NumberOfReceivedVoltageValues)
%                         if (obj.ExpectedNumberOfCurrentValues~=obj.NumberOfReceivedCurrentValues)
%                             obj.AbstractResult.Value='error';
%                             obj.AbstractResult.Description='Neither Votage nor Current values were received completely';
%                             disp('SM reported "error" message to Simulation Manager because both Voltage and Current values were missing')
%                             disp(['SimulationId:' obj.SimulationId])
%                         end
%                     end
%                 end

            %%%%%

            if (obj.GridReadinessFlag)==2
                    t = datetime('now', 'TimeZone', 'UTC');
                    t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
                obj.AbstractResult.Timestamp=t;
                MyStringOut = java.lang.String(jsonencode(obj.AbstractResult));
                MyBytesOut = MyStringOut.getBytes(java.nio.charset.Charset.forName('UTF-8'));
                obj.AmqpConnector.sendMessage('Status.Error', MyBytesOut);
                clear t MyStringOut MyBytesOut
                obj.State='Stopped';
%                 elseif strcmp(obj.AbstractResult.Value,'ready')
%                         t = datetime('now', 'TimeZone', 'UTC');
%                         t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
%                     obj.AbstractResult.Timestamp=t;
%                     MyStringOut = java.lang.String(jsonencode(obj.AbstractResult));
%                     MyBytesOut = MyStringOut.getBytes(java.nio.charset.Charset.forName('UTF-8'));
%                     obj.AmqpConnector.sendMessage('Status.Ready', MyBytesOut);
%                     clear t MyStringOut MyBytesOut
            end
            if (obj.GridReadinessFlag)==1
                obj.SMreadiness;
            end
        end

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 10

        function Publisher(obj)
            if obj.VoltageReadinessFlag==1
                obj.AbstractResult.VoltageStatus=obj.VoltageStatus;
                obj.VoltageStatus=[];
%                obj.VoltageReadinessFlag=0;
                obj.AbstractResult.Type='DMSNetworkStatus.Voltage';
                obj.AbstractResult.SimulationId=obj.SimulationId{1};
                obj.AbstractResult.SourceProcessId=obj.SourceProcessId;
                obj.MessageCounterOutbound=obj.MessageCounterOutbound+1;
                    s = strcat('StateMonitoring',num2str(obj.MessageCounterOutbound));
                obj.AbstractResult.MessageId=s;
                obj.AbstractResult.EpochNumber=obj.Epoch;
                obj.AbstractResult.TriggeringMessageIds={obj.InboundMessage.MessageId};
                t = datetime('now', 'TimeZone', 'UTC');
                    t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
                obj.AbstractResult.Timestamp=t;
                MyStringOut = java.lang.String(jsonencode(obj.AbstractResult));
                MyBytesOut = MyStringOut.getBytes(java.nio.charset.Charset.forName('UTF-8'));
                obj.AmqpConnector.sendMessage('DMSNetworkStatus.Voltage', MyBytesOut);
                disp('Voltage status message was published')
                obj.AbstractResult=[];
                clear t MyStringOut MyBytesOut s
                obj.StatusPublishingFlag=obj.StatusPublishingFlag+1;
                obj.VoltageReadinessFlag=0;
            end
            if obj.CurrentReadinessFlag==1
                obj.AbstractResult.CurrentStatus=obj.CurrentStatus;
                obj.CurrentStatus=[];
%                obj.CurrentReadinessFlag=0;
                obj.AbstractResult.Type='DMSNetworkStatus.Current';
                obj.AbstractResult.SimulationId=obj.SimulationId{1};
                obj.AbstractResult.SourceProcessId=obj.SourceProcessId;
                obj.MessageCounterOutbound=obj.MessageCounterOutbound+1;
                    s = strcat('StateMonitoring',num2str(obj.MessageCounterOutbound));
                obj.AbstractResult.MessageId=s;
                obj.AbstractResult.EpochNumber=obj.Epoch;
                obj.AbstractResult.TriggeringMessageIds={obj.InboundMessage.MessageId};
                t = datetime('now', 'TimeZone', 'UTC');
                    t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
                obj.AbstractResult.Timestamp=t;
                MyStringOut = java.lang.String(jsonencode(obj.AbstractResult));
                MyBytesOut = MyStringOut.getBytes(java.nio.charset.Charset.forName('UTF-8'));
                obj.AmqpConnector.sendMessage('DMSNetworkStatus.Current', MyBytesOut);
                disp('Current status message was published')
                obj.AbstractResult=[];
                clear t MyStringOut MyBytesOut s
                obj.StatusPublishingFlag=obj.StatusPublishingFlag+1;
                obj.CurrentReadinessFlag=0;
            end
            if obj.StatusPublishingFlag==2
                obj.SMreadiness;
            end
        end 
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Method 11

        function SMreadiness(obj)
           SMIsReady=0;
            if obj.StatusPublishingFlag==2
               if obj.GridReadinessFlag==1
                   SMIsReady=1;
               end
            end
           if SMIsReady==1
               obj.AbstractResult.Type='Status';
               obj.InboundMessage.Value='ready';
               obj.AbstractResult.SimulationId=obj.SimulationId{1};
               obj.AbstractResult.SourceProcessId=obj.SourceProcessId;
               obj.MessageCounterOutbound=obj.MessageCounterOutbound+1;
                   s = strcat('StateMonitoring',num2str(obj.MessageCounterOutbound));
               obj.AbstractResult.MessageId=s;
               obj.AbstractResult.EpochNumber=obj.Epoch;
               obj.AbstractResult.TriggeringMessageIds={obj.InboundMessage.MessageId};
                   t = datetime('now', 'TimeZone', 'UTC');
                   t=datestr(t,'yyyy-mm-ddTHH:MM:ss.FFFZ');
               obj.AbstractResult.Timestamp=t;
               MyStringOut = java.lang.String(jsonencode(obj.AbstractResult));
               MyBytesOut = MyStringOut.getBytes(java.nio.charset.Charset.forName('UTF-8'));
               obj.AmqpConnector.sendMessage('Status.Ready', MyBytesOut);
               clear s t MyStringOut MyBytesOut
               obj.AbstractResult=[];
               disp('StateMonitoring is ready')
           end
           clear SMIsReady;
        end
    end
end

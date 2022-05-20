function ManagementCallback(hObject, eventData)
   global NumOfSimRun
   global Handles
   global States
   global SimulationId
   
   mystr = java.lang.String(eventData.message, 'UTF-8');
   str = char(mystr);  %    Making the input into a character array
   InboundMessage = jsondecode(str); % decoding JSON data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if strcmp(InboundMessage.Type,'Start')
        if NumOfSimRun==0
            NumOfSimRun=NumOfSimRun+1;      
            StateMonitoingBlock=InboundMessage.ProcessParameters.StateMonitoring;
            SimulationSpecificExchange=InboundMessage.SimulationSpecificExchange;
            SimulationId(NumOfSimRun)=cellstr(InboundMessage.SimulationId);

            fields = fieldnames(StateMonitoingBlock);
            SMName = fields{1,1};

            Grid=StateMonitoingBlock.(SMName).MonitoredGridName;
            MaxVoltage=StateMonitoingBlock.(SMName).MaxVoltage;
            MinVoltage=StateMonitoingBlock.(SMName).MinVoltage;
            UpperAmberBandVoltage=StateMonitoingBlock.(SMName).UpperAmberBandVoltage;
            LowerAmberBandVoltage=StateMonitoingBlock.(SMName).LowerAmberBandVoltage;
            OverloadingBaseline=StateMonitoingBlock.(SMName).OverloadingBaseline;
            AmberLoadingBaseline=StateMonitoingBlock.(SMName).AmberLoadingBaseline;

            Object(NumOfSimRun)=StateMonitoring(SimulationSpecificExchange,SimulationId(NumOfSimRun),SMName,Grid,MaxVoltage,MinVoltage,UpperAmberBandVoltage,LowerAmberBandVoltage,OverloadingBaseline,AmberLoadingBaseline);
%             Handles{NumOfSimRun} = @() Object(NumOfSimRun).Main;
%             States{NumOfSimRun}=parfeval(@() Object.Main,1);
            Object(NumOfSimRun).Main
        else
            sum=0;
            for i=1:NumOfSimRun % to assure that start message is for starting up a new simulation run not resending the start message to awake a component
                tf=strcmp(char(SimulationId(i)),InboundMessage.SimulationId);
                sum=sum+tf;
            end
                if sum==0
                    NumOfSimRun=NumOfSimRun+1;
                    StateMonitoingBlock=InboundMessage.ProcessParameters.StateMonitoring;
                    SimulationSpecificExchange=InboundMessage.SimulationSpecificExchange;
                    SimulationId(NumOfSimRun)=cellstr(InboundMessage.SimulationId);

                    fields = fieldnames(StateMonitoingBlock);
                    SMName = fields{1,1};

                    Grid=StateMonitoingBlock.(SMName).MonitoredGridName;
                    MaxVoltage=StateMonitoingBlock.(SMName).MaxVoltage;
                    MinVoltage=StateMonitoingBlock.(SMName).MinVoltage;
                    UpperAmberBandVoltage=StateMonitoingBlock.(SMName).UpperAmberBandVoltage;
                    LowerAmberBandVoltage=StateMonitoingBlock.(SMName).LowerAmberBandVoltage;
                    OverloadingBaseline=StateMonitoingBlock.(SMName).OverloadingBaseline;
                    AmberLoadingBaseline=StateMonitoingBlock.(SMName).AmberLoadingBaseline;

                    Object(NumOfSimRun)=StateMonitoring(SimulationSpecificExchange,SimulationId(NumOfSimRun),SMName,Grid,MaxVoltage,MinVoltage,UpperAmberBandVoltage,LowerAmberBandVoltage,OverloadingBaseline,AmberLoadingBaseline);
%                     Handles{NumOfSimRun} = @() Object(NumOfSimRun).Main;
%                     States{NumOfSimRun}=parfeval(@() Object.Main,1);
                    Object(NumOfSimRun).Main
                end  
        end       
    end
end
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% InboundMessage.SimulationSpecificExchange='simexe30';
% InboundMessage.SimulationId='SimTest30';
% 
% InboundMessage.StateMonitoring.MonitoredGridName='Grid';
% InboundMessage.StateMonitoring.MaxVoltage=1.05;
% InboundMessage.StateMonitoring.MinVoltage=0.95;
% InboundMessage.StateMonitoring.UpperAmberBandVoltage=0.01;
% InboundMessage.StateMonitoring.LowerAmberBandVoltage=0.01;
% InboundMessage.StateMonitoring.OverloadingBaseline=1;
% InboundMessage.StateMonitoring.AmberloadingBaseline=0.1;
% 
% NumOfSimRun=1;
% Object(NumOfSimRun)=StateMonitoring(InboundMessage.SimulationSpecificExchange,InboundMessage.SimulationId,InboundMessage.StateMonitoring.MonitoredGridName,InboundMessage.StateMonitoring.MaxVoltage,InboundMessage.StateMonitoring.MinVoltage,InboundMessage.StateMonitoring.UpperAmberBandVoltage,InboundMessage.StateMonitoring.LowerAmberBandVoltage,InboundMessage.StateMonitoring.OverloadingBaseline,InboundMessage.StateMonitoring.AmberloadingBaseline);   
% 
% % InboundMessage.SimulationSpecificExchange='simexe31';
% % InboundMessage.SimulationId='SimTest31';
% % NumOfSimRun=2;
% % Object(NumOfSimRun)=StateMonitoring(InboundMessage.SimulationSpecificExchange,InboundMessage.SimulationId);   
% 
% parfor i=1:NumOfSimRun
%     Object(i).Main;
% end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% function ManagementCallback(hObject, eventData)
%    global NumOfSimRun
%    global Handles
%    global States
%    
%    mystr = java.lang.String(eventData.message, 'UTF-8');
%    str = char(mystr);  %    Making the input into a character array
%    InboundMessage = jsondecode(str); % decoding JSON data
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     if strcmp(InboundMessage.Type,'Start')
%         if NumOfSimRun==0 
%         NumOfSimRun=NumOfSimRun+1
%         StateMonitoingBlock=InboundMessage.ProcessParameters.StateMonitoring
%         SimulationSpecificExchange=InboundMessage.SimulationSpecificExchange;
%         SimulationId=InboundMessage.SimulationId;
% 
%         fields = fieldnames(StateMonitoingBlock)
%         GridName = fields{1,1}
%         
%         Grid=StateMonitoingBlock.(GridName).MonitoredGridName;
%         MaxVoltage=StateMonitoingBlock.(GridName).MaxVoltage;
%         MinVoltage=StateMonitoingBlock.(GridName).MinVoltage;
%         UpperAmberBandVoltage=StateMonitoingBlock.(GridName).UpperAmberBandVoltage;
%         LowerAmberBandVoltage=StateMonitoingBlock.(GridName).LowerAmberBandVoltage;
%         OverloadingBaseline=StateMonitoingBlock.(GridName).OverloadingBaseline;
%         AmberLoadingBaseline=StateMonitoingBlock.(GridName).AmberLoadingBaseline;
% 
%         Object(NumOfSimRun)=StateMonitoring(SimulationSpecificExchange,SimulationId,GridName,Grid,MaxVoltage,MinVoltage,UpperAmberBandVoltage,LowerAmberBandVoltage,OverloadingBaseline,AmberLoadingBaseline);
% %       Handles{NumOfSimRun} = @() Object(NumOfSimRun).Main
% %         States{NumOfSimRun}=parfeval(@() Object.Main,1)
%         parfor i=1:NumOfSimRun
%             Object(i).Main;
%         end
%         end
%     end
% end



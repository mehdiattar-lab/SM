**StateMonitoring (SM)**

Author:

> Mehdi Attar
>
> Tampere University
>
> Finland

**Introduction**

One of the distribution management system's (DMS) application systems resposible for monitoring of the grid's state in real-time.

The component is only deployable in the [SimCES ](https://simcesplatform.github.io/)platform as an [externaly managed component](https://simcesplatform.github.io/core_workflow-start-end/#externally-managed-components).

**Workflow of the SM.**

**1**- In the first epoch, NIS component in the SimCES environment publishes the network information system ([NIS](https://simcesplatform.github.io/energy_msg-init-nis-networkcomponentinfo/)) and CIS publishes customer information system ([CIS](https://simcesplatform.github.io/energy_msg-init-cis-customerinfo/)) to the RabbitMQ broker topics "Init.NIS.#" and "Init.CIS.CustomerInfo" respectively. By listening to the topics, SM has access to NIS and CIS data.

2- SM analyse the grid flows (i.e., [voltage ](https://simcesplatform.github.io/energy_msg-networkstate-voltage/)and [current](https://simcesplatform.github.io/energy_msg-networkstate-current/)) according to the network limitations (NIS data), and discovers any probable network congestions.

**Requirements**

Matlab R2020a (has not been tested with versions other than R2020a)

Java: JDK/JRE 8 or newer

Matlab- rabbitmq connection:

To connect Matlab and RabbitMQ please visit the following page:

https://kannisto.github.io/Cocop.AmqpMathToolConnector

https://github.com/simcesplatform/AmqpMathToolIntegration

The following libraries were utilised in development. Therefore, all of the libraries should be downloaded and utilized based on instructions given in above webpages [1](https://kannisto.github.io/Cocop.AmqpMathToolConnector) and [2](https://github.com/simcesplatform/AmqpMathToolIntegration)

amqp-client-4.2.2.jar

amqp-client-4.2.2-javadoc.jar

commons-logging-1.2.jar

slf4j-api-1.7.25.jar

slf4j-nop-1.7.25.jar

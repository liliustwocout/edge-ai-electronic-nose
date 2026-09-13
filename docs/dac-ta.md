Advantech AIoT InnoWorks - Project Information: Team
Team Name TaskForce141 No. of Team Members 3
Project Topic Edge AI-Based Electronic Nose for Hydrogen Sulfide Leak Detection in Natural Gas Processing Plants Adviser Dr. Nguyen Dac Cu
Member background (department) 1. Do Duc Khoi - Lead
2. Le Pham Thanh Dat - Member
3. Vu Anh Kiet - Member
Project introduction

For example:
The target audience of the project, the issue want to be resolved and the expected benefits of the project This project proposes an AIoT-based Electronic Nose (E-Nose) system for the early detection and prediction of hydrogen sulfide (H₂S) leak events in oil and gas processing plants. Inspired by the biological olfactory system, the proposed electronic nose employs an array of gas sensors and environmental sensors to capture characteristic gas signatures associated with normal operating conditions and potential H₂S leakage scenarios.
The system consists of multiple ESP32-based sensor nodes deployed throughout the facility. Each node continuously measures H₂S concentration together with environmental parameters such as temperature and humidity. The collected data are transmitted through an industrial Modbus RS-485 communication network to a Raspberry Pi 5 edge gateway.
Acting as the central intelligence unit of the system, the Raspberry Pi 5 performs Modbus RTU Master communication, data acquisition, local database management, and Edge AI inference. During the data collection phase, H₂S measurements, environmental parameters, timestamps, and node identifiers are continuously recorded and stored locally. The collected data are subsequently synchronized with the WISE-IoT platform to support remote monitoring, visualization, and long-term data storage.
The recorded dataset is used to construct labeled samples representing normal operating conditions and various H₂S leak scenarios. Based on this dataset, machine learning models are developed to classify environmental conditions and predict potential gas leakage events. After model optimization, the trained models are converted into TensorFlow Lite format and deployed on the Raspberry Pi 5 gateway for edge inference.
The Raspberry Pi 5 performs real-time data preprocessing, feature extraction, model inference, and risk assessment at the network edge. Instead of relying solely on fixed concentration thresholds, the Edge AI model analyzes temporal gas patterns and environmental conditions to identify abnormal behavior and predict potential leak events before critical safety limits are reached. The prediction results are categorized into multiple risk levels, including Normal, Warning, Hazardous, and Emergency.
The inference results, event logs, and system status are transmitted to the WISE-IoT platform via MQTT for real-time visualization and notification services. Plant operators can access the monitoring dashboard to observe H₂S concentration trends, review historical data, and receive predictive early warning notifications whenever abnormal conditions are detected.
Please provide the functional/system diagram of the project and briefly describe how Edge AI / Edge Computing will be utilized in the project?
  
System Architecture Description
The proposed Electronic Nose (E-Nose) system for gas leak monitoring and predictive early warning is organized into 5 layers: Electronic Nose Sensor Layer, Communication Layer, Edge Computing Layer, Cloud Platform Layer, and Application Layer.
System Architecture Description
The proposed Electronic Nose (E-Nose) system for hydrogen sulfide (H₂S) leak monitoring and predictive early warning is organized into five layers: Perception Layer, Communication Layer, Edge Computing Layer, Cloud Platform Layer, and Application Layer.

1. Perception Layer
The Perception Layer is responsible for sensing, preprocessing, and transmitting environmental data from various monitoring locations within the natural gas processing plant.
Each Electronic Nose (E-Nose) node is built around an ESP32 microcontroller and integrates multiple sensing elements, including:
• ZE03-H₂S sensor for hydrogen sulfide (H₂S) detection.
• MQ136 sensor for cross-sensitive H₂S gas monitoring and gas pattern recognition.
• Temperature and humidity sensor for environmental compensation and sensor calibration.
Unlike conventional gas monitoring systems that rely on a single gas detector, the proposed Electronic Nose combines multiple sensing elements to capture characteristic gas signatures and environmental patterns associated with normal operating conditions and potential H₂S leak events.
The ESP32 continuously acquires sensor measurements and performs basic preprocessing tasks such as signal filtering and conditioning before transmitting the data to the gateway.
The primary functions of the E-Nose node include:
• Real-time H₂S concentration monitoring.
• Temperature and humidity measurement.
• Signal conditioning and filtering.
• Timestamp generation.
• Node identification management.
• Data packaging into Modbus RTU frames.
• Modbus RTU Slave communication.
Multiple E-Nose nodes can be deployed near pipelines, compressors, storage tanks, and gas treatment units to provide distributed monitoring coverage throughout the facility.
2. Communication Layer
The Communication Layer is responsible for transmitting sensing data between distributed Electronic Nose nodes and the edge gateway.
The communication infrastructure is based on RS-485 industrial communication using the Modbus RTU protocol.
Key advantages include:
• Long-distance communication capability.
• High reliability in industrial environments.
• Strong immunity to electromagnetic interference.
• Multi-drop network architecture supporting multiple sensor nodes.
• Low implementation cost and easy scalability.
The Raspberry Pi 5 acts as a Modbus RTU Master, while each Electronic Nose node operates as a Modbus RTU Slave with a unique node address.
This layer ensures reliable and efficient transmission of gas sensing data from distributed monitoring locations to the edge computing platform.
3. Edge Computing Layer
The Edge Computing Layer is implemented using a Raspberry Pi 5 and serves as the local processing and decision-making unit of the proposed system.
The Raspberry Pi 5 performs the following functions:
• Modbus RTU Master communication.
• Data collection from all Electronic Nose nodes.
• Local database storage.
• Data preprocessing and feature extraction.
• Edge AI model execution.
• Event logging and risk assessment.
• MQTT communication with the cloud platform.
The Raspberry Pi 5 continuously receives H₂S concentration measurements and environmental data from all Electronic Nose nodes through the RS-485 network.
During the data acquisition phase, sensor readings from the ZE03-H₂S sensor, MQ136 sensor, temperature and humidity sensor, together with timestamps and node identifiers, are stored locally to build a gas sensing dataset representing various operating conditions.
The Edge Computing Layer performs local processing tasks such as signal filtering, feature extraction, data aggregation, and anomaly screening before transmitting relevant information to the cloud platform.
Machine learning models are deployed directly on the Raspberry Pi 5 to enable Edge AI capabilities. The Edge AI module performs:
• Real-time gas pattern recognition.
• H₂S leak detection.
• Environmental condition classification.
• Anomaly detection.
• Risk level prediction.
Instead of relying solely on predefined concentration thresholds, the model analyzes the relationships among H₂S concentration, cross-sensitive sensor responses, temperature, and humidity to identify abnormal situations and predict potential leak events at an earlier stage.
The prediction output is classified into four risk levels:
• Normal.
• Warning.
• Hazardous.
• Emergency.
By executing data processing and AI inference locally, the Edge Computing Layer achieves low-latency decision making, reduces communication bandwidth requirements, minimizes cloud dependency, and maintains continuous operation even during network interruptions.
4. Cloud Platform Layer
The Cloud Platform Layer is implemented using the WISE-IoT platform and provides centralized monitoring, data management, and long-term storage services.
Its main functions include:
• Historical data storage.
• Real-time dashboard visualization.
• Device management.
• Alarm management.
• Trend analysis.
• Report generation.
• Remote system monitoring.
The Raspberry Pi 5 gateway communicates with the WISE-IoT platform using MQTT over Ethernet or Wi-Fi networks.
The cloud platform receives sensor measurements, Edge AI prediction results, event logs, and system status information from the gateway. It also provides long-term data storage for future analysis and model improvement.
5. Application Layer
The Application Layer provides an interface for plant operators, maintenance engineers, and safety personnel to access monitoring information and system status.
Users can access the system through a web-based dashboard provided by the WISE-IoT platform.
The dashboard provides:
• Real-time H₂S concentration monitoring.
• Edge AI prediction results.
• Risk level visualization.
• Historical trend analysis.
• Alarm notifications.
• Device status monitoring.
• Event log visualization.
This interface enables operators to observe gas concentration changes, identify abnormal situations, evaluate potential risks, and respond proactively before hazardous conditions occur.
The Application Layer supports informed decision-making and enhances operational safety within natural gas processing facilities.
Edge AI and Edge Computing Utilization
The proposed system leverages Edge Computing and Edge AI by deploying machine learning models directly on the Raspberry Pi 5 gateway rather than relying entirely on cloud-based processing.
Sensor data collected from distributed Electronic Nose nodes are processed locally at the edge. The Raspberry Pi 5 performs data filtering, feature extraction, and TensorFlow Lite model inference in real time. The Edge AI model analyzes methane and hydrogen sulfide concentration patterns to detect anomalies, classify risk levels, and predict potential gas leakage events.
By performing inference locally, the system significantly reduces response latency, minimizes network bandwidth usage, and maintains continuous operation during network interruptions. The Edge AI architecture also improves system reliability and enables predictive early warning capabilities, allowing plant operators to take preventive actions before gas concentrations reach critical safety thresholds.

Project Timeline and Work Plan

Phase Duration Main Tasks Deliverables
Phase 1 Week 1–2 Requirement Analysis and Literature Review System Requirements Specification
Phase 2 Week 3–4 Electronic Nose Hardware Design Circuit Schematic and Prototype Design
Phase 3 Week 5–6 Sensor Node Development ESP32-Based E-Nose Node
Phase 4 Week 7–8 Edge Gateway Development Raspberry Pi 5 Gateway Software
Phase 5 Week 9–11 Dataset Collection and Storage H2S Dataset
Phase 6 Week 12–13 AI Model Development and Training Trained Machine Learning Model
Phase 7 Week 14 TinyML Deployment and Optimization Edge AI Model on Raspberry Pi 5
Phase 8 Week 15 System Integration Complete AIoT System
Phase 9 Week 16 Testing and Performance Evaluation Final System Validation Report

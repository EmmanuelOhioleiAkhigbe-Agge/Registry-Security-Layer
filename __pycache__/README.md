# Windows Registry Security Layer

A Python-based defensive security prototype designed to monitor Windows Registry changes, analyze their potential risk, and record security events.

The project combines rule-based security analysis with a machine-learning classifier to provide an additional layer of visibility into potentially suspicious registry activity.

---

## Project Overview

The Windows Registry stores important configuration information used by Windows and installed applications.

Because registry modifications can be associated with legitimate configuration changes as well as suspicious activity, this project explores how an external security layer can continuously monitor registry changes and assess their potential risk.

The current prototype focuses on safe monitoring of a controlled registry test location.

### Core workflow

Windows Registry  
↓  
Registry Monitor  
↓  
Change Detection  
↓  
Security Engine  
↙                 ↘  
Rule Analysis       Machine Learning  
↘                 ↙  
Risk Assessment  
↓  
Security Decision  
↓  
Event Logging

---

## Features

### Registry Monitoring

The system continuously monitors a designated Windows Registry test location.

Current test location:

`HKCU\Software\RegistrySecurityTest_New`

The monitor detects:

- Added values
- Modified values
- Removed values

---

### Rule-Based Risk Analysis

The security engine examines registry changes for potentially suspicious indicators.

Examples include:

- PowerShell-related activity
- Commands
- Scripts
- Shell activity
- Startup-related changes
- Run-related activity

A numerical risk score from `0` to `100` is generated.

Current classifications:

| Risk Score | Classification |
|---|---|
| 0–39 | LOW RISK |
| 40–69 | SUSPICIOUS |
| 70–100 | HIGH RISK |

---

### Machine-Learning Analysis

The project also uses a machine-learning classifier based on:

- TF-IDF text feature extraction
- Logistic Regression

The model analyzes information about the registry change and produces:

- A predicted classification
- A confidence value

The machine-learning component is intended as an additional analytical signal rather than a replacement for security rules.

---

### Security Decision Layer

The system converts the security classification into an operational decision.

#### LOW RISK

The event is logged as normal activity.

#### SUSPICIOUS

The event is flagged for review.

#### HIGH RISK

A security alert is generated recommending investigation.

The current prototype does **not automatically block registry changes**.

---

### Security Event Logging

Live registry events are stored separately from the machine-learning training dataset.

Live events are recorded in:

`security_events.csv`

Each event contains:

- Change type
- Registry value name
- Previous value
- New value
- Risk score
- Classification

Example:

```text
modified,TestValue,Safe,Normal User Setting,10,LOW RISK

Suspicious example:

modified,TestValue,Safe,PowerShell Encoded Script,70,HIGH RISK
Machine-Learning Dataset

The training dataset is stored separately:

security_dataset.csv

This separation prevents live monitoring events from automatically becoming training data.

The current dataset is synthetic and was created specifically for development and testing.

Therefore, the reported model performance should not be interpreted as real-world malware-detection accuracy.

Project Structure
Registry-Security-Layer/
│
├── main.py
├── registry_monitor.py
├── security_engine.py
├── security_events.py
├── system_monitor.py
│
├── train_model.py
├── test_model.py
├── explain_prediction.py
├── generate_training_data.py
│
├── security_dataset.csv
├── security_events.csv
│
└── README.md
Technologies
Python
Windows Registry API (winreg)
Windows Management Instrumentation (WMI)
Pandas
Scikit-learn
TF-IDF
Logistic Regression
CSV-based event logging
Installation

Clone the repository and open the project directory.

Install the required Python packages:

pip install pandas scikit-learn WMI

The project is designed for Windows because it uses Windows-specific registry and system APIs.

Running the Registry Monitor

Start the monitoring system:

python registry_monitor.py

The program monitors:

HKCU\Software\RegistrySecurityTest_New

The monitor checks the registry periodically for changes.

Testing

The project uses a controlled registry key so that testing does not require modifying important Windows registry locations.

Normal test

A normal configuration change can be used to produce a low-risk event.

Suspicious test

A controlled test value containing terms such as:

PowerShell Encoded Script

can be used to demonstrate the detection and classification pipeline.

These tests are performed only against the project's designated test registry location.

Example Result

A monitored change can produce output similar to:

Registry change:
Changed value TestValue from Safe to PowerShell Encoded Script

Rule-based analysis:
Risk score: 70 / 100
Classification: HIGH RISK

Machine-learning analysis:
Prediction: HIGH RISK
Confidence: 76.98%

Security decision:
SECURITY ALERT: High-risk registry activity detected.
Manual investigation recommended.

The event is then recorded in:

security_events.csv
Architecture

The prototype is divided into several components.

registry_monitor.py

Responsible for:

Reading registry values
Creating the controlled test key
Detecting changes
Sending changes to the security engine
security_engine.py

Responsible for:

Rule-based risk calculation
Machine-learning prediction
Confidence calculation
Security classification
Security decisions
Sending events to the event logger
security_events.py

Responsible for:

Recording live security events
Maintaining the separate event log
system_monitor.py

Provides system/process information through Windows Management Instrumentation.

Machine-Learning Scripts

The project also contains separate scripts for:

Generating development data
Training the model
Testing predictions
Explaining detected indicators
Current Limitations

This project is a research and development prototype.

It currently does not provide:

Kernel-level registry protection
Automatic blocking of registry modifications
Guaranteed attribution of every registry change to a specific process
Production-grade malware detection
Protection against kernel-level attacks
Enterprise-scale event collection

The current registry monitoring system operates on a controlled user-level test location.

The machine-learning dataset is synthetic and relatively small, so model performance should not be interpreted as evidence of production security effectiveness.

Future Development

Potential future research directions include:

Process-aware registry event attribution
Windows event tracing integration
More sophisticated behavioral analysis
Registry integrity monitoring
Trusted configuration baselines
Automated rollback and recovery mechanisms
Privileged Windows service architecture
Advanced anomaly detection
Larger real-world security datasets
Deeper Windows security and kernel-level integration
Research Motivation

The project explores the concept of placing an independent security analysis layer between operating-system configuration changes and security decision-making.

Rather than relying exclusively on static security rules, the proposed architecture combines:

Continuous monitoring
Rule-based analysis
Machine-learning classification
Risk scoring
Explainable indicators
Security event logging

The long-term research direction is to investigate whether these techniques can improve the detection and analysis of suspicious registry behavior while minimizing unnecessary computational overhead and false alerts.

Safety

All current experiments are performed using a dedicated test registry location:

HKCU\Software\RegistrySecurityTest_New

The prototype does not intentionally modify Windows system registry locations or automatically block system activity.

Project Status

Version 1 — Prototype Complete

Current implementation includes:

Registry monitoring
Change detection
Rule-based risk scoring
Machine-learning classification
Security decision layer
Live event logging
Separate training and live-event datasets
Author

Emmanuel Ohiolei Akhigbe-Agge

Computer Science / Cybersecurity Research Portfolio
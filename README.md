**Overview**

The HK.py script is a Python-based automation tool designed to perform health checks on a set of network devices managed through a VMM (Virtual Machine Manager). It collects critical diagnostic information from the devices, including interface statuses, system alarms, chassis information, and core dumps, providing detailed insights into the state of the infrastructure.

This script dynamically retrieves device IPs using the vmm utility, connects to each device via SSH, executes a series of CLI commands, and saves the outputs to a timestamped file for further analysis.

**Features""

- Dynamic Device IP Retrieval: Automatically fetches the IP addresses of target devices using the vmm utility.
- Secure SSH Access: Connects to devices securely using paramiko.
- Customizable Commands: Executes predefined CLI commands to collect device diagnostics.
- Error Handling: Logs connection failures or errors for troubleshooting.
- Timestamped Outputs: Saves health check results to a uniquely named output file for easy identification.

**Prerequisites**

Python Environment:
  Python 3.x installed.
  Required modules: paramiko, subprocess, and re.

VMM CLI Utility:
  The vmm command-line tool must be available and configured on the system.

Device Credentials:
  Ensure you have valid SSH credentials for the target devices.

Network Access:
  The server running the script must have network access to the target devices.

Run the script - python3 HK.py

Outputs - cat vmm_health_check_YYYY-MM-DD_HH-MM-SS.txt

![image](https://github.com/user-attachments/assets/d964ddf7-ff16-4d92-8155-4c1fa38508a1)

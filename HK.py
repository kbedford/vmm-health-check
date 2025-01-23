import paramiko
import subprocess
import re
import os
from datetime import datetime

# List of target devices
TARGET_DEVICES = [
    "PTX1_1_RE0", "PTX2_2_RE0", "PTX3_3_RE0", "PTX4_4_RE0",
    "vMX1_RE", "vMX2_RE", "vMX3_RE", "vMX4_RE", "vRR1_RE", "vRR2_RE"
]

# CLI commands to execute
commands = [
    "show interfaces terse",
    "show chassis routing-engine",
    "show version",
    "show chassis fpc",
    "show system alarms",
    "show system core-dumps"
]

# Function to grab VMM IPs dynamically
def get_vmm_ips():
    try:
        vmm_output = subprocess.check_output(["vmm", "ip"], text=True)
        # Extract device names and their corresponding IPs
        ip_pattern = re.compile(r"(\S+)\s+((?:\d{1,3}\.){3}\d{1,3})")
        matches = ip_pattern.findall(vmm_output)
        return {device: ip for device, ip in matches if device in TARGET_DEVICES}
    except Exception as e:
        print(f"Failed to retrieve VMM IPs: {str(e)}")
        return {}

# Function to execute CLI commands via SSH
def execute_cli_commands(ip, username, password, commands):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password, timeout=10)

        # Start a shell session
        shell = ssh.invoke_shell()
        buffer_size = 2048  # Increase buffer size for large outputs

        # Switch to CLI mode
        shell.send("cli\n")
        while True:
            if shell.recv(buffer_size).decode("utf-8").strip().endswith(">"):
                break

        # Disable pagination
        shell.send("set cli screen-length 0\n")
        shell.send("set cli screen-width 0\n")
        while True:
            if shell.recv(buffer_size).decode("utf-8").strip().endswith(">"):
                break

        results = []
        for command in commands:
            shell.send(f"{command}\n")
            output = ""
            while True:
                chunk = shell.recv(buffer_size).decode("utf-8")
                output += chunk
                if chunk.strip().endswith(">"):
                    break
            results.append(f"--- {command} ---\n{output.strip()}\n")

        ssh.close()
        return "\n".join(results)
    except Exception as e:
        return f"Error connecting to {ip}: {str(e)}"

# Main function
if __name__ == "__main__":
    # Define device credentials
    username = "root"
    password = "Embe1mpls"

    # Retrieve the VMM IP addresses for target devices
    device_ips = get_vmm_ips()

    if not device_ips:
        print("No valid target devices found. Exiting.")
        exit()

    print(f"Retrieved target devices and IPs: {device_ips}")

    # Create an output file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"vmm_health_check_{timestamp}.txt"

    # Open the output file
    with open(output_file, "w") as file:
        # Iterate through each target device
        for device, ip in device_ips.items():
            print(f"\nConnecting to {device} ({ip})...")
            results = execute_cli_commands(ip, username, password, commands)

            # Write the results for this device to the file
            if "Error connecting" not in results:
                file.write(f"=== Device: {device} ({ip}) ===\n")
                file.write(results)
                file.write("\n\n")
                print(f"Results for {device} saved.")
            else:
                file.write(f"=== Device: {device} ({ip}) ===\n")
                file.write(results)
                file.write("\n\n")
                print(f"Failed to retrieve data from {device}: {results}")

    print(f"\nHealth-check completed. All outputs saved in {output_file}.")


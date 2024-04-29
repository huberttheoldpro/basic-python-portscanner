import ping3
import socket
import time
import concurrent.futures
import os

def ping_host(host):
    result = ping3.ping(host)
    if result is not None:
        print(f"{host} is reachable. Round-trip time: {result} ms")
    else:
        print(f"Failed to ping {host}")

def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  #As this only scans 1 port you can set a higher timout here
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} is open")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
    finally:
        sock.close()

def scan_ports(host, ports):
    print(f"Scanning ports for {host}...")
    num_cpus = os.cpu_count() or 1
    num_threads_used = input(f"You have {num_cpus} threads at your disposal. How many would you like to allocate to scanning? ")

    
    while not num_threads_used.isdigit():
        num_threads_used = input("Please enter a valid number: ")

    num_threads_used = int(num_threads_used)

    #CPU usage protection module that isn't rlly a module
    if num_threads_used < 1 or num_threads_used > num_cpus:
        print(f"Invalid number of threads. Please enter a number between 1 and {num_cpus}.")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads_used) as executor:
        futures = [executor.submit(scan_port, host, port) for port in ports]
        concurrent.futures.wait(futures)
        timout = input("You now have the reults above if there are none than no ports are open in the range specified, press enter again to end the running of this code")




target_host = "google.com"
ping_host(target_host)
scan_ports(target_host, range(1, 1025))  #Most common ports will be bellow


#This code will NOT function correctly if you have a strict firewall or limitations on sending ICMP echo packets #type:ignore

#common ports
#ports 1-1023  Ports in the range 0-1023 are reserved for well-known services and protocols defined by the Internet Assigned Numbers Authority (IANA) #type:ignore
#ports 1023-49151  Ports in the range 1024-49151 are registered ports, which means they can be used by specific applications and services upon registration with IANA. These are mainly NAS servers, databases and Game servers (multiplayer) #type:ignore
#ports 49152-65535  Ports in the range 49152-65535 are dynamic or private ports, which means they are not assigned to any specific service or application, these ports are available for use by client applications and are typically used for outgoing connections. #type:ignore

#website of common ports used
#https://www.geeksforgeeks.org/50-common-ports-you-should-know/

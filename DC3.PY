# Experiment 3: Implement Group Communication
import socket
import struct
import threading
import time
import sys

# Configuration
MULTICAST_GROUP = '224.1.1.1'
PORT = 5007

def receive():
    """Background thread function to listen for multicast messages."""
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    # Allow multiple applications to use the same port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to the port
    sock.bind(('', PORT))
    
    # Construct the membership request
    # '4s4s' represents two 4-byte sequences: Group IP and Interface IP (0.0.0.0)
    group = socket.inet_aton(MULTICAST_GROUP)
    mreq = struct.pack('4s4s', group, socket.inet_aton('0.0.0.0'))
    
    # Join the multicast group
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    print(f"--- Receiver ready on {MULTICAST_GROUP}:{PORT} ---")
    
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            print(f"\n[Received from {addr}]: {data.decode()}")
            # Re-print prompt to keep UI clean
            print("Enter message (or 'exit' to quit): ", end="", flush=True)
    except Exception as e:
        print(f"\nReceiver error: {e}")
    finally:
        sock.close()

def send():
    """Main thread function to send multicast messages."""
    # Small delay to let the receiver thread initialize its print statements
    time.sleep(0.5)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    # Set the Time-to-Live (TTL). 1 = Local Network only.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    
    print("--- Sender initialized ---")
    
    try:
        while True:
            msg = input("Enter message (or 'exit' to quit): ")
            
            if msg.lower() == 'exit':
                print("Shutting down...")
                break
                
            if msg.strip():
                sock.sendto(msg.encode('utf-8'), (MULTICAST_GROUP, PORT))
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()

if __name__ == "__main__":
    # 1. Start the receiver in the background (daemon)
    # Daemon threads automatically exit when the main thread stops
    receiver_thread = threading.Thread(target=receive, daemon=True)
    receiver_thread.start()
    
    # 2. Run the sender in the foreground
    send()
    
    print("Program terminated.")
    sys.exit()
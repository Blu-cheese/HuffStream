import socket
import os
import sys
import time
import subprocess

# Add the parent directory to sys.path to import the utils module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.huffman import encode_data

# Configuration variables
SERVER_IP = "172.20.10.4"  # Server IP address
PORT = 9999               # Server port
FILE_PATH = "sending_files/sample.txt"   # Path of the file to send

def send_encoded_file(host, port, file_path):
    """Encode a file using Huffman coding and send it to the server."""
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        print(f"Connecting to {host}:{port}...")
        client_socket.connect((host, port))
        
        # Read the file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Encode the data in memory
        print(f"Encoding file using Huffman coding...")
        encoded_data, compression_ratio = encode_data(file_data)
        
        # Get the filename for the encoded version
        filename = os.path.basename(file_path)
        base_name, ext = os.path.splitext(filename)
        encoded_filename = f"{base_name}_encoded{ext}"
        
        # Send encoded filename and filesize
        filesize = len(encoded_data)
        file_info = f"{encoded_filename}|{filesize}"
        client_socket.send(file_info.encode('utf-8'))
        
        # Wait briefly to ensure server is ready
        time.sleep(0.1)
        
        # Send the encoded data
        print(f"Sending encoded file {encoded_filename} ({filesize} bytes)...")
        client_socket.sendall(encoded_data)
        
        print(f"\nEncoded file sent successfully (compression ratio: {compression_ratio:.2f}%)")
        
        # Receive acknowledgment from server
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Check if the file exists
    if not os.path.exists(FILE_PATH):
        print(f"Error: File '{FILE_PATH}' not found")
        sys.exit(1)
    
    print(f"Server: {SERVER_IP}:{PORT}")
    print(f"File: {FILE_PATH}")
    
    # Send the encoded file
    success = send_encoded_file(SERVER_IP, PORT, FILE_PATH)
    
    if not success:
        print("Failed to send encoded file to server.")

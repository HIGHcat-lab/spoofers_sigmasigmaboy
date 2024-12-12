import socket
import os
import time

file_path = "woofer.py"
if os.path.exists(file_path):
    os.remove(file_path)
else:
    print("The file does not exist")



# Define global variables
user_connected = False
client_socket = None

# Define terminal color
os.system("color a")

def clear():
    """Clear the terminal screen."""
    os.system("cls" if os.name == 'nt' else 'clear')

clear()

def connect():
    """Connect to the server."""
    global client_socket, user_connected

    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Replace '127.0.0.1' and 8080 with the server's IP and port.
    local_ip = socket.gethostbyname(socket.gethostname())
    server_address = (local_ip, 8080)

    try:
        # Connect to the server
        client_socket.connect(server_address)
        print(f"Connected to server at {server_address}")
        user_connected = True

        # Get the key from the user
        key = input("Enter key: ")

        # Send the key to the server
        client_socket.sendall(key.encode())

        # Receive the server's response
        response = client_socket.recv(1024).decode()
        if response == "Good":
            print("Key accepted!")
        else:
            print("Key rejected!")
            user_connected = False  # Disconnect if key is invalid
            client_socket.close()
            client_socket = None

    except Exception as e:
        print(f"Error connecting to server: {e}")
        user_connected = False

def handle_spoofer():
    """Handle the 'spoofer' command."""
    global client_socket
    if user_connected:
        try:
            # Send the 'spoofer' command to the server
            client_socket.sendall(b"spoofer")

            # Receive the file data from the server
            print("Receiving file from server...")
            with open('woofer.py', 'wb') as file:
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    file.write(data)
                    break

            os.system("start woofer.py")




            print("File received and saved as 'woofer.py'.")
        except Exception as e:
            print(f"Error during file reception: {e}")
    else:
        clear()
        print("You must connect first!")
        input("Press Enter to continue...")

def handle(command):
    """Handle user commands."""
    if command == "help":
        print(commands)
        input("Press Enter to continue...")
    elif command == "connect":
        connect()
    elif command == "spoofer":
        handle_spoofer()
    else:
        print(f"Unknown command: {command}")

commands = ["connect", "help"]

banner = r"""
 ________       .__.__   
/   __   \_____ |__|  |  
\____    /     \|  |  |  
   /    /  Y Y  \  |  |__
  /____/|__|_|  /__|____/
              \/         
"""

def menu():
    """Display the main menu."""
    while True:
        clear()
        print(banner)
        print("<9mil> Type 'help' to show commands")
        if user_connected and "spoofer" not in commands:
            commands.append("spoofer")
        command = input("> ").strip()
        handle(command)

if __name__ == "__main__":
    menu()

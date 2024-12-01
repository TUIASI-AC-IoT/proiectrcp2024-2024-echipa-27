import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk  # Import ttk for Progressbar
import socket
from mqtt_conn_packet import create_connect_packet, create_publish_packet, create_subscribe_packet
import time

BROKER_HOST = 'test.mosquitto.org'
BROKER_PORT = 1883

class MQTTClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Client")
        
        self.client_socket = None

        self.create_widgets()

    def create_widgets(self):
        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_to_broker)
        self.connect_button.pack()

        self.disconnect_button = tk.Button(self.root, text="Disconnect", command=self.disconnect_from_broker)
        self.disconnect_button.pack()

        self.subscribe_button = tk.Button(self.root, text="Subscribe", command=self.subscribe_topic)
        self.subscribe_button.pack()

        self.publish_button = tk.Button(self.root, text="Publish", command=self.publish_message)
        self.publish_button.pack()

        self.message_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=10)
        self.message_area.pack()

        self.connect_spinner = ttk.Progressbar(self.root, orient="horizontal", mode="indeterminate")
        self.connect_spinner.pack()
        self.connect_spinner.pack_forget()  # Hide the spinner initially

        self.subscribe_spinner = ttk.Progressbar(self.root, orient="horizontal", mode="indeterminate")
        self.subscribe_spinner.pack()
        self.subscribe_spinner.pack_forget()  # Hide the spinner initially

        self.publish_spinner = ttk.Progressbar(self.root, orient="horizontal", mode="indeterminate")
        self.publish_spinner.pack()
        self.publish_spinner.pack_forget()  # Hide the spinner initially

    def show_spinner(self, spinner):
        spinner.pack()
        spinner.start()

    def hide_spinner(self, spinner):
        spinner.stop()
        spinner.pack_forget()

    def connect_to_broker(self):
        try:
            self.show_spinner(self.connect_spinner)
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((BROKER_HOST, BROKER_PORT))

            client_id = "test_client"
            self.client_socket.sendall(create_connect_packet(client_id))
            self.message_area.insert(tk.END, "CONNECT packet sent\n")

            connack_packet = self.client_socket.recv(4)
            packet_type = connack_packet[0] >> 4
            if packet_type == 2:
                self.message_area.insert(tk.END, "CONNACK received, connection successful\n")
            else:
                self.message_area.insert(tk.END, "Invalid CONNACK packet\n")
                self.client_socket.close()
                self.client_socket = None
        except Exception as e:
            self.message_area.insert(tk.END, f"Error connecting to broker: {e}\n")
        finally:
            self.hide_spinner(self.connect_spinner)

    def disconnect_from_broker(self):
        if self.client_socket:
            try:
                self.client_socket.close()
                self.client_socket = None
                self.message_area.insert(tk.END, "Disconnected from broker\n")
            except Exception as e:
                self.message_area.insert(tk.END, f"Error disconnecting from broker: {e}\n")
        else:
            self.message_area.insert(tk.END, "Not connected to broker\n")

    def publish_message(self):
        if self.client_socket:
            try:
                self.show_spinner(self.publish_spinner)
                topic = "senzor/temperatura/living"
                message = "25"
                publish_packet = create_publish_packet(topic, message, 1, 1)
                self.client_socket.sendall(publish_packet)
                self.message_area.insert(tk.END, f"Publish packet sent: {publish_packet}\n")
                
                # Wait for PUBACK (QoS 1)
                ack_packet = self.client_socket.recv(4)
                packet_type = ack_packet[0] >> 4
                if packet_type == 4:  # PUBACK
                    self.message_area.insert(tk.END, "PUBACK received, message published successfully\n")
            except Exception as e:
                self.message_area.insert(tk.END, f"Error sending publish packet: {e}\n")
            finally:
                self.hide_spinner(self.publish_spinner)
        else:
            self.message_area.insert(tk.END, "Not connected to broker\n")

    def subscribe_topic(self):
        if self.client_socket:
            try:
                self.show_spinner(self.subscribe_spinner)
                topic = "senzor/temperatura/living"
                subscribe_packet = create_subscribe_packet(topic)
                
                self.client_socket.sendall(subscribe_packet)
                time.sleep(3)

                self.message_area.insert(tk.END, f"Subscribe packet sent for topic '{topic}'\n")
                suback_packet = self.client_socket.recv(5)  # Adjust the number of bytes as needed
                print("suback_packet", suback_packet)
                if len(suback_packet) < 5:
                    self.message_area.insert(tk.END, "Incomplete SUBACK packet received\n")
                    return
                packet_type = suback_packet[0] >> 4
                print("packet_type", packet_type)
                if packet_type != 9:
                    self.message_area.insert(tk.END, "Invalid SUBACK packet\n")
                    return
                
                # Extract the return code from the payload (last byte of the suback_packet)
                return_code = suback_packet[-1]
                if return_code == 0x80:
                    self.message_area.insert(tk.END, "Subscription refused\n")
                else:
                    self.message_area.insert(tk.END, "Subscription successful\n")
            except Exception as e:
                self.message_area.insert(tk.END, f"Error subscribing to topic: {e}\n")
            finally:
                self.hide_spinner(self.subscribe_spinner)
        else:
            self.message_area.insert(tk.END, "Not connected to broker\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MQTTClientApp(root)
    root.mainloop()
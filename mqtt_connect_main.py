import tkinter as tk
from tkinter import scrolledtext, ttk
import socket
import threading
from mqtt_conn_packet import *
import time 
import hashlib
import base64
import os
BROKER_HOST = 'localhost'
BROKER_PORT = 1883

class MQTTClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Client")
        self.client_socket = None
        self.keep_alive_timer = None
        self.create_widgets()
        self.password_file = "C:/passwd" 
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Add window close handler

    def on_closing(self):
        try:
            if self.keep_alive_timer:
                self.keep_alive_timer.cancel()
            
            if self.client_socket:
                self.disconnect_from_broker()
                
            self.hide_spinner(self.connect_spinner)
            self.hide_spinner(self.subscribe_spinner)
            self.hide_spinner(self.publish_spinner)
            
            self.root.destroy()
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
            self.root.destroy()
        
    def create_widgets(self):
        # Add authentication frame
        auth_frame = ttk.LabelFrame(self.root, text="Authentication")
        auth_frame.pack(padx=5, pady=5, fill="x")
        
        ttk.Label(auth_frame, text="Username:").pack(side=tk.LEFT)
        self.username_entry = ttk.Entry(auth_frame)
        self.username_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(auth_frame, text="Password:").pack(side=tk.LEFT)
        self.password_entry = ttk.Entry(auth_frame, show="*")
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        # Add topic frame
        topic_frame = ttk.LabelFrame(self.root, text="Topic")
        topic_frame.pack(padx=5, pady=5, fill="x")
        
        ttk.Label(topic_frame, text="Topic:").pack(side=tk.LEFT)
        self.topic_entry = ttk.Entry(topic_frame, width=30)
        self.topic_entry.pack(side=tk.LEFT, padx=5)
        self.topic_entry.insert(0, "senzor/temperatura/living")
        
        # Add QoS frame
        qos_frame = ttk.LabelFrame(self.root, text="QoS")
        qos_frame.pack(padx=5, pady=5, fill="x")
        
        self.qos_var = tk.IntVar(value=0)
        for i in range(3):
            ttk.Radiobutton(qos_frame, text=f"QoS {i}", 
                          variable=self.qos_var, 
                          value=i).pack(side=tk.LEFT, padx=5)
        
        # Add message frame
        msg_frame = ttk.LabelFrame(self.root, text="Message")
        msg_frame.pack(padx=5, pady=5, fill="x")
        
        ttk.Label(msg_frame, text="Message:").pack(side=tk.LEFT)
        self.message_entry = ttk.Entry(msg_frame, width=30)
        self.message_entry.pack(side=tk.LEFT, padx=5)
        
        # Add buttons frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(padx=5, pady=5)
        
        self.connect_button = ttk.Button(button_frame, text="Connect", command=self.connect_to_broker)
        self.connect_button.pack(side=tk.LEFT, padx=2)
        
        self.disconnect_button = ttk.Button(button_frame, text="Disconnect", command=self.disconnect_from_broker)
        self.disconnect_button.pack(side=tk.LEFT, padx=2)
        
        self.subscribe_button = ttk.Button(button_frame, text="Subscribe", command=self.subscribe_topic)
        self.subscribe_button.pack(side=tk.LEFT, padx=2)
        
        self.unsubscribe_button = ttk.Button(button_frame, text="Unsubscribe", command=self.unsubscribe_topic)
        self.unsubscribe_button.pack(side=tk.LEFT, padx=2)
        
        self.publish_button = ttk.Button(button_frame, text="Publish", command=self.publish_message)
        self.publish_button.pack(side=tk.LEFT, padx=2)
        
        # Add message area
        self.message_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=10)
        self.message_area.pack(padx=5, pady=5)

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

    def start_keep_alive(self):
        try:
            if self.keep_alive_timer:
                self.keep_alive_timer.cancel()
            self.keep_alive_timer = threading.Timer(60.0, self.send_ping)
            self.keep_alive_timer.daemon = True  # Make timer thread daemon
            self.keep_alive_timer.start()
        except Exception as e:
            self.message_area.insert(tk.END, f"Keep-alive timer error: {str(e)}\n")

    def send_ping(self):
        if self.client_socket:
            try:
                self.client_socket.sendall(create_pingreq_packet())
                pingresp = self.client_socket.recv(2)
                if pingresp[0] >> 4 == 13:
                    self.message_area.insert(tk.END, "Keep-alive successful\n")
            except Exception as e:
                self.message_area.insert(tk.END, f"Keep-alive failed: {e}\n")
            finally:
                self.start_keep_alive()
        
    def connect_to_broker(self):
        try:
            # Check Mosquitto service
            import subprocess
            try:
                subprocess.run(['sc', 'query', 'mosquitto'], check=True)
            except subprocess.CalledProcessError:
                self.message_area.insert(tk.END, "Starting Mosquitto service...\n")
                subprocess.run(['net', 'start', 'mosquitto'])
                time.sleep(2)

            username = self.username_entry.get()
            password = self.password_entry.get()
            
            self.show_spinner(self.connect_spinner)
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                self.client_socket.connect((BROKER_HOST, BROKER_PORT))
            except ConnectionRefusedError:
                self.message_area.insert(tk.END, "Connection refused. Checking Mosquitto status...\n")
                raise
            
            connect_packet = create_connect_packet_with_auth(
                client_id="test_client",
                username=username,
                password=password
            )
            
            self.client_socket.sendall(connect_packet)
            
            # Parse CONNACK
            connack = self.client_socket.recv(4)
            if len(connack) < 4:
                self.message_area.insert(tk.END, "Invalid CONNACK received\n")
                return
                
            packet_type = connack[0] >> 4
            return_code = connack[3]
            
            if packet_type == 2:  # CONNACK
                if return_code == 0:
                    self.message_area.insert(tk.END, "Connected successfully\n")
                    self.start_keep_alive()
                elif return_code == 135:
                    self.message_area.insert(tk.END, "Connection refused: Bad username or password\n")
                
                else:
                    self.message_area.insert(tk.END, f"Connection refused: Error code {return_code}\n")
            else:
                self.message_area.insert(tk.END, "Invalid packet type received\n")
                
            self.hide_spinner(self.connect_spinner)
                
        except Exception as e:
            self.message_area.insert(tk.END, f"Connection error: {str(e)}\n")
            self.hide_spinner(self.connect_spinner)

    def disconnect_from_broker(self):
        if self.client_socket:
            try:
                # Cancel keep-alive timer first
                if self.keep_alive_timer:
                    self.keep_alive_timer.cancel()
                    self.keep_alive_timer = None
                
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
                topic = self.topic_entry.get()
                message = self.message_entry.get()
                qos = self.qos_var.get()
                packet_id = 1

                publish_packet = create_publish_packet(
                    topic=topic,
                    message=message,
                    qos=qos,
                    packet_id=packet_id
                )
                
                self.message_area.insert(tk.END, f"Sending PUBLISH: {publish_packet.hex()}\n")
                self.client_socket.sendall(publish_packet)
                self.message_area.insert(tk.END, f"Published message: {message} to topic: {topic}\n")

                # Handle QoS acknowledgment
                if qos > 0:
                    ack = self.client_socket.recv(4)
                    self.message_area.insert(tk.END, f"Received ACK: {ack.hex()}\n")
                    
                    if len(ack) >= 4:
                        packet_type = (ack[0] & 0xF0) >> 4
                        if packet_type == 4:  # PUBACK
                            ack_packet_id = (ack[2] << 8) | ack[3]
                            if ack_packet_id == packet_id:
                                self.message_area.insert(tk.END, "Publish acknowledged\n")
                            else:
                                self.message_area.insert(tk.END, f"PUBACK packet ID mismatch\n")
                        else:
                            self.message_area.insert(tk.END, f"Invalid PUBACK type: {packet_type}\n")
                    else:
                        self.message_area.insert(tk.END, "Invalid PUBACK length\n")

            except Exception as e:
                self.message_area.insert(tk.END, f"Publish error: {str(e)}\n")
            finally:
                self.hide_spinner(self.publish_spinner)
        else:
            self.message_area.insert(tk.END, "Not connected to broker\n")

    def subscribe_topic(self):
        if self.client_socket:
            try:
                self.show_spinner(self.subscribe_spinner)
                topic = self.topic_entry.get()
                packet_id = 1
                subscribe_packet = create_subscribe_packet(topic, qos=self.qos_var.get(), packet_id=packet_id)
                
                self.client_socket.sendall(subscribe_packet)
                
                # Debug SUBACK
                suback = self.client_socket.recv(5)
                self.message_area.insert(tk.END, f"SUBACK received: {suback.hex()}\n")
                
                if len(suback) >= 4:  # MQTT 3.1.1/5.0 minimum SUBACK length
                    packet_type = (suback[0] & 0xF0) >> 4  # Correct packet type extraction
                    if packet_type == 9:  # SUBACK
                        remaining_length = suback[1]
                        if remaining_length > 0:
                            reason_code = suback[-1]  # Last byte is reason code
                            if reason_code <= 2:
                                self.message_area.insert(tk.END, f"Subscribed successfully with QoS {reason_code}\n")
                            else:
                                self.message_area.insert(tk.END, f"Subscription failed with reason code: {reason_code}\n")
                        else:
                            self.message_area.insert(tk.END, "Invalid SUBACK remaining length\n")
                    else:
                        self.message_area.insert(tk.END, f"Invalid packet type: {packet_type}, raw byte: {suback[0]:02x}\n")
                else:
                    self.message_area.insert(tk.END, f"Invalid SUBACK length: {len(suback)}\n")
                    
            except Exception as e:
                self.message_area.insert(tk.END, f"Subscribe error: {str(e)}\n")
            finally:
                self.hide_spinner(self.subscribe_spinner)
        else:
            self.message_area.insert(tk.END, "Not connected to broker\n")
                
    def unsubscribe_topic(self):
        if self.client_socket:
            try:
                topic = self.topic_entry.get()
                unsubscribe_packet = create_unsubscribe_packet(topic)
                self.client_socket.sendall(unsubscribe_packet)
                self.message_area.insert(tk.END, f"Unsubscribe packet sent for topic '{topic}'\n")
            except Exception as e:
                self.message_area.insert(tk.END, f"Error unsubscribing from topic: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MQTTClientApp(root)
    root.mainloop()
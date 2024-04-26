import os,sys
import tkinter as tk
from tkinter import messagebox, ttk
import speedtest
import threading


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def fetch_servers():
    try:
        st = speedtest.Speedtest()
        st.get_servers()  # Retrieve server list from speedtest
        # Format server names with location and distance
        servers_dict = {f"{server['name']} ({server['country']}, {server['sponsor']}) [{server['d']:.2f} km]": server['id']
                        for sublist in st.servers.values() for server in sublist}
        print("Servers fetched: ", servers_dict)  # Debug: Print fetched servers
        server_combo['values'] = list(servers_dict.keys())
        server_combo.current(0)
        return servers_dict
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch servers: {str(e)}")
        return {}

def test_speed():
    server_name = server_combo.get()
    server_id = servers.get(server_name)

    def run_test():
        progress_bar['value'] = 0
        update_progress(10)
        try:
            st = speedtest.Speedtest()
            # Debug: Output server name and ID being used for the test
            print("Testing with server:", server_name, "ID:", server_id)
            # Make sure we use the correct server
            st.get_servers([server_id])
            st.get_best_server()  # Find the best server from the list of one server
            update_progress(30)
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            update_progress(70)
            download_label.config(text=f"Download Speed: {download_speed:.2f} Mbps")
            upload_speed = st.upload() / 1_000_000     # Convert to Mbps
            update_progress(100)
            upload_label.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to test speed: {str(e)}")
        progress_bar['value'] = 0

    def update_progress(value):
        progress_bar['value'] = value
        root.update_idletasks()

    threading.Thread(target=run_test).start()

# GUI setup
root = tk.Tk()
root.iconbitmap(resource_path("speedtest-icon.ico"))
root.title("Speedy v0.1.0")
root.configure(bg='#333333')
root.geometry('350x200')  # Adjust window size

# Load and set the window icon (top left corner), resize icon to fit better
datafile="speedtest-icon.png"
speedimg=resource_path(datafile)
original_icon = tk.PhotoImage(file=speedimg)
icon = original_icon.subsample(9, 9)  # Experiment with subsample value to fit the size
icon_label = tk.Label(root, image=icon, bg='#333333')
icon_label.pack(side="top", anchor="nw")

dark_bg = '#333333'
dark_fg = '#ffffff'
accent_color = '#0078d7'

download_label = tk.Label(root, text="Download Speed: ", bg=dark_bg, fg=dark_fg)
download_label.pack(pady=3)

upload_label = tk.Label(root, text="Upload Speed: ", bg=dark_bg, fg=dark_fg)
upload_label.pack(pady=3)

server_combo = ttk.Combobox(root, width=50)
server_combo.pack(pady=10)
servers = fetch_servers()  # Fetch servers and populate combobox

progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=300)
progress_bar.pack(pady=5)
progress_bar_style = ttk.Style()
progress_bar_style.theme_use('clam')
progress_bar_style.configure("Horizontal.TProgressbar", background=accent_color, troughcolor=dark_bg, bordercolor=dark_bg, lightcolor=accent_color, darkcolor=accent_color)

test_button = tk.Button(root, text="Test Speed", command=test_speed, bg=dark_bg, fg=dark_fg, highlightbackground=dark_bg)
test_button.pack(pady=2)

root.mainloop()

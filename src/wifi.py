# This module contains the function to connect to my home wifi on startup.
# The basics were taken from youtube (https://www.youtube.com/watch?v=w0Roolfg0wc)
# Changes made:
# - network_name and network_password are now parameters of the function.
# - The object names are self-explanatory now.
# - The IP configuration is now taken from the DHCP server instead of a fixed address.
# - The function returns the network config
# - Calling the function will always reset the wifi connection and connect again


def connect_wifi(network_name, network_password):
    import network
    # Deactivate the automatic accesspoint
    try:
        accesspoint = network.WLAN(network.AP_IF)
        accesspoint.active(False)
    except:
        print("Error while deactivating accesspoint")

    # and now connect to the given wifi
    try:
        wifi_client = network.WLAN(network.STA_IF)
        wifi_client.active(True)
        wifi_client.connect(network_name, network_password)
        while not wifi_client.isconnected():
            pass
    except:
        print("Error while connecting to your wifi")
    return wifi_client.ifconfig()

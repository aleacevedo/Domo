import paho.mqtt.publish as pub


def send_to(topic, value):
    pub.single( str(topic), payload= value, hostname="localhost")
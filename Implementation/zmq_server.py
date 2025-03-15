import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:2000")

while True:
    message = socket.recv()
    print(f"Received request: {message}")
    socket.send(b"World")
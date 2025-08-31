import socket
import time


def read_seed(path: str) -> list:
    messages = []

    with open(path, 'rb') as fp:
        while True:
            # Read the 4-byte little-endian message length
            length_data = fp.read(4)
            if not length_data:
                break  # End of file

            if len(length_data) < 4:
                raise RuntimeError(f'Not enough data in seed file: {path}')

            # Unpack the length (little-endian)
            msg_length = int.from_bytes(length_data, byteorder='little')

            # Read the message content
            msg = fp.read(msg_length)
            if len(msg) < msg_length:
                raise RuntimeError(f'Incomplete message content in seed file: {path}')

            messages.append(msg)

    return messages


def recvall(sock: socket.socket, sock_type) -> bytes:
    response = b''
    timeout = sock.gettimeout()
    times = timeout / 0.01
    sock.settimeout(0.01)

    received_first = False
    count = 0
    while True:
        try:
            if sock_type == socket.SOCK_STREAM:
                chunk = sock.recv(4096)
            else:
                chunk, _ = sock.recvfrom(4096)
            if not chunk:
                break
            received_first = True
            response += chunk
        except socket.timeout:
            if received_first:
                break
            else:
                count += 1
                if count >= times:
                    break
    sock.settimeout(timeout)
    return response


# for TCP
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=True, type=str, help='path to input seed')
args = parser.parse_args()

path = args.input
messages = read_seed(path)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(0.5)
sock.connect(('127.0.0.1', 8080))

mi = 0

while mi < len(messages):
    sock.sendall(messages[mi]); mi += 1
    data = recvall(sock, socket.SOCK_STREAM)
    print(f'recv: {len(data)}, {data[:1024]}')
    time.sleep(0.1)
sock.close()

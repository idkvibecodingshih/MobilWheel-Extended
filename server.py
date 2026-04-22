import socket
import threading
import logging
import time
from dataclasses import dataclass
from typing import Dict, Optional

from .vjoy_controller import VJoyController
from .mapper import Mapper

logging.basicConfig(level=logging.INFO)


@dataclass
class MobileDevice:
    address: tuple
    socket: socket.socket


class MobilWheelTCPServer:
    def __init__(self):
        self.port = 12345
        self.devices: Dict[str, MobileDevice] = {}
        self.active_device_id: Optional[str] = None

        self.vjoy = self._init_vjoy_with_retry()
        self.mapper = Mapper()

        self.running = True

        self.last_input_time = time.time()

        # estado atual
        self.steer = 0
        self.throttle = 0
        self.brake = 0
    
    def _init_vjoy_with_retry(self):
        retry_delay = 0.5  # leve e imperceptível

        while True:
            try:
                return VJoyController()

            except Exception:
                time.sleep(retry_delay)

    # =========================
    def safe_float(self, val):
        try:
            return float(val)
        except:
            return None

    # =========================
    def _udp_discovery(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("", self.port))

        while self.running:
            data, addr = sock.recvfrom(1024)
            msg = data.decode().strip()

            if msg == "DISCOVER_SERVER":
                response = f"{self._get_ip()}:{self.port}\n"
                sock.sendto(response.encode(), addr)

    # =========================
    def _tcp_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("", self.port))
        server.listen(5)

        logging.info(f"Servidor rodando na porta {self.port}")

        while self.running:
            client, addr = server.accept()

            threading.Thread(
                target=self._handle_client,
                args=(client, addr),
                daemon=True
            ).start()

    def _handle_client(self, client, addr):
        device_id = f"{addr[0]}:{addr[1]}"
        self.devices[device_id] = MobileDevice(addr, client)

        if self.active_device_id is None:
            self.active_device_id = device_id

        buffer = ""

        try:
            while self.running:
                data = client.recv(1024)
                if not data:
                    break

                buffer += data.decode()

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self._process_command(device_id, line.strip())

        finally:
            client.close()
            self.devices.pop(device_id, None)
            self.vjoy.reset()

    # =========================
    def _process_command(self, device_id, cmd):
        if device_id != self.active_device_id:
            return

        try:
            if cmd.startswith("A:"):
                val = self.safe_float(cmd[2:])
                if val is not None:
                    self.steer = self.mapper.map_steering(val / 10.0)

            elif cmd.startswith("B:"):
                val = self.safe_float(cmd[2:])
                if val is not None:
                    self.throttle = self.mapper.map_trigger(val / 100.0, "throttle")

            elif cmd.startswith("C:"):
                val = self.safe_float(cmd[2:])
                if val is not None:
                    self.brake = self.mapper.map_trigger(val / 100.0, "brake")

            elif cmd == "D":
                self.vjoy.press_button("handbrake")

            elif cmd == "E":
                self.vjoy.press_button("boost")

            elif cmd == "F":
                self.vjoy.press_button("x")

            elif cmd == "G":
                self.vjoy.press_button("y")

            self.last_input_time = time.time()

        except Exception as e:
            logging.error(f"Erro comando {cmd}: {e}")

    # =========================
    def _output_loop(self):
        while self.running:
            # FAILSAFE
            if time.time() - self.last_input_time > 1:
                self.steer = 0
                self.throttle = 0
                self.brake = 0

            self.vjoy.update_all(self.steer, self.throttle, self.brake)
            time.sleep(0.01)

    # =========================
    def start(self):
        threading.Thread(target=self._udp_discovery, daemon=True).start()
        threading.Thread(target=self._tcp_server, daemon=True).start()
        threading.Thread(target=self._output_loop, daemon=True).start()

        while self.running:
            time.sleep(1)

    def _get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip


if __name__ == "__main__":
    MobilWheelTCPServer().start()
class UsernameException(Exception):

    def __init__(self, username, message = "Usuario invalido: "):
        self.username = username
        self.message = message

class LengthException(Exception):

    def __init__(self, message = "Error en la conexion tcp"):
        self.message = message

class UdpException(Exception):

    def __init__(self, udp_port, message = "Puerto UDP invalido: "):
        self.udp_port = udp_port
        self.message = message

class TimeoutException(Exception):

    def __init__(self, elapsed_time, message = "Se acabo el tiempo de espera: "):
        self.elapsed_time = elapsed_time
        self.message = message

class BadChecksumException(Exception):

    def __init__(self, message = "Error con el checksum"):
        self.message = message

class SocketException(Exception):

    def __init__(self, message = "Ocurrió un problema en la conexion"):
        self.message = message
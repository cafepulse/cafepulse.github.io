import logging
import routeros_api
from routeros_api.exceptions import RouterOsApiConnectionError, RouterOsApiCommunicationError

logger = logging.getLogger(__name__)

class RouterClient:
    """
    Lightweight, synchronous wrapper around routeros_api.
    Responsible ONLY for connection, disconnection, and credential validation.
    """
    def __init__(self, host, username, password, port=8728, use_ssl=False):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.use_ssl = use_ssl
        
        self.connection = None
        self.api = None
        
    def connect(self):
        """
        Establishes connection to the MikroTik router.
        Raises specific exceptions on failure.
        """
        if self.connection and self.api:
            return True
            
        try:
            self.connection = routeros_api.RouterOsApiPool(
                self.host,
                username=self.username,
                password=self.password,
                port=self.port,
                plaintext_login=True,
                use_ssl=self.use_ssl
            )
            self.connection.set_timeout(3)
            self.api = self.connection.get_api()
            logger.info(f"Connected to MikroTik router at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to router {self.host}: {str(e)}")
            self.disconnect()
            raise
            
    def disconnect(self):
        """
        Safely disconnects from the router.
        """
        try:
            if self.connection:
                self.connection.disconnect()
        except Exception as e:
            logger.warning(f"Error during disconnect: {str(e)}")
        finally:
            self.connection = None
            self.api = None
            logger.info("Disconnected from MikroTik router")
            
    def validate_credentials(self):
        """
        Attempts to connect and immediately disconnects to validate credentials.
        Returns (True, None) if valid, (False, error_message) if invalid.
        """
        try:
            self.connect()
            self.disconnect()
            return True, None
        except RouterOsApiCommunicationError as e:
            return False, "Authentication/Communication failed. Please check credentials and API status."
        except RouterOsApiConnectionError as e:
            return False, f"Connection failed. Please check host and port: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error during validation: {str(e)}"
            
    def get_api(self):
        """
        Returns the active API instance.
        """
        if not self.api:
            raise RuntimeError("Not connected to router. Call connect() first.")
        return self.api

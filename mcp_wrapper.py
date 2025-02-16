import logging
from mcp import MCPClient

class MCPWrapper:
    def __init__(self, default_server_url="http://localhost:8000", server_urls=None):
        """
        Initialize the MCP client with a default server URL.
        Allows specifying different URLs for specific resources.
        """
        self.default_server_url = default_server_url
        self.server_urls = server_urls or {}  # Dict of {resource_name: server_url}
        self.clients = {}  # Cache MCP clients per server
        self.logger = logging.getLogger("MCPWrapper")

    def _get_client(self, resource):
        """
        Get or create an MCP client for the given resource's server.
        """
        server_url = self.server_urls.get(resource, self.default_server_url)
        
        if server_url not in self.clients:
            self.logger.info(f"Initializing MCP client for {server_url}")
            self.clients[server_url] = MCPClient(server_url=server_url)
        
        return self.clients[server_url]

    def call(self, resource, params):
        """
        Make a request to the MCP server handling the given resource.
        """
        client = self._get_client(resource)
        self.logger.info(f"Calling MCP Resource: {resource} with params: {params}")

        try:
            response = client.request(resource, params)
            if response.error:
                self.logger.error(f"MCP Error ({resource}): {response.error}")
                return None  # Handle errors gracefully
            
            return response.data  # Return data if successful

        except Exception as e:
            self.logger.exception(f"Unexpected MCP Error ({resource}): {str(e)}")
            return None  # Gracefully handle unexpected failures

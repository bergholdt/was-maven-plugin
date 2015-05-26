import sys

class ServerMapping:
    def __init__(self, server):
        self.server = server

    def build:
        serverMapping = 'WebSphere:server=' + server
        return serverMapping

class ClusterServerMapping(ServerMapping):
    def __init__(self, server, cluster):
        super.__init(server)
        self.cluster = cluster

    def build:
        cell = AdminControl.getCell()
        serverMapping = 'WebSphere:cell=' + cell + ',cluster=' + self.cluster
        unmanagedNodeNames = AdminTask.listUnmanagedNodes().splitlines()
        for unmanagedNodeName in unmanagedNodeNames:
            webservers = AdminTask.listServers('[-serverType WEB_SERVER -nodeName ' + unmanagedNodeName + ']').splitlines()
            for webserver in webservers:
                webserverName = AdminConfig.showAttribute(webserver, 'name')
                serverMapping = serverMapping + '+WebSphere:cell=' + cell + ',node=' + unmanagedNodeName + ',server=' + webserverName
        return serverMapping

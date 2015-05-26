import websphere

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

class MyWebsphere(WebSphere):
    def _getAppManager(self):
        if "" != cluster:
            appManager = AdminControl.queryNames('type=ApplicationManager,process=' + server + ',*')
        elif "" != node:
            appManager = AdminControl.queryNames('node=' + node + ',type=ApplicationManager,process=' + server + ',*')
        else:
            appManager = AdminControl.queryNames('type=Server,process=' + server + ',*')
        return appManager

    def _getServerOptions(self):
        options = ['-deployws', '-distributeApp', '-appname', applicationName, '-server', server]

        if "" != cluster:
            serverMapping = ClusterServerMapping(server, cluster).build()
            options += ['-cluster', cluster, '-MapModulesToServers', [['.*','.*', serverMapping]]]
        else:
            serverMapping = ServerMapping(server).build()
            options += ['-MapModulesToServers', [['.*','.*', serverMapping]]]

        if "" != contextRoot:
            options += ['-contextroot', contextRoot]

        if "" != virtualHost:
            options += ['-MapWebModToVH', [['.*','.*', virtualHost]]]

        if "" != sharedLibs:
            libs = []
            for lib in sharedLibs.split(','):
                libs.append(['.*','.*', lib])
            options += ['-MapSharedLibForMod', libs]

        return options

targetScope = 'resourceGroup'

@minLength(1)
@description('Primary location for all resources')
param location string = 'eastus'

@description('Name used to generate a unique string for deployed resources.')
param environmentName string = 'qdrantazureaks'

@secure()
param sshRSAPublicKey string

@description('Username to connect to the AKS cluster.')
param linuxAdminUsername string

var abbrs = loadJsonContent('abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))

module aks 'resources.bicep' = {
  name: 'qdrant-aks-deploy'
  scope: resourceGroup()
  params: {
    location: location
    dnsPrefix: environmentName
    clusterName: '${abbrs.containerServiceManagedClusters}${resourceToken}'
    linuxAdminUsername: linuxAdminUsername
    sshRSAPublicKey: sshRSAPublicKey
  }
}

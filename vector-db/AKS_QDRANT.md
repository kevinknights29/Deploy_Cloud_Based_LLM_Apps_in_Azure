# Running qdrant in `AKS`

## Pre Requisites

### Install Azure CLI

MacOS

```bash
brew update && brew install azure-cli
```

Windows

```powershell
$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'; Remove-Item .\AzureCLI.msi
```

Check full list of options for Windows [here](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli)

Docs: [Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

## Deployment

1. Create a resource group in Azure

    ```bash
    az group create --name <YOUR_RESOURCE_GROUP_NAME> --location eastus

    az sshkey create --name "qdrantSSHKey" --resource-group "<YOUR_RESOURCE_GROUP_NAME_CREATED_ABOVE>"
    ```

2. Create an AKS resource

    ```bash
    az deployment group create \
    --name qdrantVectorDB \
    --resource-group '<YOUR_RESOURCE_GROUP_NAME_CREATED_ABOVE>' \
    --template-file vector-db/aks/main.bicep \
    --parameters location='eastus' environmentName='qdrantazureaks' linuxAdminUsername='<YOUR_PUBLIC_SSH_KEY_CREATED_ABOVE>' sshRSAPublicKey='<YOUR_PUBLIC_SSH_KEY_CREATED_ABOVE>'
    ```

    To point to a path, you can: `"$(cat your/ssh/path)"`

3. Get AKS Crendetials

    ```bash
    az aks get-credentials --resource-group <YOUR_RESOURCE_GROUP_NAME_CREATED_ABOVE>  --name <YOUR_AKS_RESOURCE_NAME_CREATED_ABOVE>
    ```

    You can check your AKS resource name from the Azure Portal:
    ![image](https://github.com/kevinknights29/Deploy_Cloud_Based_LLM_Apps_in_Azure/assets/74464814/17e1b725-12e1-4be0-bd12-d38d7ab33b38)

4. Install Helm Chart

    ```bash
    helm install "<YOUR_INSTALLATION_NAME>" vector-db/aks/helm --create-namespace
    ```

5. Test your cluster

    ```bash
    kubectl get services
    ```

    Extract the external ip address from the loadbalancer.

    ```bash
    curl -X PUT 'http://<YOUR_LOAD_BALANCER_EXTERNAL_IP_ADDRESS>:6333/collections/test_collection' \
    -H 'Content-Type: application/json' \
    --data-raw '{
        "vectors": {
            "size": 4,
            "distance": "Dot"
        }
    }'
    ```

    You verify if the collection was created by accessing: `http://<YOUR_LOAD_BALANCER_EXTERNAL_IP_ADDRESS>:6333/dashboard`

    OR

    ```bash
    curl 'http://<YOUR_LOAD_BALANCER_EXTERNAL_IP_ADDRESS>:6333/collections/test_collection'
    ```

    ![image](https://github.com/kevinknights29/Deploy_Cloud_Based_LLM_Apps_in_Azure/assets/74464814/5eaf4d46-278d-43c3-b950-03443ff400f3)

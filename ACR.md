# Pushing container to Azure Container Registry

1. Create Azure Container Registry Resource

    ```bash
    az acr create --resource-group "<YOUR_RESOURCE_GROUP_NAME>" --name "<YOUR_CONTAINER_REGISTRY_NAME>"  --sku Basic
    ```

2. Grant access to Azure Container Registry

    - Visit [Azure Portal](https://portal.azure.com/)
    - Search for your Resource Group.
    - Search for your Azure Container Registry.
    - Select `Access Control (IAM)` on the left menu.
    - Select `add` on the top menu.
    - Select `add role assignment`.
    - Grant you the roles:
        - AcrPull
        - AcrPush

    ![image](https://github.com/kevinknights29/Deploy_Cloud_Based_LLM_Apps_in_Azure/assets/74464814/aaabdb17-c8f5-47e7-b010-ccb93c87a82a)

    ![image](https://github.com/kevinknights29/Deploy_Cloud_Based_LLM_Apps_in_Azure/assets/74464814/de4530cc-57eb-4c3b-8759-d7adcdf5863c)

3. Login to the Azure Container Registry

    ```bash
    az acr login -n "<YOUR_CONTAINER_REGISTRY_NAME>"
    ```

    If you get an error, you can try refreshing your credentials with:

    ```bash
    az login
    ```

4. Push image to the Azure Container Registry

    ```bash
    docker build -t <YOUR_IMAGE_NAME>:<YOUR_VERSION_NUMBER> .
    docker tag <YOUR_IMAGE_NAME>:<YOUR_VERSION_NUMBER> <YOUR_CONTAINER_REGISTRY_NAME>.azurecr.io/azure_demo:v1
    docker push <YOUR_CONTAINER_REGISTRY_NAME>.azurecr.io/<YOUR_IMAGE_NAME>:<YOUR_VERSION_NUMBER>
    ```

5. Verify image was uploaded to Azure Container Registry

    ![image](https://github.com/kevinknights29/Deploy_Cloud_Based_LLM_Apps_in_Azure/assets/74464814/526871f5-4dcd-40be-b982-6d89fb97450d)

    ![image](https://github.com/kevinknights29/Deploy_Cloud_Based_LLM_Apps_in_Azure/assets/74464814/4b02e3fa-739c-4593-b71d-d8687cf21a92)

6. Get your container registry password

    ```bash
    az acr update -n <YOUR_CONTAINER_REGISTRY_NAME> --admin-enabled true
    az acr credential show --name <YOUR_CONTAINER_REGISTRY_NAME>
    ```

7. Modify the following lines of: `deployment.yml`
    - line 2: location
    - line 3: name
    - line 6: name (app)
    - line 8: image
    - line 19: server (regisrtry url)
    - line 20: username (regisrtry name)
    - line 21: password (registry password)
    - line 30: dnsNameLabel

8. Modify the following lines of: `nginx.conf`
    - line 22,53: server_name ($dnsNameLabel.$location)

9. Create container

    ```bash
    az container create --resource-group <YOUR_RESOURCE_GROUP_NAME> --name <YOUR_DEPLOYMENT_NAME>  -f deployment.yml
    ```

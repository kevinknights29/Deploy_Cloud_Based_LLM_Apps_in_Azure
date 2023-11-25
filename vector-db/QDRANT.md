# Running qdrant in docker

## Setup

To run qdrant locally, run the following commands:

```bash
docker pull qdrant/qdrant
```

```bash
docker run -p 6333:6333 \
    -v $(pwd)/vector-db/data:/qdrant/storage \
    -v $(pwd)/vector-db/.config/config.yaml:/qdrant/config/production.yaml \
    qdrant/qdrant
```

## Results

Your output should look like this:

![image](https://github.com/kevinknights29/Deploy_Cloud_Based_LLM_Apps_in_Azure/assets/74464814/58be6e26-ff3a-494f-9eac-7a4ca4af3e8c)

## Tips

If you would like to run the container in the background and keep your terminal for development, you can run:

```bash
docker run -d -p 6333:6333 \
    -v $(pwd)/vector-db/data:/qdrant/storage \
    -v $(pwd)/vector-db/.config/config.yaml:/qdrant/config/production.yaml \
    qdrant/qdrant
```

The flag `-d` will detach the docker container output from your terminal.

![image](https://github.com/kevinknights29/Deploy_Cloud_Based_LLM_Apps_in_Azure/assets/74464814/6a7a4b9b-2e4d-4d25-aa82-8c1e6948986b)

### View from Docker Desktop

![image](https://github.com/kevinknights29/Deploy_Cloud_Based_LLM_Apps_in_Azure/assets/74464814/8a5eb6a5-d3ce-40c5-a6e2-5da306cae7c0)

## Resources

- [Azure Sample for qdrant](https://github.com/Azure-Samples/qdrant-azure/blob/main/Local-Docker-Deployment/README.md)
- [qdrant Docs](https://qdrant.tech/documentation/guides/installation/)

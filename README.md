
## Docker Commands
```
docker build -t assignment .
docker run --name assignment -p 8040:80 assignment 
```

## API
To see if the container is running, send a GET request to http://localhost:8040/, you should see a `{"Hello": "World"}`

To send a query to the model, send a POST request to 
http://localhost:8040/query, with the JSON body `{"query": "{YOUR_QUERY}"}`

For example:

Sending a POST request with body `{"query": "who are you?"}`

You should see an output like this: `{
    "output": "I am not a real person. I am an artificial intelligence program designed to help you communicate with chatbots. However, my programming code and responses are generated using a complex algorithm that incorporates data and analytics from various sources"
}`
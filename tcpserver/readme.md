This is a multi-threaded TCP server that listens on local network interface, port 1800, sleeps for 5 seconds, and returns an HTTP response.
The main thread issues the blocking call **accept** and forks a new thread on receiving a request. With a new thread processing the request, the main thread can serve multiple clients simultaneously.
The OS calls accept, recv, send are blocking. *accept* returns a new socket object that is different from the one that server is using to listen on port 1800 to accept new connection. This new socket is the one server uses to communicate with the client.

Start server using
```
python tcpserver.py
```

Send requests via curl
```
curl http://localhost:1800
```

Potential improvements:
1. Limit the number of concurrent threads
2. Reduce thread creation latency by using a threadpool
3. Specify a connect timeout to handle slow clients
4. Specify a tcp backlog queue size

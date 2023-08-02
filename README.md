## Tips

If you are running this on a machine that is also acting as the reverse proxy, some of the DNS can get wonky. An easy work around is to run the script in a container and provide a custom DNS server.

```
docker run 
    --dns 8.8.8.8 
    -v <path_to_repo>:/host_monitor 
    python:slim python3 /host_monitor/monitor.py -u <url> -n <service_name>
```
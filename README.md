# wrkbench

This is a simple shell script to create lua file to test http multipart upload.

## Example

For example you want to post N files using multipart
```
 ./wrkbench <file1> <file2> .. <fileN>
```
This will create a folder ```/tmp/wrkbench-<seconds-since-epoch>```

run wrk command with -s post.lua to start the test. Example
```
wrk -t1 -c1 -d5s -R1 -s /tmp/wrkdesk-1585595404/post.lua https://192.168.2.2:8443/uploader
```

## Happy Benchmarking

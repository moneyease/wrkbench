# wrkbench

This is a simple shell script to create lua file to test http multipart upload.

## Example

For example you want to upload two (or more files)
```
 ./wrkbench <file1> <file2> .. <fileN>
```
This will create a folder ```/tmp/wrkbench-<seconds-since-epoch>```

run wrk command with -s post.lua to start the test

## Happy Benchmarking

WORKFOLDER=/tmp/wrkbench-`date +%s`
mkdir $WORKFOLDER
OUTFILE=out
TMPFILE=$WORKFOLDER/$OUTFILE
c=0
for var in "$@"
do
    echo  "--e31ffb3db174a8bc"                                                 >> $TMPFILE
    echo  "Content-Disposition: form-data; name="file$c"; filename=\"$var\""   >> $TMPFILE
    echo  "Content-Type: application/octet-stream"                             >> $TMPFILE
    echo  ""                                                                   >> $TMPFILE
    cat $var                                                                     >> $TMPFILE
    echo  ""                                                                   >> $TMPFILE
    c=$((c + 1))
done
echo  "--e31ffb3db174a8bc--\c"                                                   >> $TMPFILE


cat <<EOT >> $WORKFOLDER/post.lua
wrk.method = "POST"
local f = io.open("$TMPFILE", "r")
wrk.body   = f:read("*all")
if not f then
        print "bad file"
        return nil
end
wrk.headers["Content-Type"] =  "multipart/form-data;boundary=\"e31ffb3db174a8bc\""
wrk.headers["Expect"] = "--http1.1"
wrk.headers["User-Agent"] = "wrk/2"
wrk.headers["Accept"] = "*/*"
wrk.headers["Host"] = "10.2.208.199:8000"
f:close()
EOT

echo "Files are stored in $WORKFOLDER"
echo "Example: wrk -t1 -c1 -d5s -s $WORKFOLDER/post.lua https://192.168.2.2:8443/uploader"

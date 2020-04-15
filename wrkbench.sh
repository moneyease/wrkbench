WORKFOLDER=/tmp/wrkbench-`date +%s`
mkdir $WORKFOLDER
OUTFILE=out
TMPFILE=$WORKFOLDER/$OUTFILE
c=0
for var in "$@"
do
    type=`echo $var | awk -F. '{print $NF}'`
    echo $type
    echo  "--e31ffb3db174a8bc"    >> $TMPFILE
    echo  "Content-Disposition: form-data; name="file$c"; filename=\"$var\""   >> $TMPFILE
    case $type in
          "json")
          CTVALUE="Content-Type: application/json"
          ;;
          "txt")
          CTVALUE="Content-Type: text/plain"
          ;;
          "doc")
          CTVALUE="Content-Type: application/msword"
          ;;
          "dot")
          CTVALUE="Content-Type: application/msword"
          ;;
          "docx")
          CTVALUE="Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          ;;
          "dotx")
          CTVALUE="Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.template"
          ;;
          "docm")
          CTVALUE="Content-Type: application/vnd.ms-word.document.macroEnabled.12"
          ;;
          "dotm")
          CTVALUE="Content-Type: application/vnd.ms-word.template.macroEnabled.12"
          ;;
          "xls")
          CTVALUE="Content-Type: application/vnd.ms-excel"
          ;;
          "xlt")
          CTVALUE="Content-Type: application/vnd.ms-excel"
          ;;
          "xla")
          CTVALUE="Content-Type: application/vnd.ms-excel"
          ;;
          "xlsx")
          CTVALUE="Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          ;;
          "xltx")
          CTVALUE="Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.template"
          ;;
          "xlsm")
          CTVALUE="Content-Type: application/vnd.ms-excel.sheet.macroEnabled.12"
          ;;
          "xltm")
          CTVALUE="Content-Type: application/vnd.ms-excel.template.macroEnabled.12"
          ;;
          "xlam")
          CTVALUE="Content-Type: application/vnd.ms-excel.addin.macroEnabled.12"
          ;;
          "xlsb")
          CTVALUE="Content-Type: application/vnd.ms-excel.sheet.binary.macroEnabled.12"
          ;;
          "ppt")
          CTVALUE="Content-Type: application/vnd.ms-powerpoint"
          ;;
          "pot")
          CTVALUE="Content-Type: application/vnd.ms-powerpoint"
          ;;
          "pps")
          CTVALUE="Content-Type: application/vnd.ms-powerpoint"
          ;;
          "ppa")
          CTVALUE="Content-Type: application/vnd.ms-powerpoint"
          ;;
          "pptx")
          CTVALUE="Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation"
          ;;
          "potx")
          CTVALUE="Content-Type: application/vnd.openxmlformats-officedocument.presentationml.template"
          ;;
          "ppsx")
          CTVALUE="Content-Type: application/vnd.openxmlformats-officedocument.presentationml.slideshow"
          ;;
          "ppam")
          CTVALUE="Content-Type: application/vnd.ms-powerpoint.addin.macroEnabled.12"
          ;;
          "pptm")
          CTVALUE="Content-Type: application/vnd.ms-powerpoint.presentation.macroEnabled.12"
          ;;
          "potm")
          CTVALUE="Content-Type: application/vnd.ms-powerpoint.template.macroEnabled.12"
          ;;
          "ppsm")
          CTVALUE="Content-Type: application/vnd.ms-powerpoint.slideshow.macroEnabled.12"
          ;;
            *)
          CTVALUE="Content-Type: application/octet-stream"  >> $TMPFILE
          ;;
    esac
    echo "$CTVALUE"  >> $TMPFILE
    echo  ""  >> $TMPFILE
    cat $var    >> $TMPFILE
    echo  ""  >> $TMPFILE
    c=$((c + 1))
done
echo  "--e31ffb3db174a8bc--" >> $TMPFILE


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

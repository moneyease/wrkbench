#!/usr/bin/python

import sys
import os 
import time
import calendar
import mimetypes

from argparse import ArgumentParser

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def write_out(args,fname):
        outer = MIMEMultipart()
        for filename in args.file:
            ctype, encoding = mimetypes.guess_type(filename)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                with open(filename) as fp:
                    # Note: we should handle calculating the charset
                    msg = MIMEText(fp.read(), _subtype=subtype)
            elif maintype == 'image':
                with open(filename, 'rb') as fp:
                    msg = MIMEImage(fp.read(), _subtype=subtype)
            elif maintype == 'audio':
                with open(filename, 'rb') as fp:
                    msg = MIMEAudio(fp.read(), _subtype=subtype)
            else:
                with open(filename, 'rb') as fp:
                    msg = MIMEBase(maintype, subtype)
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'form-data', filename=filename)
            outer.attach(msg)
        composed = outer.as_string()
        with open(fname, 'w') as fp:
            fp.write(composed)
	fp.close()

def write_script(args,fname):
	fs= open(fname,"w+")
	fs.write('wrk.method = "POST"\n')
	fs.write('local f = io.open("out", "r")\n')
	fs.write('wrk.body   = f:read("*all")\n')
	fs.write('if not f then\n')
	fs.write('   print "bad file"\n')
	fs.write('   return nil\n')
	fs.write('end\n')
        for h in args.header:
            data = h.split(':',1)
            fs.write('wrk.headers["'+data[0]+'"] = "'+data[1]+'"\n')
	fs.write('f:close()\n')
	fs.close()

def main():
   parser = ArgumentParser(description="""\
Use this script to generate a lua script for multipart
upload test with wrk tool
Example: ./wrkbench.py -F file1 -F file2 -H "User-Agent:Mozila"
Usage: wrk -s post.lua
""")
   parser.add_argument('-F', '--file',required=True,action='append',
                help='List file(s) to be uploaded(required)')
   parser.add_argument('-H', '--header',action='append',
                help='Add HTTP header(s) e.g. "key:value"')
   parser.add_argument('-o', '--output',default='/tmp',
                help='Specify output directory')
   args = parser.parse_args()

   ts = calendar.timegm(time.gmtime())
   path= args.output+'/wrkbench-'+ str(ts)
   os.mkdir(path)

   write_out(args,path+'/out')
   write_script(args, path+'/post.lua')
   print "Files generated in "+path

if __name__ == "__main__":
    main()
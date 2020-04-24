#!/usr/bin/python3

import calendar
import hashlib
import mimetypes
import ntpath
import os
import time
from argparse import ArgumentParser
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_digest(filename):
    h = hashlib.sha256 ()
    with open (filename, 'rb') as file:
        while True:
            chunk = file.read (h.block_size)
            if not chunk:
                break
            h.update (chunk)
    return h.hexdigest ()


def write_mime(outer, filename):
    ctype, encoding = mimetypes.guess_type (filename)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split ('/', 1)
    if maintype == 'text':
        with open (filename) as fp:
            # Note: we should handle calculating the charset
            msg = MIMEText (fp.read (), _subtype=subtype)
    elif maintype == 'image':
        with open (filename, 'rb') as fp:
            msg = MIMEImage (fp.read (), _subtype=subtype)
    elif maintype == 'audio':
        with open (filename, 'rb') as fp:
            msg = MIMEAudio (fp.read (), _subtype=subtype)
    else:
        with open (filename, 'rb') as fp:
            msg = MIMEBase (maintype, subtype)
            msg.set_payload (fp.read ())
        encoders.encode_base64 (msg)
    msg.add_header ('Content-Disposition', 'form-data', filename=filename)
    outer.attach (msg)


def write_out(args, path):
    fname = path + '/out'
    ftmp = fname + '.tmp'
    outer = MIMEMultipart ()
    for filename in args.file:
        write_mime (outer, filename)
    composed = outer.as_string ()
    with open (ftmp, 'w') as fp:
        fp.write (composed)
    fp.close
    with open (ftmp, 'r') as fp:
        first_line = fp.readline ()
        data = fp.read ().splitlines (True)
    fp.close ()
    os.remove(ftmp)
    with open (fname, 'w') as fout:
        truncate = data [2:]
        for line in truncate:
            fout.write (line.replace (path + '/', ''))
        fout.close ()
    return first_line.replace ('mixed', 'form-data').replace ('"', '\\"').replace ('\n', '')


def write_script(args, path, first_line):
    fname = path + '/post.lua'
    fs = open (fname, "w+")
    fs.write ('wrk.method = "POST"\n')
    fs.write ('local f = io.open("out", "r")\n')
    fs.write ('wrk.body   = f:read("*all")\n')
    fs.write ('if not f then\n')
    fs.write ('   print "bad file"\n')
    fs.write ('   return nil\n')
    fs.write ('end\n')
    data = first_line.split (':', 1)
    fs.write ('wrk.headers["' + data [0] + '"] = "' + data [1].replace(" ","") + '"\n')
    if args.header:
        for h in args.header:
            data = h.split (':', 1)
            fs.write ('wrk.headers["' + data [0] + '"] = "' + data [1] + '"\n')
    else:
            fs.write ('wrk.headers["User-Agent"] = "wrk2"\n')
    fs.write ('f:close()\n')
    fs.close ()


def basename(filepath):
    name = ntpath.basename (filepath)
    basename, _ = os.path.splitext (name)
    return basename


def main():
    parser = ArgumentParser (description="""\
Use this script to generate a lua script for multipart
upload test with wrk tool
Example: ./wrkbench.py -F file1 -F file2 -H "User-Agent:Mozila"
Usage: wrk -s post.lua
""")
    parser.add_argument ('-F', '--file', required=True, action='append',
                         help='List file(s) to be uploaded(required)')
    parser.add_argument ('-H', '--header', action='append',
                         help='Add HTTP header(s) e.g. "key:value"')
    parser.add_argument ('-o', '--output', default='/tmp',
                         help='Specify output directory')
    parser.add_argument ('-t', '--tenant', default='gpcs',
                         help='Specify tenant')
    parser.add_argument ('-p', '--profile', default='11995050',
                         help='Specify profile')
    parser.add_argument ('-s', '--service', default='prisma-access',
                         help='Specify service name')
    args = parser.parse_args ()

    ts = calendar.timegm (time.gmtime ())
    path = args.output + '/wrkbench-' + str (ts)
    os.mkdir (path)

    first_line = write_out (args, path)
    write_script (args, path, first_line)
    print ("Files generated in " + path)


if __name__ == "__main__":
    main ()

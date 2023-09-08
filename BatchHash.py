"""
@author:
@file:file-hash.py
@time:2023/09/0611:20
@file_desc:
  calculate the files' hash code,
  - allow wild-card
  - allow recursive search given depth
"""
import os,sys
import glob
import hashlib
import argparse

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__=='__main__':
    parser=argparse.ArgumentParser("Calculate the check-sum(md5) of files. \n"+os.path.basename(__file__))
    parser.add_argument("files",type=str,help="specify file(s).")
    parser.add_argument("-d","--dir",type=str,help="folder to search. current folder if ignored.")
    parser.add_argument("-r", "--recursive", action='store_true',help="perform recursive. default is false")
    parser.add_argument("-o", "--output", type=str, help="output file")
    parser.add_argument("-v", "--verbose", action='store_true', help="stdout print")
    args=parser.parse_args()
    files = args.files
    rootdir = args.dir
    recursive = args.recursive
    output = args.output
    verbose = args.verbose

    if rootdir is None:
        rootdir ='./'
    try:
        if output:
            f = open(output, "wt")
    except Exception as e:
        print(e)
        sys.exit(1)

    occured=[]
    total = 0
    for root,*_ in os.walk(rootdir):
        files_=root+"/"+files
        # print(files_)
        for fname in sorted(glob.glob(files_)):
            res = md5(fname)
            total +=1
            if res in occured:
                boccured = True
            else:
                boccured = False
                occured.append(res)
            out_str = "%s\t%s\t%s"%(fname,res, "+++" if boccured else "***")
            if verbose:
                print(out_str)
            if output:
                f.write("%s\n"%(out_str))
        if not recursive:
            break
    out_str = "Total:%d identical:%d duplicated:%d"%(total,len(occured),total-len(occured))
    if verbose:
        print(out_str)
    if output:
        f.write("%s\n" % (out_str))
    try:
        if output:
            f.close()
    except Exception as e:
        print(e)
        sys.exit(2)

    sys.exit(0)
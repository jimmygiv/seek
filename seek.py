#!/usr/bin/env python3
from re import finditer,match,compile as recompile,error as regerror,sub,MULTILINE,IGNORECASE
from os import access,path,R_OK
from argparse import ArgumentParser,ArgumentTypeError


class Seek:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.filename = self.validate_file(self.kwargs.get('filename'))
        self.string = self.validate_string(self.kwargs.get('string'))
        self.regex = self.validate_regex(self.kwargs.get('regex'))
        self.hexstring = self.validate_hex(self.kwargs.get('hexstring'))
        for searchtype in (self.string, self.regex, self.hexstring):
            if bool(searchtype):
                self.pattern = searchtype
                break
    def run(self):
        self.openfile()
        self.search()
        self.preview()
    def validate_file(self, value):
        if value is None: return value
        if not path.isfile(value):
            raise ArgumentTypeError("Invalid file")
        if not access(value, R_OK):
            raise ArgumentTypeError("File is not readable")
        return value
    def validate_string(self, value):
        if value is None:
            return
        elif type(value) not in [str, int, float]:
            raise ArgumentTypeError("Invalid string")
        return value.encode()
    def validate_regex(self, value):
        if value is None:
            return
        try:
            if 'nocase' in self.kwargs and self.kwargs['nocase'] == True:
                value = recompile(value.encode(), IGNORECASE)
            elif 'multiline' in self.kwargs and self.kwargs['multiline'] == True:
                value = recompile(value.encode(), MULTILINE)
            elif ('multiline' and 'nocase') in self.kwargs and (self.kwargs['nocase'] and self.kwargs['multiline']) == True:
                value = recompile(value.encode(), MULTILINE, IGNORECASE)
            else:
                value = recompile(value.encode())
        except regerror as e:
            raise ArgumentTypeError("Invalid regular expression") from e
        return value
    def validate_hex(self, value):
        if value is not None:
            value = value.replace(' ','')
            value = value.replace('\r','')
            value = value.replace('\n', '')
            value = value.replace('\t', '')  
            try:
                return bytes.fromhex(value)
            except ValueError as e:
                raise ArgumentTypeError("Invalid hex string") from e
    def openfile(self, filename=None):
        if not self.filename:
            self.filename = filename
        self.file = open(self.filename, 'rb')
        if 'mindepth' in self.kwargs and type(self.kwargs['mindepth']) == int:
            self.file.seek(self.kwargs['mindepth'])
            self.mindepth = self.kwargs['mindepth']
        if 'maxdepth' in self.kwargs and type(self.kwargs['maxdepth']) == int:
            self.content = self.file.read(self.kwargs['maxepth'])
            self.maxdepth = self.kwargs['maxepth']
        else:
            self.content = self.file.read()
    def search(self, pattern=None, content=None):
        if not self.content:
            self.content = content
        if not self.pattern:
            self.pattern = pattern
        self.offsets = [
            [match.start(),match.start()+len(match.group(0))] for match in finditer(self.pattern, self.content)
        ]
        if self.kwargs['mindepth']:
            for i, li in enumerate(self.offsets, 0):
                x,y = li
                self.offsets[i] = [x+self.mindepth,y+self.mindepth]
                
    def preview(self, offsets=None):
        self.offsets = offsets or self.offsets
        if not self.offsets: 
            print("[!] No results found.")
            return
        print(f"# PATTERN: {self.pattern}")
        print(f'# MATCHES: {len(self.offsets)}')
        print(f"# OFFSETS: {self.offsets}")
        print( "# MIN    : MAX      -- CONTENT[min-20]:CONTENT[max+20]")
        for x,y in self.offsets:
            if self.kwargs['mindepth']:
                x = x-self.mindepth
                y = y-self.mindepth
            print(
                  repr(f'# {x+self.kwargs["mindepth"] if self.kwargs["mindepth"] else x}'.ljust(9).encode()   #Adjust x for mindepth offset
                + ": ".encode()
                + f'{y+self.kwargs["mindepth"] if self.kwargs["mindepth"] else y}'.ljust(9, ' ').encode()     #Adjust y for mindepth offset
                + b'-- '
                + self.content[x -20:x]
                + self.content[x:y]
                + self.content[y:y+20])[2:-1]
            )

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", required=True, default=None,
                        help="input file")
    parser.add_argument("-s", "--string", required=False, default=None, type=str,
                        help="search string")
    parser.add_argument("--hex", required=False, default=None, 
                        help="search for a hex pattern")
    parser.add_argument("-r", "--regex", required=False, default=None, 
                        help="search for a regular expression pattern")
    parser.add_argument("-m", "--multiline", action="store_true", required=False, default=None,
                        help="Regex option for multiline searching")
    parser.add_argument("--nocase", action="store_true", required=False, default=None,
                        help="Regex option for ignorecase aka nocase")
    parser.add_argument("--min", "--min-depth", required=False, default=None, type=int,
                        help="Minimum depth to read in a file")
    parser.add_argument("--max", "--max-depth", required=False, default=None, type=int,
                        help="Maximum depth to read in a file")
    args = parser.parse_args()
    s = Seek(
        filename=args.file,
        string=args.string, regex=args.regex, hexstring=args.hex, #Search types
        multiline=args.multiline, nocase=args.nocase,             #Regex options
        mindepth=args.min, maxdepth=args.max                      #File seek options
    )
    s.run()

args = parser.parse_args()

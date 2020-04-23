import re

class WowTocParser:
    def __init__(self, toc):
        self.toc = toc
        self.name = ""
        self.version = ""
        self.tocVersion = ""

        self._parse()

    def _removeStupidStuff(self, s):
        s = re.sub(r"\|r", "", s)
        s = re.sub(r"\|c.{8}", "", s)
        s = re.sub(r"\[|\]", "", s)

        return s

    def _lchop(self, s, prefix):
        if prefix and s.startswith(prefix):
            return s[1:]

        return s

    def _parse(self):
        directive_re = re.compile(r"^## *(.*): *(.*)$")

        titleDirectives = ['X-Curse-Project-Name', 'Title', 'Title.....', ]
        versionDirectives = ['X-Curse-Packaged-Version', 'X-Packaged-Version', 'Version']
        tocVersionDirectives = ['Interface']

        line = self.toc.readline()
        while line:
            line = line.strip()
            line = self._lchop(line, '\ufeff')

            m = directive_re.match(line)

            if m:
                if m.group(1) in titleDirectives:
                    self.name = m.group(2)
                
                if m.group(1) in versionDirectives:
                    self.version = m.group(2)

                if m.group(1) in tocVersionDirectives:
                    self.tocVersion = m.group(2)
            
            line = self.toc.readline()

        if not self.version:
            self.version="n/a"
        if not self.name:
            print("not enough information found for addon:\n{}").format(self.toString())

        self.name = self._removeStupidStuff(self.name)

    def toString(self):
        return "TOC metadata:\n---\n{}\n---\nParser output: (version={},name={},toc={})".format(self.toc.getvalue(), self.version, self.name, self.tocversion)

    def getName(self):
        return self.name

    def getVersion(self):
        return self.version

    def getTocVersion(self):
        return self.tocVersion
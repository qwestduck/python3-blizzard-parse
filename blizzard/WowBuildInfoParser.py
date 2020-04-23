class WowBuildInfoParser:
    def __init__(self, buildinfo):
        self.buildinfo = buildinfo
        self._parseHeaders()
        self._parseGames()

    def _rchop(self, s, suffix):
        if suffix and s.endswith(suffix):
            return s[:-len(suffix)]

        return s

    def _parseHeaders(self):
        self.headers = {}

        for h in self.buildinfo.readline().split('|'):
            l = h.split('!')
            r = l[1].split(':')
            self.headers[l[0]] = {}
            self.headers[l[0]]['type'] = r[0]
            self.headers[l[0]]['size'] = r[1]

    def _parseGames(self):
        self.games = {}

        line = self.buildinfo.readline()
        while line:
            game = line.split('|')
            i = 0
            g = {}
            for record in game:
                g[list(self.headers.keys())[i]] = record
                i += 1

            self.games[self._rchop(g["Product"], "\n")] = g
            line = self.buildinfo.readline()

    def toString(self):
        return str(self.games)

    def getTocVersion(self, product):
        v = self.games[product]["Version"].split('.')
        return str(int(v[0])*10000 + int(v[1])*100)
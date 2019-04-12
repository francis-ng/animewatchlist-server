import json

class WatchTitle:
    def __init__(self, data):
        self.user = data['user']
        self.title = data['title']
        self.season = data['season']
        self.isshort = 'false' if data['isShort'] == '' else data['isShort']
        self.start_date = None if data['startDate'] == '' else data['startDate']
        self.day = None if data['watchDay'] == '' else data['watchDay']
        self.source = None if data['channel'] == '' else data['channel']
        self.op = 'false' if data['op'] == '' else data['op']
        self.ed = 'false' if data['ed'] == '' else data['ed']
        self.other = None if 'others' not in data else data['others']
        self.watched = None if data['latestWatched'] == '' else data['latestWatched']
        self.bd = 'false' if data['bd'] == '' else data['bd']
        self.notes = None if 'remarks' not in data else data['remarks']

    def get_json(self):
        res = {
            'user': self.user,
            'title': self.title,
            'season': self.season,
            'isShort': self.isshort,
            'op': self.op,
            'ed': self.ed,
            'bd': self.bd,
        }

        if self.start_date:
            res.update({'startDate': self.start_date})

        if self.day:
            res.update({'watchDay': self.day})

        if self.source:
            res.update({'channel': self.source})

        if self.other:
            res.update({'others': self.other})

        if self.watched:
            res.update({'latestWatched': self.watched})

        if self.notes:
            res.update({'remarks': self.notes})

        return json.dumps(res)
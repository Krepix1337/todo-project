import json

def print_with_indent(value, indent=0):
    indentation = " " * indent
    print(indentation + str(value))


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    @classmethod
    def entry_from_json(cls, value: dict):
        new_entry = cls(value['title'])
        for item in value.get('entries', []):
            new_entry.add_entry(cls.entry_from_json(item))
        return new_entry

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)


class EntryManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.entries = []

    def load(self):
        import os
        folder = self.data_path
        for filename in os.listdir(folder):
            if filename.endswith(".json"):
                filepath = os.path.join(folder, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    entry = Entry.entry_from_json(data)
                    self.entries.append(entry)

my_entry = Entry('Продукты')
meet = Entry('Мясное')
my_entry.add_entry(meet)
kolbasa = Entry('Колбаса')
meet.add_entry(kolbasa)
my_entry.print_entries()

res = my_entry.json()

print(json.dumps(res, ensure_ascii=False, indent=4))
new_entry = Entry.entry_from_json(res)
new_entry.print_entries()

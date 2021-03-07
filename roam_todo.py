import re
import argparse
from dataclasses import dataclass
import datetime 
import parsedatetime
from pyroam import BlockContentKV, PageTag, KeyValue


class RoamTodo:
    """Roam Todo"""
    def __init__(self, block):
        self.block = block

    @property
    def scheduled(self):
        return self.block.get_kv("scheduled")
    @scheduled.setter
    def scheduled(self, date):
        self.block.set_kv("scheduled", date)

    @property
    def due(self):
        return self.block.get_kv("due")
    @due.setter
    def due(self, date):
        self.block.set_kv("due", date)

    @property
    def deferrals(self):
        return self.block.get_kv("deferrals", 0)
    @deferrals.setter
    def deferrals(self, num):
        self.block.set_kv("deferrals", num)

    @property
    def interval(self):
        return self.block.get_kv("interval", 0)
    @interval.setter
    def interval(self, num):
        self.block.set_kv("interval", num)

    @property
    def archived(self):
        archived = False
        for obj in self.block:
            if hasattr(obj, "title") and obj.title == "Archive":
                archived = True
                break
        return archived
    def archive(self):
        if self.archived:
            return
        self.block.append(PageTag("Archive"), add_whitespace=True) 
        self.block.append(PageTag(".strikethrough"), add_whitespace=True) 

    def schedule(self, new_scheduled):
        if self.scheduled:
            prev_scheduled = self.scheduled if type(self.scheduled) == datetime.date else self.scheduled.date()
            diff = (new_scheduled - prev_scheduled).days
            self.scheduled = new_scheduled
            if diff > 0:
                self.interval = diff
            self.deferrals += 1
        else:
            self.scheduled = new_scheduled

    def set_due(self, due):
        self.due = due

    def later(self, today=datetime.datetime.now().date()):
        self.interval = 2*self.interval if self.interval > 0 else 1
        self.scheduled = today + datetime.timedelta(days=self.interval)
        self.deferrals += 1

    def command(self, command):
        for cmd in self.split_command(command):
            if cmd == 'later':
                self.later()
            elif cmd == 'archive':
                self.archive()
            elif cmd == 'due to scheduled':
                self.due_to_scheduled()
            else:
                attr, date_string = self.parse_command(cmd)
                date = text_to_datetime(date_string).date()
                if attr=="due":
                    self.set_due(date)
                elif attr=="schedule":
                    self.schedule(date)
                else:
                    raise ValueError("Invalid command string")

    @staticmethod
    def parse_command(cmd):
        date_string = re.search("^scheduled?(?:\s*for\s*)?(.*)", cmd)
        if date_string:
            return "schedule", date_string.groups()[0]
        date_string = re.search("^due?(?:\s*on\s*)?(.*)", cmd)
        if date_string:
            return "due", date_string.groups()[0]
        return "schedule", cmd

    @staticmethod
    def split_command(command):
        return re.split("\s*and\s*|\s*,\s*", command) 

    @classmethod
    def from_string(cls, string):
        block = BlockContentKV.from_string(string)
        return cls(block)

    def to_string(self):
        return self.block.to_string()

    def __repr__(self):
        return repr(self.block)

    def due_to_scheduled(self):
        kv_due = self.block.get_kv_item("due")
        if kv_due:
            kv_due.key = "scheduled"


def text_to_datetime(text):
    cal = parsedatetime.Calendar()
    timetuple, _ = cal.parse(text)
    dt = datetime.datetime(*timetuple[:6])
    return dt


def main():
    parser = argparse.ArgumentParser(description='Process a todo')
    parser.add_argument('todo', type=str, help='Roam todo as text')
    parser.add_argument('command', type=str, help='Command on todo')
    args = vars(parser.parse_args())

    todo = RoamTodo.from_string(args["todo"])
    todo.command(args["command"])

    print(todo.to_string())


if __name__=="__main__":
    main()

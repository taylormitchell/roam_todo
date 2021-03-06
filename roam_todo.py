import argparse
from dataclasses import dataclass
import datetime 
import parsedatetime
from pyroam.content import BlockContentKV, PageTag


@dataclass
class Todo:
    """Roam Todo"""
    description: str
    due: datetime.date
    scheduled: datetime.date
    done: bool = False
    interval: int = 1
    deferrals: int = 0
    archived: bool = False

    def reschedule(self, date):
        self.scheduled = date
        self.deferrals += 1


        block_content.set_kv("schedule", self.__class__.__name__)
        interval = block_content.set_default_kv("interval", self.init_interval)
        due = dt.datetime.now() + dt.timedelta(days=interval)
        block_content.set_default_kv("due", due)

    def archive(self):
        self.archived = True

    def later(self, today=datetime.datetime.now().date()):
        self.interval *= 2
        self.scheduled = today + datetime.timedelta(days=self.interval)
        self.deferrals += 1

    def command(self, cmd):
        if cmd == 'later':
            self.later()
        elif cmd == 'archive':
            self.archive()
        else:
            date = text_to_datetime(cmd).date()
            self.reschedule(date)

    def __repr__(self):
        state = "DONE" if self.done else "TODO"
        return f"[{state}] {self.description} [scheduled: {self.scheduled}] [due: {self.due}] [archived: {self.archived}]"


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
    def deferrals(self):
        return self.block.get_kv("deferrals")
    @deferrals.setter
    def deferrals(self, num):
        self.block.set_kv("deferrals", num)

    @property
    def interval(self):
        return self.block.get_kv("interval")
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
        self.block.append(PageTag("Archive")) 
        self.block.append(PageTag(".strikethrough")) 

    def reschedule(self, new_scheduled):
        scheduled = self.scheduled if type(self.scheduled) == datetime.date else self.scheduled.date()
        diff = (new_scheduled - scheduled).days
        self.scheduled = new_scheduled
        self.deferrals += 1
        if diff > 0:
            self.interval = diff

    def later(self, today=datetime.datetime.now().date()):
        self.interval *= 2
        self.scheduled = today + datetime.timedelta(days=self.interval)
        self.deferrals += 1

    def command(self, cmd):
        if cmd == 'later':
            self.later()
        elif cmd == 'archive':
            self.archive()
        else:
            new_scheduled = text_to_datetime(cmd).date()
            self.reschedule(new_scheduled)

    @classmethod
    def from_string(cls, string):
        block = BlockContentKV.from_string(string)
        return cls(block)

    def to_string(self):
        return self.block.to_string()

    def __repr__(self):
        return repr(self.block)


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

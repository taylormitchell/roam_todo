import unittest
import datetime
from roam_todo import RoamTodo


class TestRoamTodo(unittest.TestCase):
    def test_schedule(self):
        todo = RoamTodo.from_string("{{[[TODO]]}} some todo")
        todo.schedule(datetime.datetime(2021, 3, 1))
        self.assertEquals(todo.to_string(), "{{[[TODO]]}} some todo #[[scheduled: 2021-03-01]]")
    
    def test_reschedule(self):
        todo = RoamTodo.from_string("{{[[TODO]]}} some todo #[[scheduled: 2021-03-01]]")
        todo.schedule(datetime.datetime(2021, 3, 2).date())
        self.assertEquals(todo.to_string(), "{{[[TODO]]}} some todo #[[scheduled: 2021-03-02]] #[[interval: 1]] #[[deferrals: 1]]")

    def test_multiple_commands(self):
        todo = RoamTodo.from_string("some todo")
        todo.command("due 7 days and scheduled for 3 days from now")
        res = todo.to_string() 

        today = datetime.datetime.now().date() 
        due_date = (today + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        sch_date = (today + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        expected = f"some todo #[[due: {due_date}]] #[[scheduled: {sch_date}]]"

        self.assertEqual(res, expected)


if __name__=="__main__":
    unittest.main()
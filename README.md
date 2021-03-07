# Roam Todo

Python script to manipulate Roam todos using natural language.

## Dependencies

- [parsedatetime](https://github.com/bear/parsedatetime)
- [pyroam](https://github.com/taylormitchell/pyroam)

## Examples

### Schedule todo
```
>>> python roam_todo.py "{{[[TODO]]}} some task" "schedule for tomorrow"
{{[[TODO]]}} some task #[[scheduled: 2021-03-08]]
```

### Reschedule todo
```
>>> python roam_todo.py "{{[[TODO]]}} some task #[[scheduled: 2021-03-08]]" "schedule for march 10th"
{{[[TODO]]}} some task #[[scheduled: 2021-03-10]] #[[interval: 2]] #[[deferrals: 1]]
```

### Reschedule todo for "later" 
Reschedule twice as far in the future as the last time it was reschedule. In the example above, the todo was rescheduled 2 days later. Rescheduling that same todo again using "later" reschedules it 4 days later.
```
>>> python roam_todo.py "{{[[TODO]]}} some task #[[scheduled: 2021-03-10]] #[[interval: 2]] #[[deferrals: 1]]" "later"
{{[[TODO]]}} some task #[[scheduled: 2021-03-14]] #[[interval: 4]] #[[deferrals: 2]]
```

### Schedule and set due date of todo
Example ran on March 7th
```
>>> python roam_todo.py "{{[[TODO]]}} some task" "due next week and schedule for tomorrow"
{{[[TODO]]}} some task #[[due: 2021-03-14]] #[[scheduled: 2021-03-08]]
```

### Archive todo
```
>>> python roam_todo.py "{{[[TODO]]}} some task" "archive"
{{[[TODO]]}} some task #Archive #.strikethrough
```

## Using todos in Roam

If today is March 7th, and we want to see all todos we have scheduled and/or due today or tomorrow, we can get a list of all those tasks with the following query:
```
{{[[query]]:{and: {or:[[due: 2021-03-07]][[due: 2021-03-08]][[due: 2021-03-07]][[due: 2021-03-08]]} {not:{or:[[DONE]][[Archive]]]}}}}}
```
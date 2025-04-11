# Discussion Grade Entry

This script helps you enter discussion grades and comments on a per-group basis, saving you the work of manually scrolling up and down the list of students.

# Usage

To use the script, first install the requirements:

```pip install -r requirements.txt```

Then, run the script with the following required arguments:

```
python3 .\enter_discussion_grades.py --ws_number WORKSHEET_NUMBER --section SECTION --group_netIDs netID1 netID2 netID3 ... --grade GRADE -- comment "comment1,comment2,..."
```

- `--ws_number`: the discussion worksheet number for which you are entering grades.
- `--section`: the section (e.g., AB3) for which you are entering grades.
- `--group_netIDs`: the netIDs of all the group members of the group you are entering grades for, to be entered as a space-separated list (e.g., netID1 netID2 ...).
- `--grade`: the grade to enter for all group members.
- `--comment`: the submission comment to enter for all group members, to be specified as a comma-separated list of comments without spaces (e.g., comment1,comment2,...); will transform comments into a bulleted list on separate lines.
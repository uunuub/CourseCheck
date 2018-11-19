# Course Check
Checks periodically for seat availability of courses.

## Running the script

```
Usage: class.py [options]

Options:
  -h, --help            show this help message and exit
  -r RECS, --receivers=RECS
                        file containing newline separated recipient emails
  -c COURSES, --courses=COURSES
                        file containing newline separated course names
```

## Requirements

* Script will be run under python2.7(Support for 3.6 will be added)
* All required packages in the requirements.txt.

## TODO:
### Short Term
* Functionality to get CRN given course name. Currently, it needs to be added manually.
* Support for different terms.
* Support for different interval 

### Long Term

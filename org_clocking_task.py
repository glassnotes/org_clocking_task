# -*- coding: utf-8 -*-
"""
Display the currently clocked-in task from emacs org-mode.

Configuration parameters:
    cache_timeout: refresh interval (default is 5)
    format: The text to be displayed before the current task. Default is 
        "Current task: " 

Requires:
    emacs
    org-mode

    emacs needs to be running with the server started.

Example:
```
org_clocking_task {
    color = "#00CCFF"
    format = "Working on: "
}
```

@author Olivia Di Matteo https://github.com/glassnotes
@license MIT 
"""

class Py3status:

    cache_timeout = 5
    format = "Current task: "

    def emacs_clock(self):
        display_string = self._get_clock_string()
        full_text = self.format + display_string
        return {
            'full_text' : full_text, 
            'cached_until' : self.py3.time_in(self.cache_timeout)
        }

    def _get_clock_string(self):
       
        # First check if we are clocking
        are_we_clocking = self.py3.command_output(["emacsclient", "--eval", "(org-clocking-p)"]).strip()

        if are_we_clocking == "t":
            raw_output = self.py3.command_output(["emacsclient", "--eval", "(org-clock-get-clock-string)"]).strip()
            clock_string = raw_output.split('\"')[1].strip()
            time, task = clock_string.split("] ")
            return task[1:-1] + " " + time +"]"
        else:   
            return "None"
  

if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)

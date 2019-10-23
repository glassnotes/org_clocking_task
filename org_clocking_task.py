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

from os import system

class Py3status:

    cache_timeout = 5
    format = "Current task: {task}"

    def post_config_hook(self):
        self.is_paused = False

    def org_clocking_task(self):
        display_string = self._get_clock_string()
        full_text = self.py3.safe_format(self.format, {'task' : display_string}) 
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
            if self.is_paused:
                return "PAUSED"
            else:   
                return "None"

    def on_click(self, event):  
        if event['button'] == 1:
            # If the button has been pressed, clock back in to the previously clocked task
            _ = self.py3.command_output(["emacsclient", "--eval", "(org-clock-in-last)"])
            self.is_paused = False
        elif event['button'] == 3:
            # If no button is set, clock out the current task and display the text for pause.
            _ = self.py3.command_output(["emacsclient", "--eval", "(org-clock-out)"])
            self.is_paused = True

if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)

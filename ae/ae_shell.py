import analytics_task_wrapper
import cmd
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

def handle_config(task_dict, cmd_list):
    task_name_index = 0
    cmd_index = task_name_index + 1
    arg_index = cmd_index + 1

    task_name = cmd_list[task_name_index]

    if task_name not in task_dict:
        return

    cmd = cmd_list[cmd_index]

    task = task_dict[task_name]

    if cmd == 'set_input_url':
        task.set_input_url(cmd_list[arg_index])
    elif cmd == 'add_output':
        task.add_output(cmd_list[arg_index])
    elif cmd == 'remove_output':
        task.remove_output(cmd_list[arg_index])

class AEShell(cmd.Cmd):
    prompt = 'AE> '
    task_dict = {}

    def do_EOF(self, line):
        return True

    def do_exit(self, line):
        return True

    def do_new(self, line):
        key = line.rstrip()
        self.task_dict[key] = analytics_task_wrapper.AnalyticsTaskWrapper(key)

    def do_list(self, line):
        for key in self.task_dict:
            self.task_dict[key].print_info()

    def do_config(self, line):
        cmd_list = line.rstrip().split()
        handle_config(self.task_dict, cmd_list)

    def do_run(self, line):
        key = line.rstrip()
        if key in self.task_dict:
            if not self.task_dict[key].is_running():
                self.task_dict[key].start()

    def do_delete(self, line):
        key = line.rstrip()
        if key in self.task_dict:
            self.task_dict[key].stop_task()
            self.task_dict[key].join()
            del self.task_dict[key]

if __name__ == '__main__':
    GObject.threads_init()
    Gst.init(None)
    AEShell().cmdloop()
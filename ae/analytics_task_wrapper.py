import analytics_pipe
import threading

class AnalyticsTaskWrapper(threading.Thread):
    name = ''
    in_url = ''
    output_list = []

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.in_url = ''
        self.output_list = []
        self.pipe = analytics_pipe.AnalyticsPipe(self.name)
        self.pipe_running = False

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_input_url(self, in_url):
        self.in_url = in_url
        self.pipe.set_input_url(in_url)

    def get_input_url(self):
        return self.in_url

    def add_output(self, output):
        self.output_list.append(output)

    def list_outputs(self):
        return self.output_list

    def remove_output(self, name):
        if name in self.output_list:
            self.output_list.remove(name)

    def stop_task(self):
        self.pipe.stop()
        self.pipe_running = False

    def print_info(self):
        print "Name: " + self.name
        print "Input URL: " + self.in_url
        print "Outputs: "
        for a in self.output_list:
            print a
        print '----------------'

    def run(self):
        if not self.pipe_running:
            self.pipe_running = True
            self.pipe.start()

    def is_running(self):
        return self.pipe_running

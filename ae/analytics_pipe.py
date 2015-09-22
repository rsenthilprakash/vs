import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, Gtk

class AnalyticsPipe(object):
    def __init__(self, id):
        self.id = id
        self.pipeline = Gst.Pipeline()
        self.uri = ''

        self.src = Gst.ElementFactory.make("rtspsrc", None)
        self.depay = Gst.ElementFactory.make("rtph264depay", None)
        self.dec = Gst.ElementFactory.make("avdec_h264", None);
        self.sink = Gst.ElementFactory.make("ximagesink", None);
        self.converter1 = Gst.ElementFactory.make("autovideoconvert", None);
        self.converter2 = Gst.ElementFactory.make("autovideoconvert", None);
        self.motioncells = Gst.ElementFactory.make("motioncells", None);

        self.pipeline.add(self.src)
        self.pipeline.add(self.depay)
        self.pipeline.add(self.dec)
        self.pipeline.add(self.sink)
        self.pipeline.add(self.converter1)
        self.pipeline.add(self.converter2)
        self.pipeline.add(self.motioncells)

        self.depay.link(self.dec)
        self.dec.link(self.converter1)
        self.converter1.link(self.motioncells)
        self.motioncells.link(self.converter2)
        self.converter2.link(self.sink)

        self.sink.set_property('sync', False)
        self.motioncells.set_property('postallmotion', True)

        self.src.connect('pad-added', self.on_pad_added)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::error', self.on_error)
        #self.bus.connect('message::element', self.on_element_message)

    def on_pad_added(self, element, pad):
        pad.link(self.depay.get_static_pad('sink'))

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        Gtk.main()

    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

    def on_eos(self, bus, msg):
        self.stop()

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())
        self.stop()

    def on_element_message(self, bus, msg):
        st = msg.get_structure()
        if st.has_name('motion'):
            (value_success, value) = st.get_int("numcells")
            if value_success:
                print("<{2}> Num Motion Cells: {0} at: {1}".format(value,
                                                                   st.get_string("motion_cells_indices"),
                                                                   self.id))

    def set_input_url(self, uri):
        self.uri = uri
        self.src.set_property('location', uri)


if __name__ == "__main__":
    GObject.threads_init()
    Gst.init(None)
    p = AnalyticsPipe(0)
    p.set_input_url("rtsp://127.0.0.1:8554/test")
    p.start()

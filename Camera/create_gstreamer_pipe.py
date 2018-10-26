#!/usr/bin/env python3

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
Gst.init(None)

def create_gstreamer_pipe():
    # create the elements:
    source = Gst.ElementFactory.make("fdsrc", "file-source")
    h264parse = Gst.ElementFactory.make("h264parse", "h264")
    avdec_h264 = Gst.ElementFactory.make("avdec_h264", "avdec_h264")
    sink = Gst.ElementFactory.make("appsink", "appsink")

    # create the pipeline:
    pipeline = Gst.Pipeline.new("drone-pipeline")
    pipeline.add(source)
    pipeline.add(h264parse)
    pipeline.add(avdec_h264)
    pipeline.add(sink)

    # link the elements:
    source.link(h264parse)
    h264parse.link(avdec_h264)
    avdec_h264.link(sink)

    sink.set_property("emit-signals", True)

    return pipeline, sink


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from sys import stdout

import pygtk
import os

pygtk.require('2.0')

import gtk
import pango

import gobject

from subprocess import Popen

class PomodoroTimer:

    def draw_timer(self):
        self.timer_label.set_text("%02d:%02d" % (self.timer / 60, self.timer % 60))

    def schedule_tick(self):
        gobject.timeout_add(1000, self.update_timer)

    def update_timer(self):
        if self.timer_state == "running":
            self.timer -= 1
            self.draw_timer()
            if self.timer == 0:

                Popen(['aplay', '-q', 'timeout.wav'])

                self.start_stop_button.set_label("Start")
                self.timer = self.initial_timer
                self.timer_state = "stop"
                self.draw_timer()
            else:
                self.schedule_tick()


    def __init__(self, initial_timer = 30 * 60):

        self.timer = initial_timer
        self.initial_timer = initial_timer
        self.timer_state = "stop"

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_title("Pomodoro timer")
        self.window.set_property("skip-taskbar-hint", True)
        self.window.set_property("resizable", False)
        self.window.set_keep_above(True)

        self.window.connect("destroy", self.on_destroy)
        self.window.set_border_width(10)

        self.vbox = gtk.VBox(False, 0)
        self.window.add(self.vbox)


        self.start_stop_button = gtk.Button("Start")
        self.start_stop_button.connect("clicked", self.on_start_stop_clicked, None)

        self.pause_resume_button = gtk.Button("Resume")
        self.pause_resume_button.connect("clicked", self.on_pause_resume_clicked, None)

        self.timer_label = gtk.Label("XX:XX")
        self.timer_label.modify_font(pango.FontDescription("Bitstream Vera Sans 18"))
        self.timer_label.set_alignment(0.5, 0)

        self.hbox = gtk.HBox(False, 0);

        self.vbox.pack_start(self.timer_label, True, True, 0)
        self.vbox.pack_start(self.hbox, True, True, 0);

        self.hbox.pack_start(self.start_stop_button, True, True, 0)
        self.hbox.pack_start(self.pause_resume_button, True, True, 0)

        self.draw_timer()

        self.pause_resume_button.hide()
        self.start_stop_button.show()
        self.timer_label.show()
        self.hbox.show()
        self.vbox.show()
        self.window.show()

    def on_start_stop_clicked(self, widget, data=None):
        if self.timer_state == "stop":
            self.start_stop_button.set_label("Stop")
            self.timer_state = "running"
            self.timer = self.initial_timer

            self.pause_resume_button.hide();

            self.update_timer()
        elif self.timer_state == "running":
            self.start_stop_button.set_label("Reset")
            self.timer_state = "paused"

            self.pause_resume_button.show();

        elif self.timer_state == "paused":
            self.start_stop_button.set_label("Start")

            self.pause_resume_button.hide();

            self.timer_state = "stop"
            self.timer = self.initial_timer
            self.draw_timer()

    def on_pause_resume_clicked(self, widget, data=None):
        self.start_stop_button.set_label("Stop")
        self.timer_state = "running"
        self.pause_resume_button.hide();
        self.update_timer();

    def on_destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()


if __name__ == "__main__":
    dirname = os.path.dirname(sys.argv[0])
    try:
        dirname = os.path.dirname(os.readlink(sys.argv[0]))
    except OSError:
        pass
    os.chdir(dirname)

    interval_s = 30 * 60
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            interval_s = 3
        else:
            try:
                interval_s = 60 * float(sys.argv[1])
            except:
                pass
    pt = PomodoroTimer(interval_s)
    pt.main()




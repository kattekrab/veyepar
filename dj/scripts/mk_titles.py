#!/usr/bin/python

# creates svg titles for all the episodes
# used to preview the title slides, 
# enc.py will re-run the same code.

import os
import subprocess

import rax_uploader

from enc import enc

from main.models import Client, Show, Location, Episode, Raw_File, Cut_List

class mk_title(enc):

    ready_state = None

    def process_ep(self, episode):

        title_img=self.mk_title(episode)

        if self.options.rsync:
            self.file2cdn(episode.show, "titles/%s.png" % (episode.slug))
            self.file2cdn(episode.show, "titles/%s.svg" % (episode.slug))
            self.file2cdn(episode.show, "tmp/%s.mlt" % (episode.slug))
            self.file2cdn(episode.show, "tmp/%s.sh" % (episode.slug))
            return 

        if self.options.display:
            png_name = u"{}/titles/{}.png".format(
                    self.show_dir, episode.slug)
            self.run_cmd(['display', png_name])

        return False # not sure what this means.. we don't bump state

    def add_more_options(self, parser):
        parser.add_option('--rsync', action="store_true",
            help="upload to DS box.")
        parser.add_option('--display', action="store_true",
            help="display the png.")

if __name__ == '__main__':
    p=mk_title()
    p.main()


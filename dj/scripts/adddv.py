#!/usr/bin/python

# Adds the .dv files to the raw files table

import  os

from process import process

from main.models import Client, Show, Location, Episode, Raw_File, Cut_List

class add_dv(process):

    def one_file(self,pathname,show,location,seq):
        print pathname,
        if self.options.test:
            rfs = Raw_File.objects.filter(
                show=show, location=location,
                filename=pathname,)
            if rfs: print "in db:", rfs
            else: print "not in db"
        else:
            rf, created = Raw_File.objects.get_or_create(
                show=show, location=location,
                filename=pathname,)
            
            if created: 
               print "(new)"
               rf.sequence=seq

               fullpathname = os.path.join(
                       self.show_dir, "dv", location.slug, pathname )
               st = os.stat(fullpathname)    
               rf.filesize=st.st_size

               rf.save()
            else:
               print "(exists)"
   
    def one_loc(self,show,location):
      """
      finds dv files for this location
      """
      if self.options.whack:
          Raw_File.objects.filter(show=show).delete()

      ep_dir=os.path.join(self.show_dir,'dv',location.slug)
      if self.options.verbose:  print "episode dir:", ep_dir
      seq=0
      for dirpath, dirnames, filenames in os.walk(ep_dir,followlinks=True):
          d=dirpath[len(ep_dir)+1:]
          if self.options.verbose: 
              print "checking...", dirpath, d, dirnames, filenames 
          for f in filenames:
              if os.path.splitext(f)[1] in [
                      '.dv', '.flv', '.mp4', '.MTS', '.mkv', '.mov' ]:
                  seq+=1
                  self.one_file(os.path.join(d,f),show,location,seq)

    def one_show(self, show):
      if self.options.whack:
          Raw_File.objects.filter(show=show).delete()
      return super(add_dv, self).one_show(show)

    def work(self):
        """
        find and process show
        """
        if self.options.client and self.options.show:
            client = Client.objects.get(slug=self.options.client)
            show = Show.objects.get(client=client, slug=self.options.show)
            self.one_show(show)

        return

if __name__=='__main__': 
    p=add_dv()
    p.main()


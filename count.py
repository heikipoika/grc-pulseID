"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import sys
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='count',   # will show up in GRC
            in_sig=[np.int8],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.pos = 0

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        
        self.pos = 0
        lgth = len(input_items[0])
        
        while self.pos < lgth:
            
            off = np.nonzero(input_items[0][self.pos:])
            if len(off[0]) > 0:
                offs = off[0][0]
                cn = np.nonzero(input_items[0][self.pos+offs:] == 0)
                if len(cn[0]) > 0:
                    cnt = cn[0][0]
                    self.pos = self.pos + offs + cnt
                else:
                    done = 0
                    break
            else:
                done = 1
                break
            sys.stdout.write("res %i \n" % (cnt))
        #print("done ", done)
        
        return len(input_items[0])

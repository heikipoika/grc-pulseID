"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import sys
import pmt
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, chan=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='counter',   # will show up in GRC
            in_sig=[np.int8],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = 0
        self.prev = 0
        self.chan = chan
        self.message_port_register_out(pmt.intern('msg_out'))

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        if np.any(input_items[0][:] > 0):
            for i in range (1, len(input_items[0])):
                if (self.prev == 0) and (input_items[0][i] == 1):
                    self.example_param = 1
                if (self.prev == 1):
                    self.example_param = self.example_param + 1
                if (self.prev == 1 and input_items[0][i] == 0):
                    sys.stdout.write("%i: %i \n" % (self.chan, self.example_param))
                    self.message_port_pub(pmt.intern('msg_out'), pmt.from_long(self.chan))
                self.prev = input_items[0][i]
            
        #output_items[0][:] = self.example_param
        return len(input_items[0])

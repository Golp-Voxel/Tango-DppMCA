# -*- coding: utf-8 -*-
#
# This file is part of the DppMCA project
#
#
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.

"""
Voxel

"""

# PROTECTED REGION ID(DppMCA.system_imports) ENABLED START #
# PROTECTED REGION END #    //  DppMCA.system_imports

# PyTango imports
import tango
from tango import DebugIt
from tango.server import run
from tango.server import Device
from tango.server import attribute, command
from tango.server import device_property
from tango import AttrQuality, DispLevel, DevState
from tango import AttrWriteType, PipeWriteType
# Additional import
# PROTECTED REGION ID(DppMCA.additionnal_import) ENABLED START #
import usb # to_install folder has the modules
import codecs # to_install folder has the modules
import struct
# PROTECTED REGION END #    //  DppMCA.additionnal_import

__all__ = ["DppMCA", "main"]


class DppMCA(Device):
    """

    **Properties:**

    - Device Property
        VENDOR
            - Vendor ID
            - Type:'str'
        PRODUCT
            - Product ID
            - Type:'str'
    """
    # PROTECTED REGION ID(DppMCA.class_variable) ENABLED START #
    LIBUSB_TIMEOUT = 500

    REQUEST_STATUS_PACKET = bytes.fromhex('F5FA01010000FE0F')              # Request Status Packet
    REQUEST_SPECTRUM_PACKET = bytes.fromhex('F5FA02010000FE0E')            # Request Spectrum Packet
    REQUEST_SPECTRUM_STATUS_PACKET = bytes.fromhex('F5FA02030000FE0C')     # Request Spectrum Status Packet

    CLEAR_SPECTRUM_BUFFER = bytes.fromhex('F5FAF0010000FD20')              # Clear Spectrum Buffer
    ENABLE_MCA_MCS = bytes.fromhex('F5FAF0020000FD1F')                     # Enable MCA MCS
    DISABLE_MCA_MCS = bytes.fromhex('F5FAF0030000FD1E')                    # Disable MCA MCS

    ACK_RESPONSE = bytes.fromhex('F5FAFF000000FD12')                       # Ack 0 response, message is OK
    CONFIGURATION = 1
    INTERFACE = 0
    ENDPOINT_IN = 0x81
    ENDPOINT_OUT = 0x02
    device_Dpp = None
    handle = None
    # PROTECTED REGION END #    //  DppMCA.class_variable

    # -----------------
    # Device Properties
    # -----------------

    VENDOR = device_property(
        dtype='str',
        doc="Vendor ID"
        mandatory=True
    )

    PRODUCT = device_property(
        dtype='str',
        doc="Product ID"
        mandatory=True
    )

    # ----------
    # Attributes
    # ----------

    Spectrum = attribute(
        dtype=('DevDouble',),
        max_dim_x=8000,
    )

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        """Initializes the attributes and properties of the DppMCA."""
        Device.init_device(self)
        self._spectrum = (0.0,)
        # PROTECTED REGION ID(DppMCA.init_device) ENABLED START #
        for bus in usb.busses():
            for dev in bus.devices:
                if dev.idVendor == self.VENDOR and dev.idProduct == self.PRODUCT:
                    # print(VENDOR)
                    # print(PRODUCT)
                    self.device_Dpp = dev


        self.handle = self.device_Dpp.open()
        self.handle.setConfiguration(self.CONFIGURATION)
        self.handle.claimInterface(self.INTERFACE)
        # PROTECTED REGION END #    //  DppMCA.init_device

    def always_executed_hook(self):
        """Method always executed before any TANGO command is executed."""
        # PROTECTED REGION ID(DppMCA.always_executed_hook) ENABLED START #
        # PROTECTED REGION END #    //  DppMCA.always_executed_hook

    def delete_device(self):
        """Hook to delete resources allocated in init_device.

        This method allows for any memory or other resources allocated in the
        init_device method to be released.  This method is called by the device
        destructor and by the device Init command.
        """
        # PROTECTED REGION ID(DppMCA.delete_device) ENABLED START #
        # PROTECTED REGION END #    //  DppMCA.delete_device

    # ------------------
    # Attributes methods
    # ------------------

    def read_Spectrum(self):
        # PROTECTED REGION ID(DppMCA.Spectrum_read) ENABLED START #
        """Return the Spectrum attribute."""
        iNumBytes = self.write_to_buff(self.REQUEST_SPECTRUM_STATUS_PACKET, self.LIBUSB_TIMEOUT)
        print( 'Bytes Out =',iNumBytes)     # debug
        bArrArrBuffer = self.read_to_buff(6216, self.LIBUSB_TIMEOUT)
        bArrStatusIn = bytearray(bArrArrBuffer)

        # print type(self.bArrStatusIn)
        # print self.bArrStatusIn.encode('hex')
        if len(bArrStatusIn) > 0:
            Header = bytearray(bArrStatusIn[0:5])
            bPID2 = Header[3]           
            Channels = 256 *  ( 2 **  ( ( ( bPID2 - 1 )  & 14 )  // 2 ) )
            print ("Channels Calc ", (Channels))
            DataRaw = bytearray(bArrStatusIn[6:Channels*3+6])
        Data=[]
        print(len(DataRaw))
        print(len(DataRaw)/3)
        for X in range(0,int(Channels)*3,3):
            Data.append((DataRaw[X]) + (DataRaw[X + 1]) * 256 + (DataRaw[X + 2]) * 256**2)
        self._spectrum = Data
        return self._spectrum
        # PROTECTED REGION END #    //  DppMCA.Spectrum_read
    # --------
    # Commands
    # --------


# ----------
# Run server
# ----------

# PROTECTED REGION ID(DppMCA.custom_code) ENABLED START #
    def write_to_buff( buffer, timeout = 0):
            return self.handle.bulkWrite(self.ENDPOINT_OUT, buffer, timeout)

    def read_to_buff(length, timeout = 0):
            return self.handle.bulkRead(self.ENDPOINT_IN, length, timeout)
# PROTECTED REGION END #    //  DppMCA.custom_code


def main(args=None, **kwargs):
    """Main function of the DppMCA module."""
    # PROTECTED REGION ID(DppMCA.main) ENABLED START #
    return run((DppMCA,), args=args, **kwargs)
    # PROTECTED REGION END #    //  DppMCA.main

# PROTECTED REGION ID(DppMCA.custom_functions) ENABLED START #
# PROTECTED REGION END #    //  DppMCA.custom_functions


if __name__ == '__main__':
    main()

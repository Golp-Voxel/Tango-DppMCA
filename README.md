# Amptek DP5 Digital Pulse Processor (DppMCA) - Tango Device Server

This repository contains the driver for reading the spectrum of an Amptek DP5 Digital Pulse Processor / Multichannel Analyzer (MCA) with the Tango Control. The communication with the device is done directly over USB (`pyusb`) using the Amptek packet protocol.

## Installation

After cloning this repository with the following command

```
git clone https://github.com/Golp-Voxel/Tango-DppMCA.git
```

It is necessary to create the `tango-env` using the following command:

```
python -m venv tango-env
```

After activating it, install `pytango` and the modules in the `to_install` folder (`pyserial` and `pyusb`):

```
pip install to_install\pyserial-3.5.tar.gz
pip install to_install\pyusb-1.0.0a2.zip
```

To complete the installation, it is necessary to copy the `Dpp.bat.temp` template, remove the `.temp`, and change the paths to the installation folder. And the command to activate the env created `tango-env\Scripts\activate`.

## Device Properties

When registering the device on the Tango Database, the following properties are **mandatory**:

- `VENDOR` - the USB Vendor ID of the device.
- `PRODUCT` - the USB Product ID of the device.

On `init_device` the server scans the USB buses for a device matching `VENDOR`/`PRODUCT` and claims its interface.

## Attributes

### Spectrum

Read-only spectrum attribute (`DevDouble`, up to 8000 channels). Reading this attribute sends the *Request Spectrum Status Packet* to the device, decodes the number of channels from the response header, and returns the counts of each channel.

```python
spectrum = DppMCA_Device.Spectrum
```

## Example of Tango Client code

```python
import tango
import matplotlib.pyplot as plt

DppMCA_Device = tango.DeviceProxy(<DppMCA_Tango_location_on_the_database>)
print(DppMCA_Device.state())

spectrum = DppMCA_Device.Spectrum
plt.plot(spectrum)
plt.xlabel("Channel")
plt.ylabel("Counts")
plt.show()
```

The notebook [`test/Dpp.ipynb`](test/Dpp.ipynb) contains a test of the communication with the device. The `doc_html` folder contains the Pogo generated documentation of the Tango class.

# References

- SDK: [Amptek DP5 Digital Pulse Processor Software - Python downloads](https://www.amptek.com/software/dp5-digital-pulse-processor-software/python-downloads)
- Message manual: [Amptek Digital Products Programmer's Guide](https://www.amptek.com/-/media/ametekamptek/documents/resources/products/user-manuals/amptek-digital-products-programmers-guide-b3.pdf?la=en&revision=1c16e5f8-448a-4fbb-a619-888600356971&hash=A94AE3AA759CA497018281C0A89848F7)

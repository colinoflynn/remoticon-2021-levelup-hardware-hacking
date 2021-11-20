# Rasperry Pi Glitching Examples

These are run on a "R-Pi 3 Model B+".

The base image was "Raspberry Pi OS (32-Bit), Released 2021-10-30".

## Glitch Loop


## RSA Glitching

This file is based on a [ChipWhisperer DFA tutorial](https://github.com/newaetech/chipwhisperer-jupyter/blob/master/courses/fault201/SOLN_Lab%202_1%20-%20Fault%20Attack%20on%20RSA.ipynb). You'll find this also detailed in the [Hardware Hacking Handbook](nostarch.com/hardwarehacking) which details a different derivation of how the fault attack works.

The description of the fault attack in the ChipWhisperer lab follows a blog post from [David Wong](https://www.cryptologie.net/article/371/fault-attacks-on-rsas-signatures/), who also wrote the great [Real World Cryptography](https://www.manning.com/books/real-world-cryptography) book.

This requires you to insert a glitch during the signing operation. To do this we'll use `pycryptodome`, but we're using an old version as current versions have fault protection which you can see [at this line for example](https://github.com/Legrandin/pycryptodome/blob/v3.11.0/lib/Crypto/PublicKey/RSA.py#L171). The protection is to perform a validation that the generated signature validates OK. Note you can bypass that with a more targeted fault injection attack.

To run `rsaglitch.py` you'll need to install pycryptodome 3.1 and an accelerated library to perform the factoring. This can be done with:

```
pip install pycryptodome==3.1
sudo apt-get install python3-gmpy2
 ```

## Voltage Glitching

If you want to run voltage glitching from the Raspberry Pi itself, you can connect a ChipWhisperer-Lite. This will require you to install ChipWhisperer and fix a few packages on the R-Pi default install:

```
pip install chipwhisperer
pip install -U numpy
sudo apt-get install libilmbase-dev
sudo apt-get install libatlas-base-dev
 ```

You'll need to setup the `udev` file as normally required for a [Linux install](https://chipwhisperer.readthedocs.io/en/latest/prerequisites.html#prerequisites-linux), see the or the lazy instructions:

```
sudo bash -c 'printf "SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"2b3e\", ATTRS{idProduct}==\"*\", TAG+=\"uaccess\"\\n" >> /etc/udev/rules.d/50-newae.rules'
sudo bash -c 'printf "SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"2b3e\", ATTRS{idProduct}==\"*\", TAG+=\"uaccess\", SYMLINK+=\"cw_serial%n\"\\n" >> /etc/udev/rules.d/50-newae.rules'
sudo bash -c 'printf "SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"03eb\", ATTRS{idProduct}==\"6124\", TAG+=\"uaccess\", SYMLINK += \"cw_bootloader%n\"\\n" >> /etc/udev/rules.d/50-newae.rules'
sudo udevadm control --reload-rules
sudo usermod -a -G dialout $USER
```
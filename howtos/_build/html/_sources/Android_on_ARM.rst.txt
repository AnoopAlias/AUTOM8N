Install LineageOS on ARM
==========================

Here I will describe how one can upgrade the Android operating system on the ARM computer architecture. This howto is specific for the

Motorola Moto G falcon ,but the methodology and basics will be similar for any supported ARM based mobile phone

Please read : https://community.nxp.com/docs/DOC-102546

Step-1- Install the required tools on your Ubuntu PC
-----------------------------------------------------

We need to install the Android Debug Bridge (adb) and Android fastboot tool (fastboot)
::

  sudo apt-get install adb fastboot

Step-2 - Enable developer options and enable USB debugging in developer options
--------------------------------------------------------------------------------

Under Settings >> About Phone >> Tap build number 7 times to enable Developer options
Settings >> Turn on USB debugging under Developer options
Settings >> Enable OEM unlock in the Developer options settings on the device

Step-3 - Unlock the bootloader
--------------------------------
The bootloader is a piece of code that runs before Android and is provided by the device manufacturer,which in this case is Motorola

The manufacturer would have placed special locks to prevent installation of 3rd party software and would in most cases also have provided

ways to circumvent this. For Motorola phones We can obtain the bootloader unlock key online at

https://motorola-global-portal.custhelp.com/app/standalone%2Fbootloader%2Funlock-your-device-b

Ensure debugging mode is on and connect your phone via USB to your Ubuntu PC and run

::

  sudo adb devices

If everything is good you will see the devices serial number listed

Put your device in fastboot mode (power off, then press the power and volume down buttons simultaneously)

and on your Ubuntu PC run
::

  sudo fastboot oem get_unlock_data

Paste together the 5 lines of output into one continuous string without (bootloader) or ‘INFO’ or white spaces. Your string needs to look like this:
0A40040192024205#4C4D355631323030373731363031303332323239#BD008A672BA4746C2CE02328A2AC0C39F951A3E5#1F532800020000000000000000000000 at Motorola website

and run
::

  sudo fastboot oem unlock UNIQUE_KEY

where UNIQUE_KEY is what you obtain from Motorola website

Your phones bootloader is now unlocked and you will be able to install 3rd party programs on your phone

Step-4 - Install a custom Recovery
--------------------------------------
TO install a custom Android ROM like LineageOS you will need to install a custom Recovery than your stock recovery provided by Android.
The recovery is how you can wipe your phone to factory reset ,how the manufacturer helps you flash OTA updates etc. But for custom ROM's you will need more
options than whats available in stock recovery and use a custom recovery

There are many third party custom recovery programs. Here we will install the Teamwin Recovery Project (TWRP)

You will need to flash the TWRP recovery program suited for your device - https://twrp.me/Devices/

For falcon I will download https://dl.twrp.me/falcon/twrp-3.0.2-2-falcon.img
::

  sudo adb reboot bootloader
  sudo fastboot flash recovery twrp-3.0.2-2-falcon.img
  sudo fastboot reboot

You will find that the stock recovery is now replaced with TWRP and it accepts touch input too

Step-5- Download and push the LineageOS flash images to your Phone
---------------------------------------------------------------------------------

For example I would download the latest nightly from https://download.lineageos.org/falcon
Also for using PlayStore and for obtaining other Google Apps download  - http://opengapps.org/

Choose ARM >> Android (version compatible with your Lineage OS .For example Android 7.1 for LineageOS 14.1 )

Once you have downloaded both files above, uplod it to your Phone
::

  sudo adb push open_gapps-arm-7.1-pico-20170128.zip /sdcard/
  sudo adb push lineage-14.1-20170124-nightly-falcon-signed.zip /sdcard/

Step-6 - Install or flash the LineageOS ROM image from the TWRP console
--------------------------------------------------------------------------
::

  If you aren’t already in recovery, boot into recovery:
  Hold Volume Down & Power simultaneously. On the next screen use Volume Down to scroll to recovery and then use Volume Up to select.
  (Optional, but recommended): Select the Backup button to create a backup.
  Select Wipe and then Advanced Wipe.
  Select Cache, System and Data partitions to be wiped and then Swipe to Wipe.
  Go back to return to main menu, then select Install.
  Navigate to /sdcard, and select the LineageOS .zip package.
  Follow the on-screen prompts to install the package.
  (Optional): Install open_gapps packages using the same method.
  Once installation has finished, return to the main menu, select Reboot, and then System.

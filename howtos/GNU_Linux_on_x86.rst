Installation of ArchLinux on x86
=====================================

This guide describes ArchLinux installation on a modern computer via USB bootable medium . The network is provided by the modem (4G) on an Android device via Wifi HotSpot

Prepare the bootable install medium
-------------------------------------
Download ( https://www.archlinux.org/download/ ) and write the image onto the USB drive
::

  dd bs=4M if=/path/to/archlinux.iso of=/dev/sdx status=progress && sync

once this is done .Boot the machine you will be installing the OS using the USB drive. ArchLinux will boot up and provide you with a root shell

Setup WIFI Networking
-----------------------
::

  ip link

Will show the network adaptor. It was named ``wlp5so`` in my case
::

  ip link set wlp5s0 up

The following command will show available networks .Look for the SSID row
::

  iw dev wlp5s0 scan|less

Android Wifi Hostspot is normally WPA/WPA2 encrypted which rquire the wpa_supplicant daemon to connect
Run the following single line command .Replace hotspot name and password with whats yours.
::

  wpa_supplicant -B -D nl80211,wext -i wlp5s0 -c <(wpa_passphrase "AndoidHotspot" "my_secure_password")

Run the dhcpcd to manage the IP lease from your hotspot
::

  dhcpcd wlp5s0

Ensure ping and domain name resolution works

Update system clock
----------------------
::

  timedatectl set-ntp true

Partition the disk
----------------------
I will create a single ext4 partition and setup a GUID partition table. The laptop I am using has Legacy BIOS and not UEFI or I in short i will use BIOS+GPT .Your method may vary with UEFI+GPT or BIOS+MBR
Since my bootloader is GRUB,I will also need something called a BIOS boot partition .Note that this is not needed in BIOS+MBR scheme as MBR has fixed size and GRUB can embed its core.img after
this fixed size .
::

  parted

  (parted)mklabel gpt
  (parted)unit Mib
  (parted)mkpart 1 1 2             #creates partition 1 with 1Mib size from 1Mib to 2Mib
  (parted)set 1 bios_grub on
  (parted)mkpart ext4 2 100%       #creates a single partition that extends to the full disk space
  (parted)quit

Create the ext4 filesystem on the block device which will hold your files
::

  mkfs.ext4 /dev/sda2      #assuming sda2 is the partition where you will b installing linux

Mount the block device to /mnt for installing Linux
::

  mount /dev/sda2 /mnt

Bootstrap Archlinux into the block device
--------------------------------------------
::

  pacstrap /mnt base         #This is the bare minimum

Generate fstab entries for the new installation
--------------------------------------------------
::

  genfstab -U /mnt >> /mnt/etc/fstab

Its time to chroot to the new install and configure
----------------------------------------------------
::

  arch-chroot /mnt

Set time-zone, locale, keyboard layout, hostname,root password
::

  #Set timezone
  ln -sf /usr/share/zoneinfo/Region/City /etc/localtime

  #Uncomment en_US.UTF-8 UTF-8 and other needed localizations in /etc/locale.gen, and generate them with:
  locale-gen

  #Set the LANG variable in locale.conf(5) accordingly, for example:
  echo "LANG=en_US.UTF-8" >> /etc/locale.conf

  #Set the keymap
  echo "KEYMAP=us" >> /etc/vconsole.conf

  #Set the hostname
  echo "thinkpad.gnusys.net" >> /etc/hostname

  #Set root password
  passwd

We install some additional packages required for networking to work that was not included in the pacstrapping of base
::

  pacman -S iw wpa_supplicant dialog wpa_actiond
  wifi-menu
  systemctl enable netctl-auto@wlp5s0.service

Initramfs is normally automatically created when the linux package is installed with pacstrap in the chroot
::

  mkinitcpio -p linux  #not needed as the initramfs is already created as mentioned above

Install the BootLoader
-------------------------

Install grub and run grub-install
::

  pacman -S grub
  grub-install --target=i386-pc /dev/sda    #Assuming /dev/sda is your harddrive
  grub-mkconfig -o /boot/grub/grub.cfg

Reboot into the new installation
--------------------------------------
::

  exit  #exit from chroot
  reboot

You should now be rebooted into the new ArchLinux installation with a working network. You can now proceed to install
additional software and a GUI . There are multiple choices of Desktop Environments available https://wiki.archlinux.org/index.php/desktop_environment

Install a Desktop Environment
-------------------------------------
::

  pacman -S gnome gnome-extra
  pacman -S firefox noto-fonts  #change firefox font to noto from firefox settings
  systmctl enable gdm

Thats it . Enjoy your ArchLinux Gnome3 Desktop after a reboot

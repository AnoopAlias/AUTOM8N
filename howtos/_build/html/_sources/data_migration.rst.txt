Data Migration Specifc notes
===============================

To move data between lan machines with low overhead
------------------------------------------------------

1.Start a listener on the target machine with nc
::

  nc -l 1234 | dd of=/dev/data/kvm121_img bs=16M

2. Send data from the source machine to the listener above
::

  pv /dev/data/kvm121_img |nc 1.2.3.4 1234

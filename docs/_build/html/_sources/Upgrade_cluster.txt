XtendWeb cluster upgrade
=========================

On All slaves
-------------

::

  yum --enablerepo=ndeploy upgrade

On master
---------

::

  yum --enablerepo=ndeploy upgrade
  cd /opt/nDeploy/conf/nDeploy-cluster
  ansible-playbook -i ./hosts cluster.yml

.. disqus::

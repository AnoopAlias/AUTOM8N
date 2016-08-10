nDeploy cluster upgrade
=======================

On All slaves
-------------

::

  yum --enablerepo=ndeploy install unison-nDeploy csync2-nDeploy nDeploy-cluster-slave nginx-nDeploy

On master
---------

::

  yum --enablerepo=ndeploy install unison-nDeploy csync2-nDeploy nDeploy nginx-nDeploy
  cd /opt/nDeploy/conf/nDeploy-cluster
  ansible-playbook -i ./hosts cluster.yml

.. disqus::

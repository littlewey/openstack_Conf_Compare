# Description
Parse conf by oslo_config and compare all conf files under two folders, typically for two cloud nodes' compare audit usage.

# Installation

This tool was only tested on Ubuntu 16.04.1 LTS while it should be working on any Unix-like environment.

A virtual env was included to make it works out of box, thus you could install it just from git via below command:

```bash
$ git clone https://github.com/littlewey/openstack_Conf_Compare
```

> note, if git is not installed, install it

```bash
// in Debian, Ubuntu etc.

$ sudo apt-get install git

// or in Redhat flavor Linux/

$ yum install git
```



# How to use

Run `configCompare.sh` with two folders' path to be compared
```bash
$ cd openstack_Conf_Compare
$ ./configCompare.sh <path of Folder A> <path of Folder B>
```
> Typical use case

Collect `neutron` and `nova` configuration files for all nodes in one Mirantis Openstack

```bash
for h in $(fuel node | grep ready |awk '{print $5}'); do echo $h; mkdir -p /tmp/confFetch/$h ; rsync -chavzP $h:/etc/nova /tmp/confFetch/$h/; done
for h in $(fuel node | grep ready |awk '{print $5}'); do echo $h; mkdir -p /tmp/confFetch/$h ; rsync -chavzP $h:/etc/neutron /tmp/confFetch/$h/; done
```
After transferring files to local machine with our tool installed, run compare, for example do compare of compaute-0-1 with compute-1-6.

```
$ ./configCompare.sh /media/confFetch/compute-1-6 /media/confFetch/compute-0-1
[OK] configCompare started ...
Different file nova.conf found in /media/confFiles/compute-1-6/nova and /media/confFiles/compute-0-1/nova
['diff', "['vnc', 'vncserver_listen', 0]", '192.168.2.31,', '192.168.2.43,']
['diff', "['vnc', 'vncserver_proxyclient_address', 0]", '192.168.2.31,', '192.168.2.43,']
['diff', "['DEFAULT', 'vcpu_pin_set', 0]", '', '3-13,17-27,']
['diff', "['DEFAULT', 'reserved_memory_pages', 0]", '0:1GB:53,', '']
['diff', "['DEFAULT', 'my_ip', 0]", '192.168.2.31,', '192.168.2.43,']
['diff', "['DEFAULT', 'reserved_host_disk_mb', 0]", '1425408,', '0,']
['leftMiss', 'reserved_huge_pages', 'NOTHING HERE', "['node:0,size:1GB,count:50']"]
['diff', "['cache', 'memcache_servers', 0]", '192.168.2.31:11211,', '192.168.2.43:11211,']

```
You could also do compare between two Openstack system's node.

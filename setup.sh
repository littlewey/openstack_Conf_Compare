source env/bin/activate.sh
git clone https://github.com/openstack/oslo.config
ln -s oslo_cfg oslo.config/oslo_cfg
pip install debtcollector netaddr rfc3986 dictdiffer

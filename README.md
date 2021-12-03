## Python Library for [Vultr](https://www.vultr.com/) API

The unofficial python library for the Vultr API.

[![CI](https://github.com/luxiaba/pyvultr/actions/workflows/ci.yaml/badge.svg)](https://github.com/luxiaba/pyvultr/actions/workflows/ci.yaml)
[![PyPI](https://img.shields.io/pypi/v/pyvultr?color=blue&label=PyPI)](https://pypi.org/project/pyvultr/)

[![Python 3.6.8](https://img.shields.io/badge/python-3.6.8-blue.svg)](https://www.python.org/downloads/release/python-368/)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


### Installation
```
pip install -U pyvultr
```

### Usage

#### Configuration
```python
from pyvultr import VultrV2

# Set your api key or we'll get it from env `VULTR_API_KEY`.
VULTR_API_KEY = '...'

v2 = VultrV2(api_key=VULTR_API_KEY)
```

#### Get Account
```python
account = v2.account.get()
print(account)
```

#### List Region
```python
regions: VultrPagination[BackupItem] = v2.region.list()

# Here `regions` is a VultrPagination object, you can use it like list, eg: get by index or slice.
# VultrPagination will help you automatically get the next page when you need it.

print(regions[3:5])
# >>> [RegionItem(id='dfw', country='US', options=['ddos_protection'], continent='North America', city='Dallas'), RegionItem(id='ewr', country='US', options=['ddos_protection', 'block_storage'], continent='North America', city='New Jersey')]

print(regions[12])
# >>> RegionItem(id='ord', country='US', options=['ddos_protection'], continent='North America', city='Chicago')

# Of course you can use `for` to iterate all items.
# But be careful, it will cause a lot of requests if it's has a lot of data.
for region in regions:
    print(region)

# A smarter way to iterate is to determine the number of iterations you want.
smart_regions: VultrPagination[RegionItem] = v2.region.list(capacity=3)
for region in smart_regions:
    print(region)
# >>> RegionItem(id='ams', country='NL', options=['ddos_protection'], continent='Europe', city='Amsterdam')
# >>> RegionItem(id='atl', country='US', options=['ddos_protection'], continent='North America', city='Atlanta')
# >>> RegionItem(id='cdg', country='FR', options=['ddos_protection'], continent='Europe', city='Paris')

# At last, you can get all data just like calling attributes (better programming experience if you use IDE):
first_region: RegionItem = regions.first()
print(first_region.country, first_region.city)
# >>> NL Amsterdam
```

## CLI
PyVultr also provides a command line interface.  
It's a simple wrapper of the python library using [Fire](https://github.com/google/python-fire),  and it has a beautiful output by using [Pygments](https://github.com/pygments/pygments).  
It registered a command `pyvultr` in the system, so you can just type `pyvultr` to use it:
```shell
# please setup Your API Key first:
# you can generate your API Key from https://my.vultr.com/settings/#settingsapi
# export VULTR_API_KEY="..."

# show help by type `pyvultr`
$ pyvultr
```

`pyvultr` cli usage is very similar to the python library usage.
let's explain this with get account information api :

**In Python**:
```python
from pyvultr import VultrV2

# here we get api key from env `VULTR_API_KEY`
VultrV2().account.get()
>>> AccountInfo(name='test man', email='test@xxx.xxx', acls=['manage_users', 'subscriptions_view', 'subscriptions', 'billing', 'support', 'provisioning', 'dns', 'abuse', 'upgrade', 'firewall', 'alerts', 'objstore', 'loadbalancer', 'vke'], balance=11.2, pending_charges=3.4, last_payment_date='2019-07-16T05:19:50+00:00', last_payment_amount=-10)
```

**In CLI**:  
```shell
$ pyvultr account get
{
    "name": "test man",
    "email": "test@xxx.xxx",
    "acls": [
        "manage_users",
        "subscriptions_view",
        "subscriptions",
        "billing",
        "support",
        "provisioning",
        "dns",
        "abuse",
        "upgrade",
        "firewall",
        "alerts",
        "objstore",
        "loadbalancer",
        "vke"
    ],
    "balance": 11.2,
    "pending_charges": 3.4,
    "last_payment_date": "2019-07-16T05:19:50+00:00",
    "last_payment_amount": -10
}
```
Actually, we have a beautiful output:  

![CLI Example](./doc/cli_example.png)

### Testing
```Python
python -m pytest -v
```

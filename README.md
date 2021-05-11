# bmc_discovery_pgsq
Public endpoint for BMC Discovery (ADDM) Generic Search Query

# Prerequisites
* BMC Discovery user with REST API access

# config.json
```
{
    "api": {
        "version": "v1.1",
        "endpoint": "data/search",
        "token": "API_TOKEN"
    },
    "appliance": {
        "address": "127.0.0.1"
    },
    "flask": {
        "host": "0.0.0.0",
        "port": 8082
    }
}
```
where:
* `API_TOKEN` - BMC Discovery REST API token
* `appliance.address` - by default set to localhost but you can also change it to IP of your BMC Discovery appliance and build Dockerfile

# Installation on BMC Discovery appliance
```
if [[ $(id -u) -eq 1000 ]] ; then
  mkdir -p /usr/tideway/bin-custom/pgsq
  wget https://raw.githubusercontent.com/mjaromi/bmc_discovery_pgsq/master/app.py -O /usr/tideway/bin-custom/pgsq/app.py
  wget https://raw.githubusercontent.com/mjaromi/bmc_discovery_pgsq/master/config.json -O /usr/tideway/bin-custom/pgsq/config.json
  chmod +x /usr/tideway/bin-custom/pgsq/app.py
  mkdir -p /usr/tideway/bin-custom/pgsq/templates
  wget https://raw.githubusercontent.com/mjaromi/bmc_discovery_pgsq/master/templates/form.html -O /usr/tideway/bin-custom/pgsq/templates/form.html
else
  echo -e '\033[1;91mYou are not tideway user. Switch to tideway and try again.\033[0m'
fi

if [[ $(id -u) -eq 1000 ]] ; then
  mkdir -p /usr/tideway/bin-custom/modules/python
  cd /usr/tideway/bin-custom/modules/python
  wget -q https://files.pythonhosted.org/packages/4e/0b/cb02268c90e67545a0e3a37ea1ca3d45de3aca43ceb7dbf1712fb5127d5d/Flask-1.1.2.tar.gz
  wget -q https://files.pythonhosted.org/packages/4f/e7/65300e6b32e69768ded990494809106f87da1d436418d5f1367ed3966fd7/Jinja2-2.11.3.tar.gz
  wget -q https://files.pythonhosted.org/packages/b9/2e/64db92e53b86efccfaea71321f597fa2e1b2bd3853d8ce658568f7a13094/MarkupSafe-1.1.1.tar.gz
  wget -q https://files.pythonhosted.org/packages/10/27/a33329150147594eff0ea4c33c2036c0eadd933141055be0ff911f7f8d04/Werkzeug-1.0.1.tar.gz
  wget -q https://files.pythonhosted.org/packages/68/1a/f27de07a8a304ad5fa817bbe383d1238ac4396da447fa11ed937039fa04b/itsdangerous-1.1.0.tar.gz
  wget -q https://files.pythonhosted.org/packages/27/6f/be940c8b1f1d69daceeb0032fee6c34d7bd70e3e649ccac0951500b4720e/click-7.1.2.tar.gz
  wget -q https://files.pythonhosted.org/packages/6b/47/c14abc08432ab22dc18b9892252efaf005ab44066de871e72a38d6af464b/requests-2.25.1.tar.gz
  wget -q https://files.pythonhosted.org/packages/cb/cf/871177f1fc795c6c10787bc0e1f27bb6cf7b81dbde399fd35860472cecbc/urllib3-1.26.4.tar.gz
  wget -q https://files.pythonhosted.org/packages/ee/2d/9cdc2b527e127b4c9db64b86647d567985940ac3698eeabc7ffaccb4ea61/chardet-4.0.0.tar.gz
  wget -q https://files.pythonhosted.org/packages/06/a9/cd1fd8ee13f73a4d4f491ee219deeeae20afefa914dfb4c130cfc9dc397a/certifi-2020.12.5.tar.gz
  wget -q https://files.pythonhosted.org/packages/9f/24/1444ee2c9aee531783c031072a273182109c6800320868ab87675d147a05/idna-3.1.tar.gz
  ls -1 *.tar.gz | xargs -I{} tar -xf {}
  find *.tar.gz -type f -delete
else
  echo -e '\033[1;91mYou are not tideway user. Switch to tideway and try again.\033[0m'
fi

if [[ $(id -u) -eq 0 ]] ; then
  FILE_IPTABLES=/etc/sysconfig/iptables
  LINE=$(cat -n ${FILE_IPTABLES} | grep '\-A INPUT -i lo -j ACCEPT' | head -1 | awk '{print $1}')
  cp -avr ${FILE_IPTABLES} /etc/sysconfig/iptables.backup_$(date +'%d_%m_%Y_%H_%M_%S')
  sed -i "${LINE}i\# Public Generic Search Query, port 8082\n-A INPUT -p tcp -m tcp --dport 8082 -j ACCEPT\n" ${FILE_IPTABLES}
  systemctl restart iptables
else
  echo -e '\033[1;91mYou are not root user. Switch to root and try again.\033[0m'
fi
```

# Docker
### pwsh
``` powershell
git clone https://github.com/mjaromi/bmc_discovery_pgsq.git
cd bmc_discovery_pgsq
docker build . ; docker run -dit -p8082:8082 $(docker images -q | select -f 1) ; docker exec -it $(docker ps -aq | select -f 1) sh
```

### shell
``` bash
git clone https://github.com/mjaromi/bmc_discovery_pgsq.git
cd bmc_discovery_pgsq
docker build . ; docker run -dit -p8082:8082 $(docker images -q | head -1) ; docker exec -it $(docker ps -aq | head -1) sh
```

# Usage
Go to the `<IP_ADDRESS>:8082`, type query and click `Run Query`. Results will be fetched from BMC Discovery appliance through REST API (pagination is supported).

If query will be invalid you will get following results:

`{"code": 400, "message": "Invalid search query", "transient": false}`

If there will be no results then you will get empty list as a results: `[]`

Otherwise you will see correct results.

# UI
![](pgsq.png)

# License
MIT

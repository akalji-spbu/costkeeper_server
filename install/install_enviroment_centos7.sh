rpm -Uvh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
yum clean all
yum -y update
yum -y upgrade
yum install -y nano mc make gcc nginx openssl-devel MariaDB-server MariaDB-client

cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.back
cp /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.back

systemctl enable mariadb.service
systemctl start mariadb.service
systemctl enable nginx.service
systemctl start nginx.service
mysql_secure_installation




cd /tmp
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
tar xzf Python-3.5.2.tgz
cd Python-3.5.2
./configure --prefix=/usr/local
make altinstall

pip3.5 install --upgrade pip
pip3.5 install sqlalchemy
pip3.5 install pymysql
pip3.5 install tornado

adduser costkeeper

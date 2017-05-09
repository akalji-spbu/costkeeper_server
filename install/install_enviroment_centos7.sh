rpm -Uvh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
touch /etc/yum.repos.d/MariaDB10.repo
echo "# MariaDB 10.1 CentOS repository list - created 2016-01-18 09:58 UTC" >> /etc/yum.repos.d/MariaDB10.repo
echo "# http://mariadb.org/mariadb/repositories/" >> /etc/yum.repos.d/MariaDB10.repo
echo "[mariadb]" >> /etc/yum.repos.d/MariaDB10.repo
echo "name = MariaDB" >> /etc/yum.repos.d/MariaDB10.repo
echo "baseurl = http://yum.mariadb.org/10.1/centos7-amd64" >> /etc/yum.repos.d/MariaDB10.repo
echo "gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB" >> /etc/yum.repos.d/MariaDB10.repo
echo "gpgcheck=1" >> /etc/yum.repos.d/MariaDB10.repo


yum clean all
yum -y update
yum -y upgrade
yum install -y epel-release
yum install -y nano mc make gcc nginx openssl-devel  supervisor wget
yum install -y MariaDB-client MariaDB-server 

cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.back
cp /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.back

systemctl enable mariadb.service
systemctl start mariadb.service
systemctl enable nginx.service
systemctl start nginx.service
systemctl enable supervisord.service
systemctl start supervisord.service
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

#!/bin/bash

PPA_REPOSITORIES=(
    'ppa:jon-severinsson/ffmpeg'
    'ppa:george-edison55/cmake-3.x'
)

PKG_DEPENDENCIES=(
    'python-setuptools'
    'python-dev'
    'build-essential'
    'git'
    'g++'
    'gfortran'
    'libopenblas-dev'
    'liblapack-dev'
    'debconf-utils'
    'redis-server'
    'mysql-server'
    'libmysqlclient-dev'
    'mc'
    'cmake'
    'unzip'
    'pkg-config'
    'checkinstall'
    'yasm'
    'python-numpy'
    'python-opencv'
    'libopencv-dev'
    'libavcodec-dev'
    'libavformat-dev'
    'libswscale-dev'
    'libjpeg-dev'
    'libpng-dev'
    'libtiff5-dev'
    'libjasper-dev'
    'libgtk2.0-dev'
    'libdc1394-22-dev'
    'libtbb2'
    'libtbb-dev'
    'libqt4-dev'
    'libxine2-dev'
    'libgstreamer0.10-dev'
    'libgstreamer-plugins-base0.10-dev'
    'libv4l-dev'
    'libfaac-dev'
    'libmp3lame-dev'
    'libtheora-dev'
    'libvorbis-dev'
    'v4l-utils'
    'x264'
)

# Enable multiverse.
sed -i "/^# deb.*multiverse/ s/^# //" /etc/apt/sources.list

if test ! $(which add-apt-repository)
    then
    apt-get install -y software-properties-common python-software-properties
fi

# Add apt repositories
for repo in "${PPA_REPOSITORIES[@]}"
do
    add-apt-repository -y $repo
done

apt-get update

export DEBIAN_FRONTEND="noninteractive"

apt-get install -y ${PKG_DEPENDENCIES[@]}

# Fix for matplotlib bug #3029.
# See: https://github.com/matplotlib/matplotlib/issues/3029
if [ ! -f "/usr/include/freetype2/ft2build.h" ]; then
    ln -s /usr/include/freetype2/ft2build.h /usr/include/
fi

echo 'Installing freetype additional packages.'
apt-get install -y freetypy*

# Create a temporary 2Gb swap file so that we don't exaust the virtual
# machines's memory when compiling scipy.
if [ ! -f "/tmp/tmp_swap" ]; then
    dd if=/dev/zero of=/tmp/tmp_swap bs=1024 count=2097152
    mkswap /tmp/tmp_swap
    swapon /tmp/tmp_swap
fi

# Install OpenCV
pushd /tmp
    wget http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.11/opencv-2.4.11.zip
    unzip opencv-2.4.11.zip
    cd opencv-2.4.11
    mkdir build
    cd build
    cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_TBB=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D WITH_V4L=ON -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON -D WITH_QT=ON -D WITH_OPENGL=ON ..
    make -j 4
    sudo make install
    sudo sh -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/opencv.conf'
    sudo ldconfig
popd

cp /vagrant/ssh_config /etc/ssh
cp /vagrant/id_rsa.bitbucket ~/.ssh
chmod 600 /etc/ssh/ssh_config
chmod 600 ~/.ssh/id_rsa.bitbucket


BIOMIO_BASE=/home/vagrant/biomio

if [ ! -d "${BIOMIO_BASE}" ]; then
	echo "Clonning BIOMIO repo..."
    ssh-keyscan -H bitbucket.org >> ~/.ssh/known_hosts
	git clone git@bitbucket.org:biomio/prototype-protocol.git ${BIOMIO_BASE} && cd ${BIOMIO_BASE} && git checkout development
fi

chown vagrant:vagrant ${BIOMIO_BASE} -R

# Enable Redis event notifications
echo "Enabling Redis event notifications"
sed -i 's/notify-keyspace-events ""/notify-keyspace-events KEA/' /etc/redis/redis.conf
service redis-server restart

# Install required python packages.
easy_install pip
pip install -r ${BIOMIO_BASE}/requirements.txt
pip install supervisor supervisor_twiddler

echo "Installing supervisor"
cp /vagrant/supervisord.conf /etc && cp /vagrant/supervisord /etc/init.d/ && chmod +x /etc/init.d/supervisord
update-rc.d supervisord defaults
service supervisord start

DB="biomio_db"
DB_USER="biomio_gate"
DB_USER_PWD="gate"

echo "Creating database and user"
mysql -e "CREATE USER '$DB_USER'@'localhost' IDENTIFIED BY '$DB_USER_PWD';\
	CREATE DATABASE $DB;\
	GRANT ALL PRIVILEGES  ON $DB.* TO '$DB_USER'@'localhost' WITH GRANT OPTION;"
echo "Loading schema for '$DB'"
mysql $DB < /vagrant/schema.sql

# Change binding address for MySQL
sed -i -r 's/bind-address\t\t= 127.0.0.1/bind-address\t\t= 0.0.0.0/' /etc/mysql/my.cnf

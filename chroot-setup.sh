#!/bin/sh -x
if id | grep -qv uid=0; then
    echo "Must run setup as root"
    exit 1
fi

create_socket_dir() {
    local dirname="$1"
    local ownergroup="$2"
    local perms="$3"

    mkdir -p $dirname
    chown $ownergroup $dirname
    chmod $perms $dirname
}

rm -rf /jail
mkdir -p /jail
mkdir -p /jail/app
cp -p index.html /jail/app

cp zook.conf /jail/app
./chroot-copy.sh zookld /jail/app
./chroot-copy.sh zookd /jail/app
./chroot-copy.sh zookfs /jail/app

#./chroot-copy.sh /bin/bash /jail

./chroot-copy.sh /usr/bin/env /jail
./chroot-copy.sh /usr/bin/python /jail

# to bring in the crypto libraries
./chroot-copy.sh /usr/bin/openssl /jail

mkdir -p /jail/usr/lib /jail/usr/lib/i386-linux-gnu /jail/lib /jail/lib/i386-linux-gnu
cp -r /usr/lib/python2.7 /jail/usr/lib
cp /usr/lib/i386-linux-gnu/libsqlite3.so.0 /jail/usr/lib/i386-linux-gnu
cp /lib/i386-linux-gnu/libnss_dns.so.2 /jail/lib/i386-linux-gnu
cp /lib/i386-linux-gnu/libresolv.so.2 /jail/lib/i386-linux-gnu
cp -r /lib/resolvconf /jail/lib

mkdir -p /jail/usr/local/lib
cp -r /usr/local/lib/python2.7 /jail/usr/local/lib

mkdir -p /jail/etc
cp /etc/localtime /jail/etc/
cp /etc/timezone /jail/etc/
cp /etc/resolv.conf /jail/etc/

mkdir -p /jail/usr/share/zoneinfo
cp -r /usr/share/zoneinfo/America /jail/usr/share/zoneinfo/

create_socket_dir /jail/app/echosvc 61010:61010 755
create_socket_dir /jail/app/authsvc 61014:61014 775
create_socket_dir /jail/app/banksvc 61015:61015 775
create_socket_dir /jail/app/profilesvc 61016:61016 775

mkdir -p /jail/tmp
chmod a+rwxt /jail/tmp

mkdir -p /jail/dev
mknod /jail/dev/urandom c 1 9

cp -r AutoPS /jail/
cp -r zoobar /jail/app/
rm -rf /jail/app/zoobar/db

python /jail/app/zoobar/zoodb.py init-person
python /jail/app/zoobar/zoodb.py init-transfer
python /jail/app/zoobar/zoodb.py init-cred
python /jail/app/zoobar/zoodb.py init-bank


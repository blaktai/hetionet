redisurl="http://download.redis.io/redis-stable.tar.gz"
curl -s -o redis-stable.tar.gz $redisurl
sudo su root
mkdir -p /usr/local/lib/
chmod a+w /usr/local/lib/
tar -C /usr/local/lib/ -xzf redis-stable.tar.gz
rm redis-stable.tar.gz
cd /usr/local/lib/redis-stable/
make && make install
sudo su root
mkdir -p /etc/redis/
touch /etc/redis/6379.conf
redis-server
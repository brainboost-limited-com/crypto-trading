
Dont use conda is useless and is buggy, just pplain source code python install



# Install everything as  root and execute everything as root as the server has no
# external exposure and with normal user errors will come up and takes more time


# Remove the python that comes by default in your ubuntu installation

apt-get remove python 
apt-get purge python 

# Install ubuntu dev essential packages to build python from C code


sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev




# Check if python command still exists

pyth[tab]

# Download python 3.9.5 from source

cd ~/Downloads/

wget https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz

# Decompress


tar xzvf Python-3.9.5.tgz

# Compile python 3.9.5 source code

cd Python-3.9.5
./configure --with-system-ffi 
make
sudo checkinstall
make install

# Python compiled installed /usr/local/bin/python3.9 , then create symlink so python points to python 3.9 

ln -s /usr/local/bin/python3.9 /usr/bin/python
ln -s /usr/local/bin/pip3.9 /usr/local/bin/pip
root@goldenthinker-trading-1:~/crypto_trading# python --version
Python 3.9.5

# You can try to execute the python and go installing packages as soon as the code crashes 
# or you can try the com_goldenthinker_trade_install/requirements.txt file as followd and see if it works

pip install -r com_goldenthinker_trade_install/requirements.txt



# Else try as follows


#Do not use pip package from pip repository use the latest github else you get the binance.helpers error

pip install git+https://github.com/sammchardy/python-binance.git

#If the previous returns error do the following


# make sure setuptools is properly installed , better do as follows just in case

python -m pip uninstall setuptools
python -m pip install setuptools

If error 

xcrun codesign --sign - "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/regex/_regex.cpython-39-darwin.so"




# Ignore the further errors if problem installing and execute testing

python gt_monitor_all_symbols.py 


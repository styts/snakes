name=snakes

cp -a ~/dvizshok .
cd ~/ps4a
./android.py build ../$name release install
cd ~/$name
rm -rf dvizshok
rm -rf *.pyo

# Preparing repository
1. Run `git submodule update --init --recursive`
2. Install yakut, nunavut `pip install -U yakut nunavut`
3. Install unzip `sudo pacman -S unzip` or `sudo apt install unzip`
4. Change directory to firmware `cd firmware`
5. Run `make dsdl`
7. Run `make -j<amount of cores or threads you have>`
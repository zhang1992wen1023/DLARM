wget https://github.com/apache/incubator-mxnet/releases/download/1.5.0/apache-mxnet-src-1.5.0-incubating.tar.gz
tar -xzvf apache-mxnet-src-1.5.0-incubating.tar.gz

sudo apt install -y liblapack3 libopenblas-base libopenblas-dev
sudo apt-get install -y git build-essential libatlas-base-dev libopencv-dev graphviz python-pip
sudo apt install libopenblas-dev libatlas-dev liblapack-dev
sudo apt install liblapacke-dev checkinstall # For OpenCV
sudo pip install --upgrade pip==9.0.1
sudo pip install numpy==1.16.4
sudo apt-get install gfortran
sudo pip install scipy # ~20-30 min on HDD
sudo apt-get install python-matplotlib
sudo apt-get install libcanberra-gtk-module
apt-get install libfreetype6-dev pkg-config libpng-dev

sudo pip install matplotlib==2.2.3
sudo pip install pyyaml
sudo pip install scikit-build
sudo apt-get -y install cmake
sudo apt install libffi-dev
sudo pip install cffi
sudo pip install pandas # ~20-30 min on HDD
sudo pip install Cython
sudo pip install scikit-image
sudo apt install python-sklearn 

sudo pip install protobuf
sudo apt-get install libboost-dev libboost-all-dev
sudo pip install graphviz jupyter
#git clone https://github.com/apache/incubator-mxnet.git --branch v1.4.x --recursive
cd incubator-mxnet/

sudo gedit 3rdparty/mshadow/make/mshadow.mk
sed -i 's/MSHADOW_LDFLAGS += -lblas/MSHADOW_LDFLAGS += -lblas \n        MSHADOW_CFLAGS += -DMSHADOW_USE_PASCAL=1/' /home/dlarm2/apache-mxnet-src-1.2.1-incubating/3rdparty/mshadow/make/mshadow.mk
#change last line to USE_PASCAL=1

cp make/config.mk .
sed -i 's/USE_CUDA = 0/USE_CUDA = 1/' config.mk
sed -i 's/USE_CUDA_PATH = NONE/USE_CUDA_PATH = \/usr\/local\/cuda/' config.mk
sed -i 's/USE_CUDNN = 0/USE_CUDNN = 1/' config.mk
sed -i '/USE_CUDNN/a CUDA_ARCH := -gencode arch=compute_53,code=sm_53 -gencode arch=compute_62,code=sm_62' config.mk

sudo apt-get install gcc-6 g++-6
sed -i 's/export CC = gcc/export CC = gcc-6/' config.mk
sed -i 's/export CXX = g++/export CXX = g++-6/' config.mk

sudo make -j 4

sudo pip install gluoncv

wget https://github.com/librosa/librosa/archive/0.6.3.tar.gz
tar -xzvf 0.6.3.tar.gz

wget http://releases.llvm.org/6.0.1/llvm-6.0.1.src.tar.xz
tar -xvf llvm-6.0.1.src.tar.xz

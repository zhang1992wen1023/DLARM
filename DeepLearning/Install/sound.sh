sudo apt-get install -y libsdl2-2.0-0 ffmpeg-doc ffmpeg libavdevice57 libsndfile1 libedit-dev
sudo apt-get install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
sudo pip install Cython cffi PySoundFile
wget https://github.com/llvm/llvm-project/releases/download/llvmorg-7.1.0/llvm-7.1.0.src.tar.xz
tar -xf llvm-7.1.0.src.tar.xz
cd llvm-7.1.0.src/
mkdir build
cd build/
cmake $LLVM_SRC_DIR -DCMAKE_BUILD_TYPE=Release \
                    -DLLVM_TARGETS_TO_BUILD="ARM;X86;AArch64"
sudo make -j 4
cd
cd Downloads
git clone https://github.com/numba/llvmlite.git
sudo LLVM_CONFIG=/home/dlarm/Downloads/llvm-7.1.0.src/build/bin/llvm-config python setup.py develop
sudo LLVM_CONFIG=/home/dlarm/Downloads/llvm-7.1.0.src/build/bin/llvm-config python setup.py install
sudo pip install numba
git clone git://github.com/numba/numba.git
cd numba/
python setup.py build_ext --inplace
pip install librosa==0.6.3
sudo apt-get remove python-joblib
pip install librosa==0.6.3

sudo apt-get install sox libsox-dev libsox-fmt-all
sudo pip install kaldi_io
git clone https://github.com/google/protobuf.git protobuf
cd protobuf/
./autogen.sh
#https://criu.org/Build_protobuf#Cross-compile_for_ARM
./configure --host=aarch64-linux-gnu --prefix=`pwd`/../`uname -m`-linux-gnu --disable-protoc PATH=`pwd`/../`uname -m`-linux-gnu/bin:$PATH
make
make install
sudo pip install flake8
git clone https://github.com/pytorch/audio.git
cd audio/
sudo python setup.py install
sudo pip install scikit-image pandas python_speech_features tensorboardX
#https://pytorch.org/audio/

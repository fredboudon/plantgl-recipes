export CXXFLAGS="-stdlib=libc++ -std=c++14"
export LINKFLAGS="-stdlib=libc++ -std=c++14 -L${LIBRARY_PATH}"

if [ "$(uname)" == "Darwin" ];
then
    export CC=clang
    export CXX=clang++

    export MACOSX_VERSION_MIN=10.11
    
    CXXFLAGS="${CXXFLAGS} -mmacosx-version-min=${MACOSX_VERSION_MIN}"
    LINKFLAGS="${LINKFLAGS} -mmacosx-version-min=${MACOSX_VERSION_MIN}"
fi

cmake -DCMAKE_OSX_DEPLOYMENT_TARGET=10.11 \
    -DCMAKE_INSTALL_PREFIX=${PREFIX}\
    -DCMAKE_PREFIX_PATH=${PREFIX}\
    -DBUILD_SHARED_LIBS=ON .

make -j${CPU_COUNT}
make install
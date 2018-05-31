# HIAFuzz
Hybrid Interface Aware Fuzz for Android Kernel Drivers
===================
This tool is for recovering ioctl interfaces in kernel drivers, which is used in kernel fuzzing.
### Tested on
Ubuntu 16.04 LTS
There are two main components of `HIAFuzz`: **Interface Recovery** and **Fuzzing Engine**

## 1. Interface Recovery
The interface recovery mechanism is based on gdb analysis on kernel image vmlinux.

### 1.1 Setup
This tool depends on pygdbmi, which is used for parsing gdb machine interface output with Python.
```
pip3 install pygdbmi
```

### 1.2 Build the Kernel

To run the Interface Recovery components on kernel drivers, we need to first compile the kernel with -g3 option.
The following command can be used to replace all -g option to -g3.
```
    for f in `find . -name Makefile`; do sed -i "s/-g /-g3 /g" $f;done
    for f in `find . -name Makefile`; do sed -i "s/-g$/-g3/g" $f; done
```
Then normal steps are taken to build the kernel. Ex:
```
make defconfig
make -j8 O=out ARCH=arm64
```
After vmlinux builded, the debug information is in the .debug section. The option -j8 makes 8 threads working in parallel, and in few minutes the kernel will be build.

### 1.3 Running
Use the following command to run this tool.
```
python3 gdbioctl.py -h
usage: gdbioctl.py [-h] [-v VMLINUX] [-f DEVICE_IOCTL_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -v VMLINUX            Path of the vmlinux image. The recovered ioctls are
                        stored in this folder.
  -f DEVICE_IOCTL_FILE  The file that conations ioctl and corresponding device
                        file names, like /dev/alarm alarm_ioctl.
```
For example, to analyze the vmlinux of kindle HDX 3rd, we need kindle7_device_ioctl.txt. Use the command
```
python3 gdbioctl.py -v /path/to/kindle/vmlinux -f /path/to/kindle7_device_ioctl.txt
```
After a few minutes the recovered interface are in the folder that -v option set.

## 2. Fuzzing
The fuzzing tool is Mango Fuzz from [difuze](https://github.com/ucsb-seclab/difuze).

## 3. Example

Now, we will show an example from the point where you have kernel sources to the point of getting Interface Recovery results.
Download and extract the kernel source of Huawei Mate 9 kernel from [MHA-NG_EMUI5.0_opensource.tar.gz](http://download-c1.huawei.com/download/downloadCenter?downloadId=95352&version=391424&siteCode=worldwide) from [Huawei Open Source Release Center](https://consumer.huawei.com/en/opensource/).
Lets say you extracted the above file in a folder called: ~/Code_Opensource
### 3.1 Build the kernel
Use the command to replace -g to -g3.

```
cd ~/Code_Opensource/kernel
for f in `find . -name Makefile`; do sed -i "s/-g /-g3 /g" $f; done
for f in `find . -name Makefile`; do sed -i "s/-g$/-g3/g" $f; done
#export PATH=$PATH:$(android platform directory you download)/prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin
export PATH=$PATH:/workspace/aosp/prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin/aarch64-linux-android-gcc
export CROSS_COMPILE=aarch64-linux-android-
mkdir ../out
make ARCH=arm64 O=../out merge_hi3660_defconfig
make ARCH=arm64 O=../out -j8
```
After a few minutes, the vmlinux of Mate 9 is generated in ../out/.

### 3.2 Running
Use mate9_device_ioctl.txt provided by this project as input.
```
python3 gdbioctl.py -v ~/Code_Opensource/out/vmlinux -f /path/to/mate9_device_ioctl.txt
```
Tow folders are created in ~/Code_Opensource/out/ called ioctl_finder_out and ioctl_preprocessed_out. All interface recovered are located in ioctl_finder_out and related struct, union, type def and etc. are in ioctl_preprocessed_out.







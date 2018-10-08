These page show the practical CVEs that Found.
# CVE-2018-11023, CVE-2018-11024
I reported these bugs to Security@amazon.com on On 5/11/2018 and now I have been told they have repaired the bugs and the details can be published. However,  Amazon does not have an advisory page at the moment. I think it is a must to list the detailed infomation here.
## Time Line
 * 5/11/2018 Bugs were reported to Security@amazon.com.
 * 06/27/2018 Amazon got confirmation that two of them allow local elevation of privilege from a regular user to root (CVE-2018-11023 and CVE-2018-11024 on /dev/gcioctl). 
 * 09/18/2018 Amazon had started updating our FireOS 4 devices with the security patches addressing the two critical issues (i.e. CVE-2018-11023 and CVE-2018-11024 on /dev/gcioctl).
 
 Details of all emails are listed here.
 


Re: Bug Report for Kindle Fire HD 3rd

"Dalci, Eric" <edalci@amazon.com>
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
To: "Dalci, Eric" <edalci@amazon.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric,
Please include my name and my department information.  Thanks a lot.
Lu Shuaibing, a security researcher from National Key Laboratory of Science and Technology on Information System Security in Beijing, China.

 

 

Image removed by sender.
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 09/18/2018 06:54, Dalci, Eric wrote:

Hi Lu,

Sorry about the delay.

Thanks again for your patience, and for working with us on this. We have started updating our FireOS 4 devices with the security patches addressing the two critical issues (i.e. CVE-2018-11023 and CVE-2018-11024 on /dev/gcioctl) that you have reported to us. It is ok now to publish the CVE details. Are you planning in publishing anything else about the vulnerabilities that you reported to us?

Thank you

-Eric

 

From: lsb <datadancer@163.com>
Date: Sunday, September 9, 2018 at 8:27 PM
To: "Dalci, Eric" <edalci@amazon.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric,
Thanks for your responsibility. What's going on now? Can the CVE be published? Thanks a lot!

 

 

Image removed by sender.
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 08/29/2018 05:41, Dalci, Eric wrote:

Hi Lu,

 

Thanks again for your patience, and for working with us on this. We were able to resolve the regression and our release testing has resumed last week. I will update you in two weeks about the status.

 

Thanks

-Eric

 

From: lsb <datadancer@163.com>
Date: Saturday, August 11, 2018 at 5:33 PM
To: "Dalci, Eric" <edalci@amazon.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric,





Thanks for your kindness. I don't go to Las Vegas this year. Have a nice weekend.





Yours,

Lu

 

Image removed by sender.
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 08/09/2018 02:24, Dalci, Eric wrote:

Hi Lu,

Thanks again for your patience, and for working with us on this.

 

We ran into a regression during testing. I will update you in two weeks about the progress. If you are going to BlackHat or Defcon conferences in Las Vegas, let me know so someone from my team can meet you there.

 

Thanks

-Eric

 

 

From: "Dalci, Eric" <edalci@amazon.com>
Date: Monday, July 23, 2018 at 6:28 PM
To: lsb <datadancer@163.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Lu,

Thanks again for your patience, and for working with us on this.

 

We will be testing the new release that will carry the patches for the two critical issues (i.e. CVE-2018-11023 and CVE-2018-11024 on /dev/gcioctl) over the next several weeks. I will update you in two weeks about the status.

 

Thanks

-Eric

 

 

From: "Dalci, Eric" <edalci@amazon.com>
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
To: "Dalci, Eric" <edalci@amazon.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric, 

Thanks for your work. The investigation is corresponding to my analysis. When can we release the CVEs? I think it's responsible for customers.

Thanks a lot 

Lu

 

Image removed by sender.
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 06/27/2018 00:07, Dalci, Eric wrote:

Hi Lu,

 

Thanks for continuing working with us. We have reviewed the issues and I would like to get confirmation that two of them allow local elevation of privilege from a regular user to root (CVE-2018-11023 and CVE-2018-11024 on /dev/gcioctl). The remaining reported crashes would need to have system access level before possible escalation to kernel (for CVE-2018-11019 and CVE-2018-11022) or require root level before possible escalation to kernel (for CVE-2018-11020, CVE-2018-11021, CVE-2018-11025 and CVE-2018-11026). Hence, we consider that those last six issues do not pose immediate risk to our customers since triggering requires system or root already.

Can you confirm that these matches your investigation? I will keep you posted on our progress of the investigation in two weeks.

 

Thanks!

-Eric

 

 

 

From: lsb <datadancer@163.com>
Date: Monday, June 25, 2018 at 2:16 AM
To: "Dalci, Eric" <edalci@amazon.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric, 

Thanks for your work! By the way, When will the update and the CVE be public? 

 

Yours 

Lu

 

Image removed by sender.
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 06/12/2018 06:27, Dalci, Eric wrote:

Hi Lu,

 

Thanks for working with us. We have been able to reproduce some of the issues and are investigating the remaining ones. I will provide an update in two weeks.

 

Thank you

-Eric

 

 

From: <detected-as-spam@amazon.com> on behalf of lsb <datadancer@163.com>
Date: Thursday, June 7, 2018 at 5:02 AM
To: "Dalci, Eric" <edalci@amazon.com>
Subject: [SPAM][100%] Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric, 

It's OK. If you have any questions about the issues, please inform me. Thanks a lot.

Best regards,

Lu Shuaibing 

Image removed by sender.
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 06/05/2018 01:42, Dalci, Eric wrote:

Hi Lu,

 

Sorry about the delay, we are actually not completely done investigating the reported issues, I will provide an update by June 11th. Thanks for understanding.

 

Regards

-Eric

 

 

From: lsb <datadancer@163.com>
Date: Tuesday, May 29, 2018 at 9:57 AM
To: "Dalci, Eric" <edalci@amazon.com>
Subject: Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric,

I am very pleased to know that you have conformed my input. Thanks for being responsible. Have a nice holiday!

 

Lu

 

Image removed by sender. http://mail-online.nosdn.127.net/d5b4db997f83b9ee12c5ae026c9bb3a0.jpg
	

lsb

邮箱：datadancer@163.com

签名由 网易邮箱大师 定制

On 05/29/2018 22:42, Dalci, Eric wrote:

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

On 05/25/2018 08:25, Dalci, Eric wrote:

Thanks Lu for sharing those CVE IDs.

I will get back to you by Monday. We finished the assessment.

 

-Eric

 

 

From: lsb <datadancer@163.com>
Date: Thursday, May 24, 2018 at 2:57 AM
To: "Dalci, Eric" <edalci@amazon.com>
Subject: Re:Re: Bug Report for Kindle Fire HD 3rd

 

Hi Eric,

Have you figure out the bugs, I have received CVE IDs from http://cve.mitre.org/.

Can you repair and publish these bugs with these CVE IDs.

Descriptions and CVE IDs are in the attachment.

 

 














At 2018-05-16 07:11:00, "Dalci, Eric" <edalci@amazon.com> wrote:










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
Shuaibing Lu

 


At 2018-05-12 01:42:31, "Dalci, Eric" <edalci@amazon.com> wrote:

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

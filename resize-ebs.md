# resize
```sh
(venv) ubuntu@ip-172-31-13-161:~/google_trends_scraper/scraper$ lsblk
NAME         MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
loop0          7:0    0 504.2M  1 loop /snap/gnome-42-2204/172
loop1          7:1    0  24.9M  1 loop /snap/amazon-ssm-agent/7628
loop2          7:2    0     4K  1 loop /snap/bare/5
loop3          7:3    0  55.7M  1 loop /snap/core18/2796
loop4          7:4    0  55.7M  1 loop /snap/core18/2812
loop5          7:5    0  63.9M  1 loop /snap/core20/2105
loop6          7:6    0  63.9M  1 loop /snap/core20/2182
loop7          7:7    0  74.1M  1 loop /snap/core22/1033
loop8          7:8    0  74.2M  1 loop /snap/core22/1122
loop9          7:9    0 266.6M  1 loop /snap/firefox/3836
loop10         7:10   0 267.5M  1 loop /snap/firefox/3941
loop11         7:11   0   497M  1 loop /snap/gnome-42-2204/141
loop12         7:12   0  91.7M  1 loop /snap/gtk-common-themes/1535
loop14         7:14   0    87M  1 loop /snap/lxd/27428
loop15         7:15   0  40.4M  1 loop /snap/snapd/20671
loop16         7:16   0  39.1M  1 loop /snap/snapd/21184
loop17         7:17   0  25.2M  1 loop /snap/amazon-ssm-agent/7983
loop18         7:18   0    87M  1 loop /snap/lxd/27948
nvme0n1      259:0    0   256G  0 disk
├─nvme0n1p1  259:1    0 127.9G  0 part /var/snap/firefox/common/host-hunspell
│                                      /
├─nvme0n1p14 259:2    0     4M  0 part
└─nvme0n1p15 259:3    0   106M  0 part /boot/efi
(venv) ubuntu@ip-172-31-13-161:~/google_trends_scraper/scraper$ sudo growpart /dev/nvme0n1 1
CHANGED: partition=1 start=227328 old: size=268208095 end=268435423 new: size=536643551 end=536870879
(venv) ubuntu@ip-172-31-13-161:~/google_trends_scraper/scraper$ sudo resize2fs /dev/nvme0n1p1
resize2fs 1.46.5 (30-Dec-2021)
Filesystem at /dev/nvme0n1p1 is mounted on /; on-line resizing required
old_desc_blocks = 16, new_desc_blocks = 32
The filesystem on /dev/nvme0n1p1 is now 67080443 (4k) blocks long.

(venv) ubuntu@ip-172-31-13-161:~/google_trends_scraper/scraper$ df -h
Filesystem       Size  Used Avail Use% Mounted on
/dev/root        248G  116G  133G  47% /
tmpfs            7.7G   48K  7.7G   1% /dev/shm
tmpfs            3.1G  332M  2.8G  11% /run
tmpfs            5.0M     0  5.0M   0% /run/lock
/dev/nvme0n1p15  105M  6.1M   99M   6% /boot/efi
tmpfs            1.6G  4.0K  1.6G   1% /run/user/1000
(venv) ubuntu@ip-172-31-13-161:~/google_trends_scraper/scraper$
```

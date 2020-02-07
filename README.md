# rossuse
Generate rpm spec files for Opensuse/SLES

This is a first attempt at integrating ROS building/packaging with the Open Build Service.

The script is messy but it works. It relies on some custom modifications to rosdistro which I am
currently maintaining in 

https://github.com/neotinker/rosdistro

I will eventual try and get these changes merged into the standard ROS rosdistro repo

https://github.com/ros/rosdistro

Use it at your own risk :)

EX)

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.1 --pkg_name ros_comm```


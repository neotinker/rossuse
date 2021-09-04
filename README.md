# rossuse
Generate service and rpm spec files for Opensuse/SLES

This is a first attempt at integrating ROS building/packaging with the Open Build Service.

The script is messy but it works. It relies on some custom modifications to rosdistro which I am
currently maintaining in 

https://github.com/neotinker/rosdistro

I will eventual try and get these changes merged into the standard ROS rosdistro repo

https://github.com/ros/rosdistro

Use it at your own risk :)

EX)

ADD A SINGLE PACKAGE TO OBS

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.1 --pkg_name ros_comm```

ADD A PACKAGE AND ALL ITS DEPENDENCIES

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.1 --gen_deps --pkg_name ros_comm```

REGENERATE SPEC AND SERVICE FILES FOR A PACKAGE

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.1 --update_existing --pkg_name ros_comm```

REGENERATE SPEC AND SERVICE FILES FOR A PACKAGE AND ALL ITS DEPENDENCIES

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.1 --gen_deps --update_existing --pkg_name ros_comm```


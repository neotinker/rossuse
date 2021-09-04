# rossuse
Generate service and rpm spec files for Opensuse/SLES

This is a first attempt at integrating ROS building/packaging with the Open Build Service.

The script is messy but it works. It relies on some custom modifications to rosdistro which I am
currently maintaining in 

https://github.com/neotinker/rosdistro

ROS developers have told me that I should not be modifying the distribution.yaml file to add OS support. They said I should look at bloom to see how it handles building for other OSs without modifying distribution.yaml. Once I have worked that out, rossuse.py should be able to use the proper ROS rosdistro github.

https://github.com/ros/rosdistro

I make no guarantees about rossuse.py. Use it at your own risk :)

NOTES

- The OBS Project that you are using must exist. rossuse.py wont create it for you.
- rossuse.py looks for its templates in the current working directory.

EX)

ADD A SINGLE PACKAGE TO OBS

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.1 --pkg_name ros_comm```

ADD A PACKAGE AND ALL ITS DEPENDENCIES

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.1 --gen_deps --pkg_name ros_comm```

REGENERATE SPEC AND SERVICE FILES FOR A PACKAGE

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.1 --update_existing --pkg_name ros_comm```

REGENERATE SPEC AND SERVICE FILES FOR A PACKAGE AND ALL ITS DEPENDENCIES

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.1 --gen_deps --update_existing --pkg_name ros_comm```


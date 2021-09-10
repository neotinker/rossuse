# rossuse
Generate service and rpm spec files for Opensuse/SLES

This is a first attempt at integrating ROS building/packaging with the Open Build Service.

The script is messy but it works.

By default, it will pull the index-v4.yaml file from https://github.com/ros/rosdistro but you can override the default to point to your own fork of rosdistro using the ROSDISTRO_INDEX_URL environment variable. I maintain my own for testing purposes at https://github.com/neotinker/rosdistro

This is the ROS default
``` 
ROSDISTRO_INDEX_URL=https://raw.githubusercontent.com/ros/rosdistro/master/index-v4.yaml
```

This points to my development branch. I rebuild it periodically from ros/rosdistro master plus any changes I haven't pushed upstream yet. Use this at your own risk. 
``` 
ROSDISTRO_INDEX_URL=https://raw.githubusercontent.com/neotinker/rosdistro/build_test/index-v4.yaml
```

I make no guarantees about rossuse.py. Use it at your own risk :)

NOTES

- The OBS Project that you are using must exist. rossuse.py wont create it for you.
- rossuse.py looks for its templates in the current working directory.
- ROSDISTRO_INDEX_URL must be exported or set inline with the rossuse.py command if you want to override the default value.

EX)

ADD A SINGLE PACKAGE TO OBS

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.1 --pkg_name ros_comm```

ADD A PACKAGE AND ALL ITS DEPENDENCIES

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.1 --gen_deps --pkg_name ros_comm```

REGENERATE SPEC AND SERVICE FILES FOR A PACKAGE

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.1 --update_existing --pkg_name ros_comm```

REGENERATE SPEC AND SERVICE FILES FOR A PACKAGE AND ALL ITS DEPENDENCIES

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.1 --gen_deps --update_existing --pkg_name ros_comm```


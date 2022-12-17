# rossuse
Generate service and rpm spec files for Opensuse/SLES

This is a first attempt at integrating ROS building/packaging with the Open Build Service.

The script is messy but it works.

By default, it will pull the index-v4.yaml file from https://github.com/ros/rosdistro but you can override the default to point to your own fork of rosdistro using the ROSDISTRO_INDEX_URL environment variable. I maintain my own for testing purposes at https://github.com/neotinker/rosdistro

This is the ROS default
``` 
ROSDISTRO_INDEX_URL=https://raw.githubusercontent.com/ros/rosdistro/master/index-v4.yaml
```

This points to my development fork of rosdistro. You only need to use this fork if you are using my older builds of ROS Melodic. (SEE https://build.opensuse.org/project/show/home:neotinker3:ROS:melodic ). I haven't been merging upstream changes to it in a while so use this at your own risk. 
``` 
ROSDISTRO_INDEX_URL=https://raw.githubusercontent.com/neotinker/rosdistro/build_test/index-v4.yaml
```

If you are using my newer builds (SEE https://build.opensuse.org/project/show/home:neotinker3:ROS:ROS1 ), we use the upstream rosdistro with overrides provided by https://github.com/neotinker/rosdistro-suse so you shouldn't need to define ROSDISTRO_INDEX_URL.

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

REGENERATE SPEC AND SERVICE FILES FOR ALL METAPACKAGES
 SEE https://github.com/ros/metapackages

```./rossuse.py --osc_project <Open Build Service Project name> --rosdistro melodic --os_name opensuse --os_version 15.3 --gen_deps --update_existing --pkg_name desktop_full --pkg_name desktop --pkg_name perception --pkg_name ros_base --pkg_name ros_core --pkg_name robot --pkg_name simulators --pkg_name viz```

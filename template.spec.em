%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^@(InstallationPrefix)/.*$
%global __requires_exclude_from ^@(InstallationPrefix)/.*$

Name:           @(Package)
Version:        @(Version)
Release:        @(RPMInc)%{?dist}
Summary:        ROS @(Name) package

License:        @(License)
Group:          Development/Libraries
@[if Homepage and Homepage != '']URL:            @(Homepage)@\n@[end if]Source0:        @(Source0)
Source1:        ros-rpmlintrc
@{pc = -1}@[for p in Patches]@{pc = pc + 1}Patch@(pc):         @p@\n@[end for]@[if NoArch]@\nBuildArch:      noarch@\n@[end if]@[for p in Depends]Requires:       @p@\n@[end for]@[for p in BuildDepends]BuildRequires:  @p@\n@[end for]@[for p in Conflicts]Conflicts:      @p@\n@[end for]@[for p in Replaces]Obsoletes:      @p@\n@[end for]
%description
@(Description)

%prep
%autosetup -p0 -n @(TarDirName)

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "@(InstallationPrefix)/setup.sh" ]; then . "@(InstallationPrefix)/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
cmake \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_LIBDIR="lib" \
    -DCMAKE_INSTALL_PREFIX="@(InstallationPrefix)" \
    -DCMAKE_PREFIX_PATH="@(InstallationPrefix)" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
@[if Name != 'catkin']    -DCATKIN_BUILD_BINARY_PACKAGE="1" \@\n@[end if]@[if PythonVersion == 2]    -DPYTHON_EXECUTABLE=/usr/bin/python \
@[elif PythonVersion == 3]    -DPYTHON_EXECUTABLE=/usr/bin/python3 \
@[end if]@[if Name == 'catkin']    -DCMAKE_BUILD_TYPE=Release \@\n@[end if]    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "@(InstallationPrefix)/setup.sh" ]; then . "@(InstallationPrefix)/setup.sh"; fi
%make_install -C obj-%{_target_platform}

%files
@(InstallationPrefix)

%changelog

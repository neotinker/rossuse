<package name="@(Name)">

  <title>ROS @(Name) package</title> <!-- Title of package -->

  <description>@(Description)</description> <!-- for long description -->

<!-- following roles are inherited from the parent project
  <person role="maintainer" userid="%(user)s"/>
  <person role="bugowner" userid="%(user)s"/>
-->
<!--
  <url>PUT_UPSTREAM_URL_HERE</url>
-->

<!--
  use one of the examples below to disable building of this package
  on a certain architecture, in a certain repository,
  or a combination thereof:

  <disable arch="x86_64"/>
  <disable repository="SUSE_SLE-10"/>
  <disable repository="SUSE_SLE-10" arch="x86_64"/>

  Possible sections where you can use the tags above:
  <build>
  </build>
  <debuginfo>
  </debuginfo>
  <publish>
  </publish>
  <useforbuild>
  </useforbuild>

  Please have a look at:
  http://en.opensuse.org/Restricted_formats
  Packages containing formats listed there are NOT allowed to
  be packaged in the openSUSE Buildservice and will be deleted!

-->

</package>

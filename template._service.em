<services>
  <service name="obs_scm">
    <param name="scm">git</param>
    <param name="url">@(ReleaseUrl)</param>
    <param name="revision">@(ReleaseTag)</param>
    <param name="versionformat">release</param>
    <param name="filename">@(Name)</param>
  </service>
  <service name="tar" mode="buildtime"/>
  <service name="recompress" mode="buildtime">
    <param name="compression">bz2</param>
    <param name="file">*.tar</param>
  </service>
</services>

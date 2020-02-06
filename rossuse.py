#!/usr/bin/python3

import os, io, yaml, em, argparse, re, textwrap, datetime, sys
from dateutil import tz
from rosdistro import get_distribution, get_index, get_index_url, _get_dist_file_data
from catkin_pkg.package import parse_package_string
from rosdep2 import create_default_installer_context
from rosdep2.catkin_support import get_catkin_view

import osc
import osc.core
import osc.conf

from urllib.parse import quote_plus

# We will assume that we can generate a spec file good for multiple OS/Versions
# based on the output from a single OS/version (opensuse 15.1)
# In the future we should enable defining multiple OS/Versions and insert 
# Conditionals in the derived files (spec,_service, etc)

rdistro = ''
os_name = ''
os_version = ''

def init_environment():
  global os_name, os_version, rdistro, ctx, os_installers, default_os_installer, dist_data, rindex, rcache, rview

  ctx = create_default_installer_context()
  os_installers = ctx.get_os_installer_keys(os_name)
  default_os_installer = ctx.get_default_os_installer_key(os_name)
  rindex = get_index(get_index_url())
  dist_data = _get_dist_file_data(rindex,rdistro,'distribution')
  rcache = get_distribution(rindex,rdistro)
  rview = get_catkin_view(rdistro,os_name, os_version, False)

def generate_package_list():
  global args, os_name, os_version, rdistro, ctx, os_installers, default_os_installer, dist_data, rindex, rcache, rview

  tlist = []

  for tpkg in rcache._distribution_file.release_packages.keys():
    tlist.append(tpkg)

  return tlist

def get_package_dist_info(pkg_name):
  global os_name, os_version, rdistro, ctx, os_installers, default_os_installer, dist_data, rindex, rcache, rview
  return dist_data[0]['repositories'][pkg_name]

def crossref_package(pkg_name):
  global os_name, os_version, rdistro, ctx, os_installers, default_os_installer, dist_data, rindex, rcache, rview
  tmp = rview.lookup(pkg_name)
  tmplist = tmp.get_rule_for_platform(os_name,os_version,os_installers,default_os_installer)

  return tmplist[1]

def rpmify_string(value):
  markup_remover = re.compile(r'<.*?>')
  value = markup_remover.sub('', value)
  value = re.sub('\s+', ' ', value)
  value = '\n'.join([v.strip() for v in textwrap.TextWrapper(width=80,break_long_words=False, replace_whitespace=False).wrap(value)])
  return value

# get_dependency_list - return a list of dependency translated
#   to correct os specific names
# input: list of type catkin_pkg.package.Dependency
# return: a list of strings
def get_dependency_list(dep_list):
  global os_name, os_version, rdistro, ctx, os_installers, default_os_installer, dist_data, rindex, rcache, rview
  tmp_list = []
  for item in dep_list:

    # name == item.name
    # condition == item.condition
    # evaluate_condition == item.evaluate_condition()
    # evaluated_condition == item.evaluated_condition
    # version_eq == item.version_eq
    # version_gt == item.version_gt
    # version_gte == item.version_gte
    # version_lt == item.version_lt
    # version_lte == item.version_lte

    subtmplist = crossref_package(item.name)
    if 'packages' in subtmplist:
      if item.version_eq != None:
        tmp_list.extend([i + " = " + item.version_eq for i in subtmplist['packages']])
      elif item.version_gt != None:
        tmp_list.extend([i + " > " + item.version_gt for i in subtmplist['packages']])
      elif item.version_gte != None:
        tmp_list.extend([i + " >= " + item.version_gte for i in subtmplist['packages']])
      elif item.version_lt != None:
        tmp_list.extend([i + " < " + item.version_lt for i in subtmplist['packages']])
      elif item.version_lte != None:
        tmp_list.extend([i + " <= " + item.version_lte for i in subtmplist['packages']])
      else:
        tmp_list.extend(subtmplist['packages'])
    else:
      if item.version_eq != None:
        tmp_list.extend([i + " = " + item.version_eq for i in subtmplist])
      elif item.version_gt != None:
        tmp_list.extend([i + " > " + item.version_gt for i in subtmplist])
      elif item.version_gte != None:
        tmp_list.extend([i + " >= " + item.version_gte for i in subtmplist])
      elif item.version_lt != None:
        tmp_list.extend([i + " < " + item.version_lt for i in subtmplist])
      elif item.version_lte != None:
        tmp_list.extend([i + " <= " + item.version_lte for i in subtmplist])
      else:
        tmp_list.extend(subtmplist)
  return tmp_list

def get_package_info(pkg_name):
  global os_name, os_version, rdistro, ctx, os_installers, default_os_installer, dist_data, rindex, rcache, rview

  return parse_package_string(rcache.get_release_package_xml(pkg_name))

def get_pkg_data(pkg_name):
  global os_name, os_version, rdistro, ctx, os_installers, default_os_installer, dist_data, rindex, rcache, rview

  pkg_data = {}
  pkg_data['release'] = {}
  pkg_data['catkin_pkg'] = {}
  pkg_data['release']['name'] = rcache._distribution_file.release_packages[pkg_name].name
  pkg_data['release']['repo_name'] = rcache._distribution_file.release_packages[pkg_name].repository_name
  pkg_data['release']['repo_data'] = dist_data[0]['repositories'][pkg_data['release']['repo_name']]['release']

  tmp_catkin_pkg_info = get_package_info(pkg_name)
  if 'urls' in tmp_catkin_pkg_info and len(tmp_catkin_pkg_info['urls']) > 0:
    pkg_data['catkin_pkg']['homepage'] = tmp_catkin_pkg_info['urls'][0].url
  else:
    pkg_data['catkin_pkg']['homepage'] = []
  pkg_data['catkin_pkg']['version'] = tmp_catkin_pkg_info['version']
  pkg_data['catkin_pkg']['licenses'] = tmp_catkin_pkg_info['licenses']
  pkg_data['catkin_pkg']['description'] = tmp_catkin_pkg_info['description']
  pkg_data['catkin_pkg']['exports'] = tmp_catkin_pkg_info['exports']
  pkg_data['catkin_pkg']['maintainers'] = tmp_catkin_pkg_info['maintainers']
  pkg_data['catkin_pkg']['buildtool_export_depends'] = get_dependency_list(tmp_catkin_pkg_info['buildtool_export_depends'])
  pkg_data['catkin_pkg']['test_depends'] = get_dependency_list(tmp_catkin_pkg_info['test_depends'])
  pkg_data['catkin_pkg']['exec_depends'] = get_dependency_list(tmp_catkin_pkg_info['exec_depends'])
  pkg_data['catkin_pkg']['build_depends'] = get_dependency_list(tmp_catkin_pkg_info['build_depends'])
  pkg_data['catkin_pkg']['group_depends'] = get_dependency_list(tmp_catkin_pkg_info['group_depends'])
  pkg_data['catkin_pkg']['doc_depends'] = get_dependency_list(tmp_catkin_pkg_info['doc_depends'])
  pkg_data['catkin_pkg']['build_export_depends'] = get_dependency_list(tmp_catkin_pkg_info['build_export_depends'])
  pkg_data['catkin_pkg']['buildtool_depends'] = get_dependency_list(tmp_catkin_pkg_info['buildtool_depends'])
  pkg_data['catkin_pkg']['replaces'] = get_dependency_list(tmp_catkin_pkg_info['replaces'])
  pkg_data['catkin_pkg']['conflicts'] = get_dependency_list(tmp_catkin_pkg_info['conflicts'])
  
  return pkg_data

def collect_template_data(pkg_data):
  global os_name, os_version, rdistro, ctx, os_installers, default_os_installer, dist_data, rindex, rcache, rview

  url = pkg_data['release']['repo_data']['url'] 
  tag = pkg_data['release']['repo_data']['tags']['release']
  version = pkg_data['release']['repo_data']['version']
  revision = tag.format(package=pkg_data['release']['name'], version=version)

  g = {}
  # Release Repo Url
  g['ReleaseUrl'] = pkg_data['release']['repo_data']['url']
  # Release Repo "tag"
  tag = pkg_data['release']['repo_data']['tags']['release']
  version = pkg_data['release']['repo_data']['version']
  g['ReleaseTag'] = tag.format(package=pkg_data['release']['name'], version=version)
  # Package Name
  g['Name'] = pkg_data['release']['name']

  # InstallationPrefix
  g['InstallationPrefix'] = '/opt/ros/melodic'
  # Package
  g['Package'] = "ros-" + rdistro + "-" + g['Name']
  # Version ( Take the repo version and split it at the hyphen [0] )
  g['Version'] = version.split('-')[0]
  # RPMInc ( Take the repo version and split it at the hyphen [1] )
  g['RPMInc'] = version.split('-')[1]
  # License
  g['License'] = pkg_data['catkin_pkg']['licenses'][0]
  # Homepage
  g['Homepage'] = pkg_data['catkin_pkg']['homepage']
  # Source0 (? taruri)
  g['Source0'] = pkg_data['release']['name'] + "-release.tar.bz2" 
  # NoArch
  g['NoArch'] = False
  for i in pkg_data['catkin_pkg']['exports']:
    if i.tagname == 'architecture_independent':
      g['NoArch'] = True
  # Depends
  g['Depends'] = [ str for str in ( pkg_data['catkin_pkg']['exec_depends'] + pkg_data['catkin_pkg']['buildtool_export_depends'] ) ]
  # BuildDepends
  g['BuildDepends'] = [ str for str in ( pkg_data['catkin_pkg']['test_depends'] + pkg_data['catkin_pkg']['build_depends'] + pkg_data['catkin_pkg']['buildtool_depends'] ) ]
  # Conflicts
  g['Conflicts'] = pkg_data['catkin_pkg']['conflicts']
  # Replaces
  g['Replaces'] = pkg_data['catkin_pkg']['replaces']
  # Description
  g['Description'] = rpmify_string(pkg_data['catkin_pkg']['description'])
  # TarDirName (? tarvername)
  g['TarDirName'] = pkg_data['release']['name'] + "-release"
  # PythonVersion
  g['PythonVersion'] = rindex.distributions[rdistro]['python_version']
  # Changelogs - {change_version, (change_date, main_name, main_email)}
  # change_version = version 
  # change_date = now
  # main_name = maintainers[0].name
  # email = maintainers[0].email
  stamp = datetime.datetime.now(tz.tzlocal()).strftime('%a %b %d %Y')
  g['changelogs'] = [(version,(stamp,pkg_data['catkin_pkg']['maintainers'][0].name,pkg_data['catkin_pkg']['maintainers'][0].email))]

  return g

def generate__service_file(g):
  global os_name, os_version, rdistro, ctx, os_installers, default_os_installer, dist_data, rindex, rcache, rview

  interpreter = em.Interpreter(output=open(g['osc_project'] + '/' + g['osc_package'] + '/_service', "w"))
  interpreter.include('template._service.em',g)
  interpreter.shutdown()

def generate_spec_file(g):
  global os_name, os_version, rdistro, ctx, os_installers, default_os_installer, dist_data, rindex, rcache, rview

  interpreter = em.Interpreter(output=open(g['osc_project'] + '/' + g['osc_package'] + '/' + g['Name'] + '.spec', "w"))
  interpreter.include('template.spec.em',g)
  interpreter.shutdown()

def generate_pkg_meta_file(g):
  global os_name, os_version, rdistro, ctx, os_installers, default_os_installer, dist_data, rindex, rcache, rview
  output = io.StringIO("")

  interpreter = em.Interpreter(output=output)
  interpreter.include('template.pkg_meta.em',g)
  retval = output.getvalue()
  interpreter.shutdown()

  return retval

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Generate an files for building rpms')
  parser.add_argument('--template', help='Define a templte to use for generating spec file')
  parser.add_argument('--osc_project', required=True, help='OSC project where we will be pushing generated files. You need to create this through OSC prior to use.')
  parser.add_argument('--rosdistro', required=True, help='ROS Distribution to generate files for')
  parser.add_argument('--os_name', required=True, help='The OS to generate files for')
  parser.add_argument('--os_version', required=True, help='The OS version to generate files for')
  parser.add_argument('--generate_all', action='store_true', default=False, required=False, help='Generate files for all packages. By default only generate files for packages not osc project')
  parser.add_argument('--dry_run', action='store_true', default=False, required=False, help='Dont generate any files or commit them to osc')
  parser.add_argument('--pkg_name', action='append', help='The package to generate files for')
  parser.add_argument('--meta', help='Generate files for Metapackage(s) instead of \'regular\' packages', action="store_true", default=False, required=False) 

  args = parser.parse_args()

  # process args
  if args.os_name != None:
    os_name = args.os_name
  else:
    os_name = 'opensuse'

  if args.os_version != None:
    os_version = args.os_version
  else:
    os_version = '15.1'

  if args.rosdistro != None:
    rdistro = args.rosdistro
  else:
    rdistro = 'melodic'

  # This could be a meta package regular package or all packages.
  if args.pkg_name != None:
    pkg_name = args.pkg_name
  else:
    # If no package is specified, then do 'all'
    pkg_name = None

  # Get data from rosdep
  init_environment()

  # Initialize OSC
  osc.conf.get_config()
  apiurl = osc.conf.config['apiurl']
  project = args.osc_project
  if osc.core.is_project_dir(project):
    # Project has already been checked out
    prj = osc.core.Project(project)
  else:
    # Project directory does not exist yet
    prj = osc.core.Project.init_project(apiurl,project,project,osc.conf.config['do_package_tracking'])

  # A package can be a "metapackage" and/or a "regular" package
  # We build rpms for "regular" packages
  # "metapackages" are patterns (not sure about building them yet)
  # Sometimes a name can be shared by both a meta and regular package

  # Generate list of packages 
  if pkg_name == None:
    # Get a list of all packages
    # This currently includes Meta and Regular packages
    pkg_list = generate_package_list()
  else:
    pkg_list = pkg_name

  ptot = len(pkg_list)
  pcounter = 0
  scounter = 0
  fcounter = 0
  for p in sorted(pkg_list):

    pcounter += 1
    print("{}/{} Looking for package data for {}".format(pcounter,ptot,p))

    try:
      pkg_data = get_pkg_data(p)
      template_data = collect_template_data(pkg_data)
      template_data['osc_project'] = project
      template_data['osc_package'] = p

      print("Found package data for {}".format(p))
      if p in osc.core.meta_get_packagelist(apiurl,project) and not args.generate_all:
        print("{} exists. Skipping".format(p))
        continue
      elif p in osc.core.meta_get_packagelist(apiurl,project):
        # Checkout package info
        if not args.dry_run:
          osc.core.checkout_package(apiurl,project,p,prj_dir=project)
      else:
        # Doesn't exist in project so initialize a new package
        print("We should create a new package for {} but I don't know how yet. so skip".format(p))
        f=generate_pkg_meta_file(template_data)
        if not args.dry_run:
          osc.core.edit_meta(metatype='pkg',data=f,apiurl=apiurl,path_args=(quote_plus(project), quote_plus(p)))
          # Checkout package info
          osc.core.checkout_package(apiurl,project,p,prj_dir=project)

    except Exception:
      e = sys.exc_info()
      print("We had problems with {}".format(p))
      print(e)
      fcounter += 1
      continue

    scounter += 1

    # Pull data to directory using oSC (if it exists)
    # This should create a directory.
    # If it doesn't then we will need to do it manually

    print("Generating files for {}".format(p))
    if not args.dry_run:
      generate_spec_file(template_data)
      generate__service_file(template_data)

    # checkin generated files using osc

    # Flush stdout
    sys.stdout.flush()

  # Print breakdown of results
  print("packages (total):{}".format(pcounter))
  print("packages (success):{}".format(scounter))
  print("packages (failure):{}".format(fcounter))


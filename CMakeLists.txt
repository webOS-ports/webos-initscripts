# Copyright (c) 2007-2018 LG Electronics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 2.8.7)

project(webos-initscripts C CXX)

include(webOS/webOS)
webos_modules_init(1 0 0 QUALIFIER RC7)
webos_component(3 0 0)

webos_distro_dep()
webos_distro_variant_dep()

add_subdirectory(src/initctl)
add_subdirectory(src/utils)

##### overrides #####
set(systemd_override
    files/systemd/overrides/multi-user.target.wants)

if(${WEBOS_TARGET_DISTRO} STREQUAL "webos")
    set(systemd_distro_override
        files/systemd/overrides/webos-cbd.target.wants)
endif()

set(systemd_enable_systemd_environments
    files/systemd/scripts/common/get-systemd-environments.sh)

##### services & targets #####
set(systemd_units
    files/systemd/targets/default-webos.target
    files/systemd/targets/webos-bd.target
    files/systemd/targets/webos-cbd.target
    files/systemd/targets/webos-dis.target
    files/systemd/targets/webos-ibd.target
    files/systemd/targets/webos-mbd.target
    files/systemd/targets/webos-rbd.target)

##### tmpfiles #####
webos_configure_source_files(systemd_in_tmpfile
    files/systemd/tmpfiles/30-run.conf
    files/systemd/tmpfiles/31-var.conf)

# install override
install(DIRECTORY
    ${systemd_override}
    ${systemd_distro_override}
    DESTINATION ${WEBOS_INSTALL_SYSCONFDIR}/systemd/system)

# install support to enable systemd environments on console
install(PROGRAMS
    ${systemd_enable_systemd_environments}
    DESTINATION ${WEBOS_INSTALL_SYSCONFDIR}/profile.d)

# install systemd units
install(FILES
    ${systemd_units}
    DESTINATION ${WEBOS_INSTALL_SYSCONFDIR}/systemd/system)

# install temp files
install(FILES
    ${systemd_tmpfile}
    ${systemd_in_tmpfile}
    DESTINATION ${WEBOS_INSTALL_SYSCONFDIR}/tmpfiles.d)

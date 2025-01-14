# Copyright 2019 The Meson development team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Mixins for compilers that *are* linkers.

While many compilers (such as gcc and clang) are used by meson to dispatch
linker commands and other (like MSVC) are not, a few (such as DMD) actually
are both the linker and compiler in one binary. This module provides mixin
classes for those cases.
"""

import os
import shlex
import typing

from ... import mesonlib

if typing.TYPE_CHECKING:
    from ...coredata import OptionDictType
    from ...environment import Environment


class LinkerEnvVarsMixin:

    """Mixin reading LDFLAGS from the environment."""

    def get_linker_args_from_envvars(self) -> typing.List[str]:
        flags = os.environ.get('LDFLAGS')
        if not flags:
            return []
        return shlex.split(flags)


class BasicLinkerIsCompilerMixin:

    """Provides a baseline of methods that a linker would implement.

    In every case this provides a "no" or "empty" answer. If a compiler
    implements any of these it needs a different mixin or to override that
    functionality itself.
    """

    def sanitizer_link_args(self, value: str) -> typing.List[str]:
        return []

    def get_lto_link_args(self) -> typing.List[str]:
        return []

    def can_linker_accept_rsp(self) -> bool:
        return mesonlib.is_windows()

    def get_linker_exelist(self) -> typing.List[str]:
        return self.exelist.copy()

    def get_linker_output_args(self, output: str) -> typing.List[str]:
        return []

    def get_linker_always_args(self) -> typing.List[str]:
        return []

    def get_linker_lib_prefix(self) -> str:
        return ''

    def get_option_link_args(self, options: 'OptionDictType') -> typing.List[str]:
        return []

    def has_multi_link_args(self, args: typing.List[str], env: 'Environment') -> typing.Tuple[bool, bool]:
        return False, False

    def get_link_debugfile_args(self, targetfile: str) -> typing.List[str]:
        return []

    def get_std_shared_lib_link_args(self) -> typing.List[str]:
        return []

    def get_std_shared_module_args(self, options: 'OptionDictType') -> typing.List[str]:
        return self.get_std_shared_lib_link_args()

    def get_link_whole_for(self, args: typing.List[str]) -> typing.List[str]:
        raise mesonlib.EnvironmentException(
            'Linker {} does not support link_whole'.format(self.id))

    def get_allow_undefined_args(self) -> typing.List[str]:
        raise mesonlib.EnvironmentException(
            'Linker {} does not support allow undefined'.format(self.id))

    def get_pie_link_args(self) -> typing.List[str]:
        m = 'Linker {} does not support position-independent executable'
        raise mesonlib.EnvironmentException(m.format(self.id))

    def get_undefined_link_args(self) -> typing.List[str]:
        return []

    def get_coverage_link_args(self) -> typing.List[str]:
        m = "Linker {} doesn't implement coverage data generation.".format(self.id)
        raise mesonlib.EnvironmentException(m)

    def no_undefined_link_args(self) -> typing.List[str]:
        return []

    def bitcode_args(self) -> typing.List[str]:
        raise mesonlib.MesonException("This linker doesn't support bitcode bundles")

    def get_soname_args(self, for_machine: 'mesonlib.MachineChoice',
                        prefix: str, shlib_name: str, suffix: str, soversion: str,
                        darwin_versions: typing.Tuple[str, str],
                        is_shared_module: bool) -> typing.List[str]:
        raise mesonlib.MesonException("This linker doesn't support soname args")

    def build_rpath_args(self, env: 'Environment', build_dir: str, from_dir: str,
                         rpath_paths: str, build_rpath: str,
                         install_rpath: str) -> typing.List[str]:
        return []

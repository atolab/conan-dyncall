# http://www.dyncall.org/r1.0/dyncall-1.0.tar.gz
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools


class DynCallConan(ConanFile):
    name = 'dyncall'
    version = '09132016'
    description = "A Generic Dynamic FFI package"
    url = "https://github.com/k0ekk0ek/conan-dyncall"
    homepage = "http://www.dyncall.org"
    # DynCall uses a custom license, modeled after the ISC license.
    license = "dyncall"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    repository = 'https://github.com/Snaipe/dyncall.git'
    branch = 'master'
    commit = '51e79a84fd91881d7424b28271c6dda4e0d97c11'

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        self.run('git clone --branch={0} {1} {2}'
            .format(self.branch, self.repository, self.source_subfolder))
        self.run('git -C {0} checkout {1}'
            .format(self.source_subfolder, self.commit))

    def configure_cmake(self):
        cmake = CMake(self)
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == 'Windows' and self.settings.arch == 'x86':
            self.cpp_info.exelinkflags.append('/SAFESEH:NO')
            self.cpp_info.sharedlinkflags.append('/SAFESEH:NO')


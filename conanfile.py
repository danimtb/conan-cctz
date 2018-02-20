#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.errors import ConanException
import os


class CCTZConan(ConanFile):
    name = "cctz"
    version = "2.2"
    url = "https://github.com/bincrafters/conan-cctz"
    description = "C++ library for translating between absolute and civil times"
    license = "Apache 2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    source_subfolder = "source_subfolder"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "build_tools" : [True, False],
        "build_testing" : [True, False],
        "build_examples" : [True, False]
    }

    default_options = (
        "shared=False", 
        "build_tools=False",
        "build_testing=False", 
        "build_examples=False"
    )

    def requirements(self):
        if self.options.build_testing:
            self.requires("gtest/1.8.0@conan/stable")

    def configure(self):
        if self.settings.compiler in [ "gcc", "clang" ] and self.settings.compiler.libcxx != 'libstdc++11':
            raise ConanException('cctz requires libstdc++11, but was passed:' + str(self.settings.compiler.libcxx))

    def source(self):
        source_url = "https://github.com/google/cctz"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

        # this is a specific patch to the CMakeLists.txt which MUST be remove iff ( cctz version > 2.2 )
        _cmakelists_new = "https://raw.githubusercontent.com/google/cctz/8768b6d02283f6226527c1a7fb39c382ddfb4cec/CMakeLists.txt"
        _cmakelists_old = os.path.join(self.source_subfolder, "CMakeLists.txt")
        tools.download(_cmakelists_new, _cmakelists_old, overwrite=True)


    def build(self):
        cmake = CMake(self)
        cmake.verbose = True
        cmake.definitions["BUILD_TOOLS"] = self.options.build_tools
        cmake.definitions["BUILD_EXAMPLES"] = self.options.build_examples
        cmake.definitions["BUILD_TESTING"] = self.options.build_testing
        if self.settings.compiler == "Visual Studio":
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = self.options.shared
        cmake.configure()
        cmake.build()

    def package(self):
        include_folder = os.path.join(self.source_subfolder, "include")
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        if self.settings.compiler in [ "gcc", "clang" ]:
            self.cpp_info.cppflags = ["-std=c++11"]


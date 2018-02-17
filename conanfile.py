#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
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
        "build_testing" : [True, False], 
        "build_examples" : [True, False]
    }
    
    default_options = (
        "shared=False", 
        "build_testing=False", 
        "build_examples=False"
    )
    
    def requirements(self):
        if self.options.build_testing:
            self.requires("gtest/1.8.0@conan/stable")
            
    def source(self):
        source_url = "https://github.com/google/cctz"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)


    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_EXAMPLES"] = self.options.build_examples
        cmake.definitions["BUILD_TESTING"] = self.options.build_testing
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
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
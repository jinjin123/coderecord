# -*- encoding: utf-8 -*-

Gem::Specification.new do |s|
  s.name = "win32-dir"
  s.version = "0.4.9"

  s.required_rubygems_version = Gem::Requirement.new(">= 0") if s.respond_to? :required_rubygems_version=
  s.authors = ["Daniel J. Berger", "Park Heesob"]
  s.date = "2014-07-02"
  s.description = "    The win32-dir library provides extra methods and constants for the\n    builtin Dir class. The constants provide a convenient way to identify\n    certain directories across all versions of Windows. Some methods have\n    been added, such as the ability to create junctions. Others have been\n    modified to provide a more consistent result for MS Windows.\n"
  s.email = "djberg96@gmail.com"
  s.extra_rdoc_files = ["README", "CHANGES", "MANIFEST"]
  s.files = ["README", "CHANGES", "MANIFEST"]
  s.homepage = "http://github.com/djberg96/win32-dir"
  s.licenses = ["Artistic 2.0"]
  s.require_paths = ["lib"]
  s.required_ruby_version = Gem::Requirement.new(">= 1.9.2")
  s.rubygems_version = "1.8.24"
  s.summary = "Extra constants and methods for the Dir class on Windows."

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_runtime_dependency(%q<ffi>, [">= 1.0.0"])
      s.add_development_dependency(%q<rake>, [">= 0"])
      s.add_development_dependency(%q<test-unit>, [">= 2.4.0"])
    else
      s.add_dependency(%q<ffi>, [">= 1.0.0"])
      s.add_dependency(%q<rake>, [">= 0"])
      s.add_dependency(%q<test-unit>, [">= 2.4.0"])
    end
  else
    s.add_dependency(%q<ffi>, [">= 1.0.0"])
    s.add_dependency(%q<rake>, [">= 0"])
    s.add_dependency(%q<test-unit>, [">= 2.4.0"])
  end
end

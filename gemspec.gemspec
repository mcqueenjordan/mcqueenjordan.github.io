# encoding: utf-8

Gem::Specification.new do |s|
  s.name = "whoami.sh"
  s.authors = ["Jordan McQueen"]
  s.summary = "This field is required? What a drag."
  s.version = "0.0.4"
  s.files = `git ls-files -z`.split("\x0").select do |f|
    f.match(%r{^((_includes|_layouts|_sass|assets)/|(LICENSE|README)((\.(txt|md|markdown)|$)))}i)
  end

  s.platform = Gem::Platform::RUBY
  s.add_runtime_dependency "jekyll", "~> 3.3"
end

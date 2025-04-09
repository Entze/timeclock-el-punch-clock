check: check-all-justfile check-all-toml check-all-yaml check-python-buildtool check-all-python

import 'check/justfile.just'
import 'check/python-buildtool.just'
import 'check/toml.just'
import 'check/yaml.just'
import 'check/python.just'

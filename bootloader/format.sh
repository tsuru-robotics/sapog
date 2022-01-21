#!/bin/bash

clang-format -i -fallback-style=none -style=file $(find src -name '*.[ch]pp')

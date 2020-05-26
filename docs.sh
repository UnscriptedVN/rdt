#!/bin/sh

pdoc3 --html renpy_distribute_tools --output docs
mv docs/renpy_distribute_tools/* docs/
rm -r docs/renpy_distribute_tools

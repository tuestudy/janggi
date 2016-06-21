#!/bin/sh

cd $(dirname "$0")
PYTHONPATH=..:core python -m janggi.gui.main "$@"

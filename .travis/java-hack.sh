#!/bin/bash
set -ev

# This may become ineffective if Oracle Java 7 ceases to be the default VM.
# We really need multiple language support
if [ "${JDK}" = "oraclejdk8" ]; then
  sudo apt-get install oracle-java8-installer
fi

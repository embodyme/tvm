#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

. /etc/profile

set -o errexit -o nounset
set -o pipefail

GRADLE_HOME=/opt/gradle
GRADLE_VERSION=5.6.4
GRADLE_SHA256=1f3067073041bc44554d0efe5d402a33bc3d3c93cc39ab684f308586d732a80d

echo "Downloading Gradle"
wget -q --output-document=gradle.zip "https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip"
echo "Checking Gradle hash"
echo "${GRADLE_SHA256} *gradle.zip" | sha256sum --check -
echo "Installing Gradle"
unzip gradle.zip
rm gradle.zip
mv "gradle-${GRADLE_VERSION}" "${GRADLE_HOME}/"
ln --symbolic "${GRADLE_HOME}/bin/gradle" /usr/bin/gradle

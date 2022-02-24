<!--- Licensed to the Apache Software Foundation (ASF) under one -->
<!--- or more contributor license agreements.  See the NOTICE file -->
<!--- distributed with this work for additional information -->
<!--- regarding copyright ownership.  The ASF licenses this file -->
<!--- to you under the Apache License, Version 2.0 (the -->
<!--- "License"); you may not use this file except in compliance -->
<!--- with the License.  You may obtain a copy of the License at -->

<!---   http://www.apache.org/licenses/LICENSE-2.0 -->

<!--- Unless required by applicable law or agreed to in writing, -->
<!--- software distributed under the License is distributed on an -->
<!--- "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY -->
<!--- KIND, either express or implied.  See the License for the -->
<!--- specific language governing permissions and limitations -->
<!--- under the License. -->

# EmbodyMe TVM

Resources

* TVM Docs, ["Install TVM from Source"](https://tvm.apache.org/docs/install/from_source.html)
* TVM Docs, ["Deploy the Pretrained Model on Android"](https://tvm.apache.org/docs/how_to/deploy_models/deploy_model_on_android.html)
* TVM Docs, ["Deploy to Android"](https://tvm.apache.org/docs/how_to/deploy/android.html)
* TVM GitHub, ["Android RPC Server for TVM"](https://github.com/apache/tvm/tree/main/apps/android_rpc)
* TVM GitHub, ["TVM4J - Java Frontend for TVM Runtime"](https://github.com/apache/tvm/blob/main/jvm/README.md)
* TVM GitHub, ["Android TVM Demo"](https://github.com/apache/tvm/blob/main/apps/android_deploy/README.md#build-and-installation)
* jangrewe @ GitHub, ["Dockerfile for Android SDK"](https://github.com/jangrewe/gitlab-ci-android/blob/master/Dockerfile)
* Android Docs, ["Android Remote Procedure Calls (RPCs)"](https://www.androidcookbook.info/android-system/remote-procedure-calls.html)
* Android Docs, ["Android Gradle Plugin Compatability Table"](https://developer.android.com/studio/releases/gradle-plugin)

## Using the Android Dockerfile

> *NOTE (Ben)*:  I am using Ubuntu 20.04.  Commands may be different on Mac or Windows.

### Step 1:  Build the Docker Image

Navigate to the directory where you want to store the TVM source code.  I recommend `~/tvm` or `/opt/tvm`, but it can go anywhere.  Now, run:

```bash
git clone --recursive https://github.com/apache/tvm tvm
cd tvm
docker build -t tvm.demo_android -f docker/Dockerfile.demo_android ./docker
```

If the build succeeds, your docker image should have working copies of:
* TVM (and TVM4J)
* Android SDK / NDK. 

> *NOTE (Ben)*: The dockerfile in the original `tvm` repository has some conflicts (the image contains an old version of `cmake`, but the scripts use commands for the new version).  I had to make a few changes to get it to work on my machine.  I also modified the `CMakeLists.txt` file to correctly set up [GoogleTest](https://google.github.io/googletest/quickstart-cmake.html).  The `embodyme/tvm` fork includes all these changes.


### Step 2:  Run the Docker Container

The docker container can be started with the following command, which launches an interactive shell.  Notice that we map port 9190 in the container to port 9190 on the host machine.

```bash
docker run --pid=host -h tvm --privileged -v $PWD:/workspace        -w /workspace -p 9190:9190 --name tvm -it --rm tvm.demo_android bash
```

You can run `docker exec -it tvm bash` to open a new shell in the container.

### Troubleshooting

If you have connected an Android device via USB, but it doesn't show up when running `adb devices` in the docker container, [run `adb kill-server` *outside* the docker container](https://stackoverflow.com/a/49003099) to make sure there aren't two `adb` daemons running.  Make sure you are running the docker container with the `--privileged` option.

## Evaluating TVM Performance on Android







<img src=https://raw.githubusercontent.com/apache/tvm-site/main/images/logo/tvm-logo-small.png width=128/> Open Deep Learning Compiler Stack
==============================================
[Documentation](https://tvm.apache.org/docs) |
[Contributors](CONTRIBUTORS.md) |
[Community](https://tvm.apache.org/community) |
[Release Notes](NEWS.md)

[![Build Status](https://ci.tlcpack.ai/buildStatus/icon?job=tvm/main)](https://ci.tlcpack.ai/job/tvm/job/main/)
[![WinMacBuild](https://github.com/apache/tvm/workflows/WinMacBuild/badge.svg)](https://github.com/apache/tvm/actions?query=workflow%3AWinMacBuild)

Apache TVM is a compiler stack for deep learning systems. It is designed to close the gap between the
productivity-focused deep learning frameworks, and the performance- and efficiency-focused hardware backends.
TVM works with deep learning frameworks to provide end to end compilation to different backends.

License
-------
TVM is licensed under the [Apache-2.0](LICENSE) license.

Getting Started
---------------
Check out the [TVM Documentation](https://tvm.apache.org/docs/) site for installation instructions, tutorials, examples, and more.
The [Getting Started with TVM](https://tvm.apache.org/docs/tutorial/introduction.html) tutorial is a great
place to start.

Contribute to TVM
-----------------
TVM adopts apache committer model, we aim to create an open source project that is maintained and owned by the community.
Check out the [Contributor Guide](https://tvm.apache.org/docs/contribute/).

Acknowledgement
---------------
We learned a lot from the following projects when building TVM.
- [Halide](https://github.com/halide/Halide): Part of TVM's TIR and arithmetic simplification module
  originates from Halide. We also learned and adapted some part of lowering pipeline from Halide.
- [Loopy](https://github.com/inducer/loopy): use of integer set analysis and its loop transformation primitives.
- [Theano](https://github.com/Theano/Theano): the design inspiration of symbolic scan operator for recurrence.

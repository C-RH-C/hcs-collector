# hcs_collector_scripting
The files in this repo will allow you to build a container running the [hcs-collector](https://github.com/C-RH-C/hcs-collector) and run **collect** and **process** jobs directly using the appropriate scripts.

## File descriptions
- **Containerfile** has the definitions for building the container
- **hcs_collect.conf** is the configuration file for the hcs_collector
- **collect.sh** is the script used for running the collection job
- **process.sh** is the script used for running the processing job

## Exporting the token as a variable.
```export TOKEN=<value of token>``` Create a variable and assign it to the token you will use for the session.

## Running the container
```podman run``` will be used with certain flags in order to run the container properly.
- ```podman run -v SOURCE-VOLUME:/CONTAINER-DIR``` This option will mount the named volume from the host into the container.
- ```podman run -e $TOKEN``` A token value needs to be passed in, this will replace the empty token variable in the **Containerfile**.

## Examples
- ```podman run -it -v /tmp/hcs:/a/b/hcs-data -e TOKEN=$TOKEN quay.io/prey/hcs-collector:1 /hcs-collector/collect.sh```
This command runs the collect script in the container.

- ```podman run -it -v /tmp/hcs:/a/b/hcs-data -e TOKEN=$TOKEN quay.io/prey/hcs-collector:1 /hcs-collector/process.sh```
This command runs the process script in the container.

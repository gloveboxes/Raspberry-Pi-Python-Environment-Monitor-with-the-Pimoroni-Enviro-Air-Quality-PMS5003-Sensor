# Developing IoT Edge Solutions on Linux

Focus of this article are my experiences building an Azure IoT Edge solution with Python and targeting IoT Edge running on a Linux Host, both desktop x64 and arm32v7 (Raspberry Pi).

This article should be read in conjunction with the [Azure IoT Edge documents and tutorials](https://docs.microsoft.com/en-us/azure/iot-edge/).

## Developer Productivity

Building for IoT Edge is not too dissimilar from building a mobile app as there is a level of indirection as soon as you start developing, deploying and testing your code to a device. Everything becomes slower from deploying code across the network, to starting the code on a lower powered device, to remotely attaching a debugger. My recommendation is that you aim to build and test as much as you can on your developer machine before you start deploying and testing on an Iot Edge device.

### Solution architecture

Think of your solution as a set of (micro) services with defined contracts that can communicate via messages or REST calls. In the world of IoT Edge these are called modules and are synonymous with Docker containers. You should code defensively across network boundaries and plan for failure using various [circuit breaker](https://en.wikipedia.org/wiki/Circuit_breaker_design_pattern)/backoff strategies because at some point the services you call will not be available for a number of reasons including but not limited to service updates.

The following example is the approach I took for backing off requests to the Image Classification Service.

```python
retry = 0
while retry < maxRetry:
    try:
        response = requests.post(self.imageProcessingEndpoint, headers=headers,
                                params=self.imageProcessingParams, data=frame)
        break
    except:
        retry = retry + 1
        print('Image Classification REST Endpoint - Retry attempt # ' + str(retry))
        time.sleep(retry)

if retry >= maxRetry:
    return []
```

### Naming Convention

As a general rule use lower case names for modules. This is especially important if making REST calls from Python modules as the Python Requests
package and the get call will lower case the endpoint name and the IoT Edge runtime will not resolve the request against modules that use mixed case names.

1. Environment variables - UPPERCASE
1. Modules Names in lowercase

Modules you need to write and modules you don’t

Microsoft 1st party

- https://docs.microsoft.com/en-au/azure/stream-analytics/stream-analytics-edge 
- https://docs.microsoft.com/en-us/azure/iot-edge/how-to-store-data-blob 
- https://docs.microsoft.com/en-us/azure/iot-edge/how-to-ci-cd 

IoT Edge Extensions

Use the Visual Studio IoT Edge Extension to scaffold your solution. This will create your project structure, the modules, dockerfiles and the deployment.json file which instructs IoT Edge what modules to load their version and location to pull from.

There is nothing to stop you closing the overall solution and opening each individual module in Visual Studio Code. It can make the development simpler, and enable others to work on other modules more easily. 

Building for IoT edge is like building for mobile, the code, deploy, test, debug cycle is elongated as there is a degree of indirection. Everything takes longer as you typically need to get the code to the device, starting a remote debugging session takes longer, stepping through the code over a network connect is slower etc - you get the idea.

Exceptions

Ensure all REST calls to modules are wrapped in exception handlers with some sort of retry/back off mechanism as modules maybe be in indeterminate states - it could be starting after a system boot, it might be being updated and the IoT Edge runtime has torn down the existing module in readiness to start the new version of the module. 

Build as much as you can on your development PC

So when building a solution develop as much as you can on your developer desktop and mock out physical sensors that you may not have access to on your desktop. The easiest way is to set an environment variable to toggle between mocked and real sensors. Make a note of all of the Python PIP packages you use as you'll need to added them to the docker pip requirements file when you come to build the docker image.

Mock out REST APIs with Function Proxies

See Dean's article on Function proxies

Linux example

Windows example

Python example with .env file

So you have a viable module to start testing with IoT Edge 

First you need to Dockerise your module. When you created a module with IoT Edge it also created dockerfile as a start point for your solution.
You'll need to customize the dockerfile to ensure all the prerequisites libraries and Python packages for the module are loaded in to the image. 

If you are cross compiling for another processor architecture then allow a lot of time for building an image - the example … 
took close to an hour to build.

Dockerise

If possible then use the same Docker base image as it will reduce the number of docker layers that need to be distributed to a device. 

https://hub.docker.com/r/microsoft/azureiotedge-azure-stream-analytics/ 

## IoT Edge Module Create Options

Build local, then Dockerise then wrap up as an IoT Module

1. Run a Local Docker Registry

- https://docs.docker.com/registry/deploying/
- docker run -d -p 5000:5000 --restart=always --name registry registry:2

## Disk Space Management

Docker images accumulate fast and gobble up disk space. So run a regular job to clean up old containers and images.

## Debugging

1. Python 4 and multi Threaded
2. https://code.visualstudio.com/docs/python/debugging
3. [Flask Apps](https://code.visualstudio.com/docs/python/debugging#_flask-debugging)
4. Local into a container running in the context of Iot Edge

## Microsoft 1st Party Modules

**FastAPI** has a very powerful but intuitive **<abbr title="also known as components, resources, providers, services, injectables">Dependency Injection</abbr>** system.

It is designed to be very simple to use, and to make it very easy for any developer to integrate other components with **FastAPI**.

## "Dependency Injection"?

**"Dependency Injection"** means, in programming, that there is a way for your code (in this case, your path operation functions) to declare things that it requires to work and use.

And then, that system (in this case **FastAPI**) will take care of doing whatever is needed to provide your code with that thing that it needs.

If you look at it, path operation functions are declared to be used whenever a path and operation matches, and then **FastAPI** will take care of calling the function with the correct parameters and use the response.

Actually, all (or most) of the web frameworks work in this same way.

You never call those functions directly. The are called by your framework (in this case, **FastAPI**).

With the Dependency Injection system, you can also tell **FastAPI** that your path operation function also "depends" on something else that should be executed before your path operation function, and **FastAPI** will take care of executing it and "injecting" the results.

Other common terms for this same idea are:

* resources
* providers
* services
* injectables

## **FastAPI** plug-ins

Integrations and "plug-in"s can be built using the **Dependency Injection** system. But in fact, there is actually **no need to create "plug-ins"**, as by using dependencies it's possible to declare an infinite number of integrations and interactions that become available to your path operation functions.

And dependencies can be created in a very simple and intuitive way that allow you to just import the Python packages you need, and integrate them with your API functions in a couple of lines of code, _literally_.

## **FastAPI** compatibility

The simplicity of the dependency injection system makes **FastAPI** compatible with:

* all the relational databases
* NoSQL databases
* external packages
* external APIs
* authentication and authorization systems
* API usage monitoring systems
* response data injection systems
* etc.


## Simple and Powerful

Although the hierarchical dependency injection system is very simple to define and use, it's still very powerful.

You can define dependencies that in turn can define dependencies themselves.

In the end, a hierarchical tree of dependencies is built, and the **Dependency Injection** system takes care of solving all these dependencies for you (and your dependencies) and providing the results at each step.

## Integrated with OpenAPI

All these dependencies, while declaring their requirements, might have been adding parameters, validations, etc. to your path operations. 

**FastAPI** will take care of adding it all to the OpenAPI schema, so that it is shown in the interactive documentation systems.

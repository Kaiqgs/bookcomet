"""
Object Reference
    Objects can be accessed via object references. To invoke a method in an object, the object reference and method name are given, together with any arguments.
Interfaces
    An interface provides a definition of the signature of a set of methods without specifying their implementation. An object will provide a particular interface if its class contains code that implement the method of that interface. An interface also defines types that can be used to declare the type of variables or parameters and return values of methods.
Actions
    An action in object-oriented programming (OOP) is initiated by an object invoking a method in another object. An invocation can include additional information needed to carry out the method. The receiver executes the appropriate method and then returns control to the invoking object, sometimes supplying a result.
Exceptions
    Programs can encounter various errors and unexpected conditions of varying seriousness. During the execution of the method many different problems may be discovered. Exceptions provide a clean way to deal with error conditions without complicating the code. A block of code may be defined to throw an exception whenever particular unexpected conditions or errors arise. This means that control passes to another block of code that catches the exception.
"""
# ABOUT DOMAIN MODEL:
# - you can replace one implementation with another at a later time.
# - you can unit test your controller when needed.


#from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

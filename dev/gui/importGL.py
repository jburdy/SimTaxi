#essais d'importer OpenGL pour wxWindows
try:
    #le packetage opengl peut être trouve ici :
    #http://PyOpenGL.sourceforge.net/
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
    haveOpenGL = True
except ImportError:
    haveOpenGL = False

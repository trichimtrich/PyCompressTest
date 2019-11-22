## python-quicklz

- Change module name to "python_quicklz" for importing

- Commit [45806bd13d654fa883ce64dc59d4e14b4005acd5](https://github.com/sergey-dryabzhinsky/python-quicklz/tree/45806bd13d654fa883ce64dc59d4e14b4005acd5)

```patch
diff --git a/quicklzpy.c b/quicklzpy.c
index e30638c..2d095e7 100644
--- a/quicklzpy.c
+++ b/quicklzpy.c
@@ -438,7 +438,7 @@ static int myextension_clear(PyObject *m) {

 static struct PyModuleDef moduledef = {
         PyModuleDef_HEAD_INIT,
-        "quicklz",
+        "python_quicklz",
         "QuickLZ module",
         sizeof(struct module_state),
         QuicklzMethods,
@@ -451,7 +451,7 @@ static struct PyModuleDef moduledef = {
 #define INITERROR return NULL

 PyObject *
-PyInit_quicklz(void)
+PyInit_python_quicklz(void)
 #else

 #define INITERROR return
@@ -469,7 +469,7 @@ initquicklz(void)
 #if PY_MAJOR_VERSION >= 3
     PyObject *module = PyModule_Create(&moduledef);
 #else
-    PyObject *module = Py_InitModule("quicklz", QuicklzMethods);
+    PyObject *module = Py_InitModule("python_quicklz", QuicklzMethods);
 #endif

     if (module == NULL)
diff --git a/setup.py b/setup.py
index da10a86..ae3546f 100644
--- a/setup.py
+++ b/setup.py
@@ -1,7 +1,7 @@
 from distutils.core import setup, Extension

 setup(
-    name = "quicklz",
+    name = "python_quicklz",
     version = "1.5.0",
     description="QuickLZ Bindings for Python",
     author='Sergey Dryabzhinsky',
@@ -9,7 +9,7 @@ setup(
     url='https://github.com/sergey-dryabzhinsky/python-quicklz',
     ext_modules = [
         Extension(
-            "quicklz",
+            "python_quicklz",
             ["quicklz.c", "quicklzpy.c"],
             extra_compile_args=[
                "-O2",
```

## pyqlz

- Fix the uncompile-able code

- [pyqlz-1.5.5.tar.gz](https://files.pythonhosted.org/packages/ef/cc/4d04d7e4ab9ee83e51af37d8fc90b7d6a5b46b3e47cb83c60f340f53d5ee/pyqlz-1.5.5.tar.gz)

- Install `Cython` first

```patch
diff --git a/pyqlz.c b/pyqlz.c
index da0266c..132b8ba 100644
--- a/pyqlz.c
+++ b/pyqlz.c
@@ -308,7 +308,7 @@ static CYTHON_INLINE float __PYX_NAN() {
 #include <math.h>
 #define __PYX_HAVE__pyqlz
 #define __PYX_HAVE_API__pyqlz
-#include "malloc.h"
+#include "stdlib.h"
 #include "wrapQLZ.h"
 #ifdef _OPENMP
 #include <omp.h>
```


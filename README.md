# KHR Binding C++ Generator

## Process

1. Load XML from Khronos repository
2. Generate C++ API binding from XML

## Preconfigured Profiles

Currently available profiles for loading and generating (in subdirectory `profiles`):
 * `gl.json` for the OpenGL API (results are deployed in [glbinding](https://github.com/cginternals/glbinding))
 * `gles.json` for the OpenGL ES API (results are deployed in [glesbinding](https://github.com/cginternals/glesbinding))
 * `glsc.json` for the OpenGL SC API (results are deployed in [glscbinding](https://github.com/cginternals/glscbinding))
 * `egl.json` for the EGL API (results are deployed in [eglbinding](https://github.com/cginternals/eglbinding))

## Examples

### Load XML from Khronos repository

```bash
python3 scripts/update.py -p profiles/gl.json
```

### Generate C++ API binding from XML

```bash
python3 scripts/generate.py -p profiles/gl.json -d glbinding
```

## Dependencies

* Python (either 2.7 or 3)
  * pystache

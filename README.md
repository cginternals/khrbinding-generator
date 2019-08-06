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
python3 scripts/update.py -p "profiles/gl.json"
python3 scripts/update.py -p "profiles/gles.json"
python3 scripts/update.py -p "profiles/glsc.json"
python3 scripts/update.py -p "profiles/egl.json"
python3 scripts/update.py -p "profiles/vk.json"
```

### Generate C++ API binding from XML

```bash
python3 scripts/generate.py -p "profiles/gl.json" -d "../glbinding/source"
python3 scripts/generate.py -p "profiles/gles.json" -d "../glesbinding/source"
python3 scripts/generate.py -p "profiles/glsc.json" -d "../glscbinding/source"
python3 scripts/generate.py -p "profiles/egl.json" -d "../eglbinding/source"
python3 scripts/generate.py -p "profiles/vk.json" -d "../vkbinding/source"
```

## Profile Documentation

A profile file is a JSON file with a flat layout, although semantic groups are intended.
The currently supported tags are:

* API specification
  * `sourceUrl`: The url to download the API specification
  * `sourceFile`: The intermediate file name to store the API specification
  * `patchFile`: A local file for patching the downloaded specification (optional)
  * `apiIdentifier`: For multi-API specification files, specifies the one API to select
* Code Generation
  * `bindingNamespace`: The identifier for the subdirectories and C++ binding namespace
  * `baseNamespace`: The C++ namespace for the generated API
  * `coreProfileSince`: The version of core profile introduction (e.g., 3.2 for OpenGL)
  * `multiContext`: Set to true if the API supports multiple contexts
  * `booleanWidth`: The width of a boolean in this API (may be either 8 or 32)

More options are subject to future development. Ideas and requirements are welcomed.

### Example profile gl.json

```json
{
  "": "API specification",
  "apiIdentifier": "gl",
  "sourceUrl": "https://raw.githubusercontent.com/KhronosGroup/OpenGL-Registry/master/xml/gl.xml",
  "sourceFile": "gl.xml",
  "patchFile": "glpatch.xml",

  "": "Code Generation",
  "bindingNamespace": "glbinding",
  "baseNamespace": "gl",
  "coreProfileSince": "3.2",
  "multiContext": true,
  "booleanWidth": 8
}
```

## Dependencies

* Python (either 2.7 or 3)
  * pystache

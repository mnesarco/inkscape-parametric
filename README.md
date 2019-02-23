# Inkscape Parametric Extension

This extension allows to define variables and set attributes with python expressions.

This is inspired by https://github.com/projectshaped/parametric-svg which is a not maintained parametric svg spec. But this implementation has two differences:

 * All expressions and scripts are plain old python code
 * This is an Inkscape extension and works directly inside inkscape, no external tools are required.

Things works very similar to: https://github.com/parametric-svg/tutorial

## Parametric expressions

Any svg attribute can be made parametric just defining a companion attribute in the parametric namespace.
For example if you want to make rect width parametric you can:

```
<rect ... parametric:width="10 + 20" />
```

The value can be any valid python expression.

## Define variables and functions

You can define your own variables and functions inside the document and use them in expressions.
Your python code must be defined in

```
<parametric:script>
width = 100
height = 2 * width

def myfunct():
  return 100

</parametric:script>
```

then you can use them in your attributes:

```
<rect ... parametric:width="width" parametric:height="height" parametric:y="myfunct()" />
```

See: example.svg

## Direct modification in the parametric script

You can also find objects directly from the script and set attributes:

```
<parametric:script>

r = _svg.findById('rect123')
r.x = 100
r.y = 100
r.width = 100
r.height = 200

</parametric:script>
```

See: example2.svg

## Install

Just copy parametric.py and parametric.inx to your inkscape extensions folder.

After install, restart inkscape and the extension will appear:

Menu / Extensions / Parametric SVG / Run and Update

You can set your parametric expressions and script values using the builtin xml editor: Shift + Ctrl + X

## External code editor

If you are using Linux, you can edit the parametric python code in an external editor called directly from inkscape:

 * Install Scintilla editor: `sudo apt-get install scite`
 * Copy parametric_editor.py and parametric_editor.inx to your inkscape extensions folder.
 * Restart inkscape

The code editor will be integrated:

Menu / Extensions / Parametric SVG / External code editor

Then you can edit the parametric script in the SciTE editor with syntax coloring. After you save and
close the editor, your chages will be propagated to your svg document.


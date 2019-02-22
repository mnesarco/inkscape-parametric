# Inkscape Parametric Extension

This extension allows to define variables and set attributes with python expressions.

## Parametric expressions

Any svg attribute can be made parametric just defining a companion attribute in the parametric namespace.
For example if you want to make rect width parametric you can:

```
<rect ... parametric:width="10 + 20" />
```

The value can be any valid python expression.

## Define variables and functions

You can define your own variables and funtions inside the document and use them in expressions.
Your python code must be defined in

```
<parametric:script>
width = 100
height = 2 * width

def myfunct():
  return 100

</parametric:script>
```

them you can use them in your attributes:

```
<rect ... parametric:width="width" parametric:height="height" parametric:y="myfunct()" />
```

## Install

Just copy parametric.py and parametric.inx in your inkscape extensions folder.



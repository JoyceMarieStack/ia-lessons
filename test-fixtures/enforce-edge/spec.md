# Spec: Loader Flag Wiring

## Behavior

When extend-mode is active, the loader keeps base keys that the project-local
schema does not override.

## Example

```js
if (settings.extendMode) {
  loader.applyBaseKeys(config);
}
```

The flag can also be set with `--extend-mode` on the command line.

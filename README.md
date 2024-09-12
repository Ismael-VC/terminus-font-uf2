# Terminus Font UF2

Convert `terminus.uf2` to `terminus.tal`:

```bash
$ xxd -g 1 -c 16 terminus0.uf2 | cut -d' ' -f2-17 > terminus.tal
```

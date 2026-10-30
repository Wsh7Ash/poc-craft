import pathlib, sys
data = pathlib.Path(sys.argv[1]).read_bytes()
raise SystemExit(0 if b"MAGIC" in data else 1)

python -m cProfile -o output.pstats Snakes.py
gprof2dot.py -f pstats output.pstats | dot -Tpng -o output.png
open output.png

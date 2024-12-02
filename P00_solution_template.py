from Pxx_input import DEMO_INPUT, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT = DEMO_INPUT
else:
    INPUT = PRODUCTION_INPUT



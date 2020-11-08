import sys

import survey
import results

assert __name__ == "__main__"

if len(sys.argv) == 2:
    if sys.argv[1] == 'survey':
        print('Running survey. Go back here to copy results afterwards!')
        survey.main()
        exit()
    elif sys.argv[1] == 'results':
        results.main()
        exit()

print(f'Run {sys.argv[0]} survey or {sys.argv[0]} results')

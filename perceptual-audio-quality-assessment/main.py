import sys

assert __name__ == "__main__"

if len(sys.argv) == 2:
    if sys.argv[1] == 'maingui':
        import maingui
        print(f'Running main GUI. Run "{sys.argv[0]} results" afterwards!')
        maingui.main()
        exit()
    elif sys.argv[1] == 'results':
        import results
        results.main()
        exit()

print(f'Run {sys.argv[0]} maingui or {sys.argv[0]} results')

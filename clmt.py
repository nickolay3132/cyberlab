import argparse


def main():
    parser = argparse.ArgumentParser(description="GUI/CLI приложение")
    parser.add_argument('mode', nargs='?', choices=['cli'], help="Режим запуска: cli или ничего (для GUI)")
    args, _ = parser.parse_known_args()

    if args.mode == 'cli':
        pass
    else:
        pass

if __name__ == "__main__":
    main()
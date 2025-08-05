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

# class Config:
#     def __init__(self, path: str):
#         self.path = path
#
# @bind
# def make_config(path: str) -> Config:
#     return Config(path=path)
#
# # Получаем связанную функцию вручную
# factory = get(Config)
# cfg = factory(path="config.yaml")
#
# print(cfg.path)  # → config.yaml
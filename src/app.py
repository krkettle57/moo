import fire

from moo.cli.handler import MOOCLIHandler


def main() -> None:
    fire.Fire(MOOCLIHandler)


if __name__ == "__main__":
    main()

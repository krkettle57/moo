import fire

from cli.handler import MOOCLIHandler


def main() -> None:
    fire.Fire(MOOCLIHandler)


if __name__ == "__main__":
    main()

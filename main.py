import argparse

from script import run


def parse_args():
    parser = argparse.ArgumentParser(
        description="Script para gerar cenários de testes utilizando a IA da OpenAI"
    )
    parser.add_argument(
        "--input_file",
        "-i",
        type=str,
        help="Caminho do arquivo de input contendo os detalhes da task",
    )
    parser.add_argument(
        "--output_dir",
        "-o",
        type=str,
        default="",
        help="Caminho de destino do diretório",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    run(args)


if __name__ == "__main__":
    main()

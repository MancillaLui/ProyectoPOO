"""Inicia la interfaz o la demostración de consola."""

from argparse import ArgumentParser


def main():
    parser = ArgumentParser(description="Sistema de gestión académica")
    parser.add_argument("--demo", action="store_true", help="Ejecuta la demostración en consola")
    args = parser.parse_args()
    if args.demo:
        from .demo import main as ejecutar
    else:
        from .interfaz.aplicacion import main as ejecutar
    ejecutar()


if __name__ == "__main__":
    main()

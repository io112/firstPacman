import sys
from scenes.field import Field


def main():
    field = Field()
    field.init_field()
    field.draw()
    sys.exit()


if __name__ == '__main__':
    main()

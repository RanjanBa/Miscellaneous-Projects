import matplotlib.image as mpimg
from entitites.grid import Grid


def levelGenerator(path: str) -> list[list[Grid]]:
    level = []

    img = mpimg.imread(path)

    for i in range(0, len(img)-3, 3):
        temp = []
        for j in range(0, len(img[i])-3, 3):
            g = Grid()
            if img[i+1][j][0] == 0:
                g.left = True

            if img[i+1][j+3][0] == 0:
                g.right = True

            if img[i][j+1][0] == 0:
                g.up = True

            if img[i+3][j+1][0] == 0:
                g.down = True
                
            temp.append(g)

        if len(temp) > 0:
            level.insert(0, temp)

    # with open(path) as f:
    #     lines = f.readlines()
        # row_len = len(lines)
        # for i in range(len(lines)):
        #     idx = row_len - i - 1
        #     temp = []
        #     for j in range(len(lines[idx])):
        #         if lines[idx][j] == 'O' or lines[idx][j] == '.':
        #             g = Grid()

        #             if lines[idx][j] == '.':
        #                 g.food = True

        #             # up
        #             if lines[idx-1][j] == '-':
        #                 g.up = True

        #             # left
        #             if lines[idx][j-1] == '|':
        #                 g.left = True

        #             # down
        #             if lines[idx+1][j] == '-':
        #                 g.down = True

        #             # right
        #             if lines[idx][j+1] == '|':
        #                 g.right = True

        #             temp.append(g)

        #     if len(temp) > 0:
        #         level.append(temp)

    return level

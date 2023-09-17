import random


def ShipLogic(round, yourMap, yourHp, enemyHp, p1ShotSeq, p1PrevHit, storage):

    if round == 1:
        storage = [[1 / (10 * 10) for _ in range(10)] for _ in range(10)]

    if round > 1:
        last_shot = p1ShotSeq[-1]
        x, y = last_shot[0] - 1, last_shot[1] - 1

        if p1PrevHit:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= x + dx < 10 and 0 <= y + dy < 10:
                        storage[x + dx][y + dy] *= 1.2
        else:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= x + dx < 10 and 0 <= y + dy < 10:
                        storage[x + dx][y + dy] *= 0.8

    max_pro = max(max(row) for row in storage)
    for i, row in enumerate(storage):
        for j, prob in enumerate(row):
            if prob == max_pro:
                next_shot = [i + 1, j + 1]
                break

    storage[next_shot[0] - 1][next_shot[1] - 1] = 0

    return next_shot, storage

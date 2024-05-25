from operator import itemgetter
import numpy as np
import random

class BeeAlgorithm:
    def __init__(self, func, scouts, elites, bees_to_promo , search_radius, perspective,
                 bees_to_perspective, x, y, area = 'sqaure'):
        self.func = func
        self.x = float(x)
        self.y = float(y)
        self.area = area

        # Инициализация разведчиков
        self.scouts = [[random.uniform(-self.x, self.x),
                        random.uniform(-self.y, self.y),
                        float(0.0)] for _ in range(scouts)]

        for scout in self.scouts:
            scout[2] = self.func(scout[0], scout[1])

        # Инициализация рабочих пчел
        self.n_workers = elites * bees_to_promo + perspective * bees_to_perspective
        self.elite = elites
        self.perspective = perspective
        self.bees_to_promo = bees_to_promo
        self.bees_to_perspective = bees_to_perspective

        max_b = max(self.scouts, key=itemgetter(2))
        self.workers = [[self.x, self.y, max_b[2]] for _ in range(self.n_workers)]

        self.bees = list()
        self.selected = list()
        self.search_radius = search_radius

    def send_scouts(self):
        """Перемещает разведчиков в случайные позиции и пересчитывает значение целевой функции."""
        for scout in self.scouts:
            scout[0] = random.uniform(-self.x, self.x)
            scout[1] = random.uniform(-self.y, self.y)
            scout[2] = self.func(scout[0], scout[1])

    def research_reports(self):
        """Сортирует всех пчел и выбирает лучшие участки."""
        self.bees = self.scouts + self.workers
        self.bees = sorted(self.bees, key=itemgetter(2), reverse=False)
        self.selected = self.bees[:self.elite + self.perspective]

    def get_best(self):
        """Возвращает пчелу с лучшим значением целевой функции."""
        return self.bees[0]

    def send_workers(self, bee_part, sector, radius):
        """Перемещает рабочих пчел в окрестности выбранного участка."""
        for worker in bee_part:
            if self.area == "square":
                worker[0] = random.uniform(sector[0] - radius, sector[0] + radius)
                worker[1] = random.uniform(sector[1] - radius, sector[1] + radius)
            elif self.area == "circle":
                # Генерация случайной точки в круге
                theta = random.uniform(0, 2 * np.pi)
                r = radius * np.sqrt(random.uniform(0, 1))
                worker[0] = sector[0] + r * np.cos(theta)
                worker[1] = sector[1] + r * np.sin(theta)
            worker[2] = self.func(worker[0], worker[1])

    def selected_search(self, param):
        """Отправляет рабочих пчел на выбранные участки с уменьшением радиуса поиска."""
        for i in range(self.e):
            self.send_workers(
                self.workers[i * self.bees_to_promo: i * self.bees_to_promo + self.bees_to_promo],
                self.selected[i],
                self.search_radius * param,
            )

        for i in range(self.perspective):
            self.send_workers(
                self.workers[
                self.elite * self.bees_to_promo + i * self.bees_to_perspective: self.elite * self.bees_to_promo + i * self.bees_to_perspective + self.bees_to_perspective
                ],
                self.selected[self.elite + i],
                self.search_radius * param,
            )

    def run(self, max_iter):
        """
        Запускает алгоритм пчелиного роя на заданное количество итераций.

        Args:
            max_iter (int): Количество итераций.

        Yields:
            tuple: Кортеж, содержащий список всех пчел, список выбранных участков и лучшую пчелу.
        """
        for i in range(max_iter):
            self.send_scouts()
            self.research_reports()
            self.selected_search(1 / (i + 1))
            best_bee = self.get_best()
            yield self.bees, self.selected, best_bee
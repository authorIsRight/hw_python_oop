from typing import List


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
            self, training_type: str,
            duration: float,
            distance: float,
            speed: float,
            calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return str(f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM: int = 1000
    MINUTES: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(
            # type(self).__name__, self.duration, <-ругается на type
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def get_spent_calories(self) -> float:
        spent_calories = ((self.coeff_calorie_1 * self.get_mean_speed()
                           - self.coeff_calorie_2) * self.weight
                          / self.M_IN_KM * self.duration * self.MINUTES)

        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
    coeff_calorie_1 = 0.035
    coeff_calorie_2 = 0.029

    def get_spent_calories(self) -> float:
        spent_calories = ((
            self.coeff_calorie_1 * self.weight
            + (self.get_mean_speed()**2 // self.height)
            * self.coeff_calorie_2 * self.weight)
            * self.duration * self.MINUTES)
        return spent_calories


class Swimming(Training):
    LEN_STEP: float = 1.38
    """Тренировка: плавание."""
    coeff_calorie_1 = 1.1

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed()
                          + self.coeff_calorie_1) * 2 * self.weight)
        return spent_calories


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    tranings = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type not in tranings:
        raise KeyError('foo bar')
    return tranings[workout_type](*data)

# ниже прекод, давайте не трогать :)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

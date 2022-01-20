from dataclasses import dataclass
from typing import ClassVar, Dict, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {"{:.3f}".format(self.duration)} ч.; '
                f'Дистанция: {"{:.3f}".format(self.distance)} км; '
                f'Ср. скорость: {"{:.3f}".format(self.speed)} км/ч; '
                f'Потрачено ккал: {"{:.3f}".format(self.calories)}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MINUTES_IN_HOUR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод работает только в наследниках'
                                  ' класса Training')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_RUN1: ClassVar[int] = 18
    COEFF_CALORIE_RUN2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_RUN1 * self.get_mean_speed()
                - self.COEFF_CALORIE_RUN2) * self.weight / self.M_IN_KM
                * self.duration * self.MINUTES_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    COEFF_CALORIE_WLK1: ClassVar[float] = 0.035
    COEFF_CALORIE_WLK2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_WLK1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CALORIE_WLK2 * self.weight)
                * self.duration * self.MINUTES_IN_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: float
    LEN_STEP: ClassVar[float] = 1.38
    COEFF_CALORIE_SWM1: ClassVar[float] = 1.1
    COEFF_CALORIE_SWM2: ClassVar[int] = 2

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_CALORIE_SWM1)
                * self.COEFF_CALORIE_SWM2 * self.weight)


def read_package(workout_type: str, data: List) -> Training:
    """Прочитать данные, полученные от датчиков."""
    training_dict: Dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in training_dict:
        return training_dict[workout_type](*data)
    else:
        raise ValueError('Переданы некорректные данные')


def main(training: Training) -> None:
    """Основная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: tuple = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

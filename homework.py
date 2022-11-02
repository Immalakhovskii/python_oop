from dataclasses import dataclass
from typing import ClassVar, Dict, List


@dataclass
class InfoMessage:
    """Class for info message on workout."""
    workout_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Workout: {self.workout_type}; '
                f'Duration: {self.duration: .3f} h.; '
                f'Distance: {"{:.3f}".format(self.distance)} km; '
                f'Average speed: {"{:.3f}".format(self.speed)} km/h; '
                f'Kcal spent: {"{:.3f}".format(self.calories)}.')


@dataclass
class Workout:
    """Basic workout class."""
    action: int
    duration: float
    weight: float
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MINUTES_IN_HOUR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Get distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get average speed."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get kcal spent."""
        raise NotImplementedError(
            'Method operates only in Workouts class inheritors'
        )

    def show_workout_info(self) -> InfoMessage:
        """Get info message on finished workout."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Workout):
    """Workout: Running."""
    COEFF_CALORIE_RUN1: ClassVar[int] = 18
    COEFF_CALORIE_RUN2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_RUN1 * self.get_mean_speed()
                - self.COEFF_CALORIE_RUN2) * self.weight / self.M_IN_KM
                * self.duration * self.MINUTES_IN_HOUR)


@dataclass
class SportsWalking(Workout):
    """Workout: Racewalking."""
    height: float
    COEFF_CALORIE_WLK1: ClassVar[float] = 0.035
    COEFF_CALORIE_WLK2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_WLK1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CALORIE_WLK2 * self.weight)
                * self.duration * self.MINUTES_IN_HOUR)


@dataclass
class Swimming(Workout):
    """Workout: Swimming."""
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


def read_package(workout_type: str, data: List) -> Workout:
    """Read data from sensors."""
    workout_dict: Dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in workout_dict:
        return workout_dict[workout_type](*data)
    else:
        raise ValueError('Incorrect data passed')


def main(workout: Workout) -> None:
    """Main function."""
    info: InfoMessage = workout.show_workout_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: tuple = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        workout = read_package(workout_type, data)
        main(workout)

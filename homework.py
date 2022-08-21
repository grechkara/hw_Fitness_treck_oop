
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Предоставляет информацию о тренировке в виде строки."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

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
        training_distance: float
        training_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return training_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float
        coef_cal_1: int = 18
        coef_cal_2: int = 20
        value_1: float = coef_cal_1 * self.get_mean_speed() - coef_cal_2
        value_2: float = self.weight / self.M_IN_KM * (self.duration * 60)
        spent_calories = value_1 * value_2
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: int

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float
        coef_cal_1: float = 0.035
        coef_cal_2: float = 0.029
        value_1: float = coef_cal_1 * self.weight
        value_2: float = coef_cal_2 * self.weight
        value_3: float = self.get_mean_speed()**2 // self.height
        spent_calories = (value_1 + value_3 * value_2) * (self.duration * 60)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: int
    count_pool: int
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed: float
        full_distance = self.length_pool * self.count_pool
        mean_speed = full_distance / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories: float
        coef_cal_1: float = 1.1
        coef_cal_2: float = 2
        value_1 = self.get_mean_speed() + coef_cal_1
        value_2 = coef_cal_2 * self.weight
        spent_calories = value_1 * value_2
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    test_training = type_training[workout_type](*data)
    return test_training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    return print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),  # action, duration (hours), weight
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

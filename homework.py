class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {round(self.duration, 3):.3f} ч.; '
                        f'Дистанция: {round(self.distance, 3):.3f} км; '
                        f'Ср. скорость: {round(self.speed, 3):.3f} км/ч; '
                        f'Потрачено ккал: {round(self.calories, 3):.3f}.'
                        )
        return message


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    HOUR_MIN = 60   # Коэфф для перевода времени в минуты.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance: float = (self.action * self.LEN_STEP / self.M_IN_KM)
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed: float = (self.get_distance() / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(self.__class__.__name__,
                                    self.duration,
                                    self.get_distance(),
                                    self.get_mean_speed(),
                                    self.get_spent_calories()
                                    )
        return training_info


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        coff_calorie_1: float = 18
        coff_calorie_2: float = 20
        run_spent_calories: float = ((coff_calorie_1 * self.get_mean_speed()
                                     - coff_calorie_2) * self.weight
                                     / self.M_IN_KM * self.duration
                                     * self.HOUR_MIN
                                     )
        return run_spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coff_calorie_1: float = 0.035
        coff_calorie_2: float = 0.029
        swl_spent_calories: float = ((coff_calorie_1 * self.weight
                                     + (self.get_mean_speed()**2
                                    // self.height) * coff_calorie_2
                                     * self.weight) * self.duration
                                     * self.HOUR_MIN
                                     )
        return swl_spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        swm_mean_speed: float = (self.length_pool * self.count_pool
                                 / self.M_IN_KM / self.duration
                                 )
        return swm_mean_speed

    def get_spent_calories(self) -> float:
        coff_calorie_1: float = 1.1
        coff_calorie_2: float = 2
        swm_spent_calories: float = ((self.get_mean_speed() + coff_calorie_1)
                                     * coff_calorie_2 * self.weight
                                     )
        return swm_spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    trainings = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in trainings:
        read_training = trainings[workout_type](*data)
    return read_training


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

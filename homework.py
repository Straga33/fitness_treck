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
        message = (f'Тип тренировки: {self.training_type}; '
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
    HOUR_MIN = 60

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

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(training_type=self.__class__.__name__,
                                    duration=self.duration,
                                    distance=self.get_distance(),
                                    speed=self.get_mean_speed(),
                                    calories=self.get_spent_calories()
                                    )
        return training_info


class Running(Training):
    """Тренировка: бег."""

    COEFF_RUN_CAL_1 = 18
    COEFF_RUN_CAL_2 = 20

    def get_spent_calories(self) -> float:

        return ((self.COEFF_RUN_CAL_1 * self.get_mean_speed()
                - self.COEFF_RUN_CAL_2) * self.weight
                / self.M_IN_KM * self.duration * self.HOUR_MIN
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_WLK_CAL_1 = 0.035
    COEFF_WLK_CAL_2 = 0.029

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:

        return ((self.COEFF_WLK_CAL_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_WLK_CAL_2 * self.weight) * self.duration
                * self.HOUR_MIN
                )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    COEFF_SWM_CAL_1 = 1.1
    COEFF_SWM_CAL_2 = 2

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

        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration
                )

    def get_spent_calories(self) -> float:

        return ((self.get_mean_speed() + self.COEFF_SWM_CAL_1)
                * self.COEFF_SWM_CAL_2 * self.weight
                )


TRANINGS = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in TRANINGS:
        raise NotImplementedError(f"тренировка {workout_type} еще"
                                  f"не поддерживается")
    return TRANINGS[workout_type](*data)


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
        try:
            training = read_package(workout_type, data)
            main(training)
        except NotImplementedError as error_workout_type:
            print(type(error_workout_type).__name__ + ':', error_workout_type)

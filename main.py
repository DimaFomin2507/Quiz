import sqlite3
import random


class Quiz:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.questions = self.load_questions()
        self.score = 0

    def load_questions(self):
        # Пример вопросов, можно расширить
        questions = {
            'easy': [
                ("Сколько будет 2+2?", "4"),
                ("Какой цвет у неба?", "синий"),
                ("Столица России?", "Москва")
            ],
            'medium': [
                ("Сколько будет 7*8?", "56"),
                ("Какой химический символ у воды?", "H2O")


            ],
            'hard': [
                ("Сколько будет 12*12?", "144"),
                ("Кто написал 'Война и мир'?", "Толстой")
            ]
        }
        return questions[self.difficulty]

    def ask_question(self):
        question, answer = random.choice(self.questions)
        user_answer = input(f"{question}\nВаш ответ: ")
        if user_answer.lower() == answer.lower():
            self.score += 1
            print("Правильно!")
        else:
            print(f"Неправильно! Правильный ответ: {answer}")

    def start(self):
        print(f"Начинаем викторину на уровне сложности: {self.difficulty}")
        for _ in range(len(self.questions)):
            self.ask_question()
        print(f"Викторина завершена! Ваш счет: {self.score}")


class Leaderboard:
    def __init__(self, db_name='quiz.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    difficulty TEXT NOT NULL
                )
            """)

    def save_result(self, name, score, difficulty):
        with self.conn:
            self.conn.execute("""
                INSERT INTO leaderboard (name, score, difficulty)
                VALUES (?, ?, ?)
            """, (name, score, difficulty))

    def display(self):
        for difficulty in ['easy', 'medium', 'hard']:
            print(f"\nТаблица лидеров ({difficulty}):")
            cursor = self.conn.execute("""
                SELECT name, score FROM leaderboard
                WHERE difficulty = ?
                ORDER BY score DESC
                LIMIT 5
            """, (difficulty,))
            for row in cursor:
                print(f"{row[0]} - {row[1]} очков")


class User:
    def __init__(self, name):
        self.name = name

    def play_quiz(self, difficulty):
        quiz = Quiz(difficulty)
        quiz.start()
        return quiz.score


def main():
    leaderboard = Leaderboard()
    name = input("Введите ваше имя: ")
    user = User(name)

    while True:
        difficulty = input("Выберите уровень сложности (easy, medium, hard): ").lower()
        if difficulty in ['easy', 'medium', 'hard']:
            break
        else:
            print("Неверный уровень сложности. Попробуйте снова.")

    score = user.play_quiz(difficulty)
    leaderboard.save_result(name, score, difficulty)
    leaderboard.display()


if __name__ == "__main__":
    main()
class Cat:
    def __init__(self, name, age, features: list):
        self.name = name
        self.age = age
        self.features = features if features else []

    def __str__(self):
        return f'Name: {self.name}, age: {self.age}, features: [{", ".join(self.features)}]'
    
cat_features = ['білий', 'чорний', 'сірий', 'рудий', 'нахабний', 'чемний', 'ходить в лоток', 'агресивний', 'ловить щурів']
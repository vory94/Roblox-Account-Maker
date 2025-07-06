from random import choice, randint, random, choices
import string
import util as u
config = u.Util.get_config()

def rxl(x):
    chars = string.ascii_letters + string.digits
    return ''.join(choices(chars, k=x))

class RobloxProfile:
    @staticmethod
    def get_username():
        untype = config["userType"]
        if len(untype) == 2 and untype.endswith("l"):
            return rxl(int(untype[0]))
        
        word_parts = [
            "Shadow", "Flame", "Wolf", "Tiger", "Dragon", "Phoenix", "Hunter", "Star", "Ghost",
            "Legend", "Galaxy", "Frost", "Sonic", "Crystal", "Silver", "Dark", "Power", "Magic", "Light",
            "Alpha", "King", "Queen", "Master", "Pro", "Hero", "Knight", "Beast", "Epic", "Ultra",
            "Fire", "Storm", "Blaze", "Ice", "Sky", "Thunder", "Raven", "Fox", "Lion", "Eagle",
            "Night", "Dawn", "Viper", "Blade", "Hawk", "Claw", "Venom", "Echo", "Bane", "Mystic",
            "Cyber", "Nova", "Orbit", "Pixel", "Glitch", "Byte", "Circuit", "Spark", "Neon", "Chase",
            "Rogue", "Stealth", "Fusion", "Prism", "Wraith", "Saber", "Pulse", "Zero", "Fury",
            "Builder", "Ninja", "Gamer", "Lava", "Stream", "Craft", "Miner", "Block", "Code", "Playz",
            "Panda", "Bear", "Slime", "Duck", "Bacon", "Cookie", "Rocket", "Moon", "Starry", "Turbo",
            "Lucky", "Flash", "Arrow", "Ace", "Omega", "Chaos", "Pixelated", "Void", "Rift", "Toxic",
            "Golden", "Blizzard", "Inferno", "Vortex", "Zoom", "Aqua", "Primal", "Chill", "Hyper", "Stormy",
            "Zap", "Flick", "Max", "Jelly", "Turbo", "Rift", "Blast", "Skater", "Dancer", "Builder",
            "Drift", "Hero", "Haze", "Craze", "Giga", "Sparkly", "Pixel", "Echo", "Rider"
        ]

        human_names = [
            "Liam", "Emma", "Noah", "Olivia", "Oliver", "Ava", "Elijah", "Sophia", "Lucas", "Isabella",
            "Mason", "Mia", "Ethan", "Charlotte", "Logan", "Amelia", "Aiden", "Harper", "James", "Evelyn",
            "Jayden", "Abigail", "Henry", "Ella", "Sebastian", "Aria", "Jackson", "Scarlett", "Alexander", "Grace",
            "Mateo", "Chloe", "Michael", "Victoria", "Daniel", "Zoe", "William", "Luna", "Levi", "Hannah",
            "Gabriel", "Addison", "Carter", "Willow", "Wyatt", "Nora", "Isaac", "Layla", "Eli", "Hazel",
            "Samuel", "Ellie", "Jack", "Paisley", "Owen", "Aurora", "Luke", "Brooklyn", "Julian", "Savannah",
            "Jaxon", "Grayson", "Hunter", "Zayden", "Ezra", "Kaylee", "Aubrey", "Riley", "Brooklynn", "Asher"
        ]

        separators = ["", "_", "."]
        part1 = choice(human_names) if random() < 0.4 else choice(word_parts)
        part2 = choice(word_parts)

        while part2.lower() == part1.lower():
            part2 = choice(word_parts)

        birth_year = randint(2002, 2024) if random() < 0.2 else ""
        short_number = str(randint(10, 99)) if random() < 0.1 else ""

        add_third = random() < 0.2
        if add_third:
            part3 = choice(word_parts)
            while part3.lower() in [part1.lower(), part2.lower()]:
                part3 = choice(word_parts)
            parts = [part1, part2, part3]
        else:
            parts = [part1, part2]

        username = "".join(choice(separators).join(parts).split())

        if random() < 0.15:
            username = f"Xx_{username}_xX"
        elif random() < 0.1:
            username = f"Xx{username}xX"

        if birth_year:
            username += str(birth_year)
        if short_number:
            username += short_number
        if random() < 0.05:
            username += "_YT" if random() < 0.5 else "YT"

        username = username.replace("o", "0") if random() < 0.2 else username
        username = username.replace("e", "3") if random() < 0.2 else username

        parts = username.split("_")
        if len(parts) > 1 and random() < 0.3:
            random_index = randint(0, len(parts) - 1)
            parts[random_index] = parts[random_index].upper()
            username = "_".join(parts)

        username = ''.join(filter(lambda x: x.isalnum() or x in ['_'], username))
        if len(username) < 3:
            username += str(randint(10, 99))
        if len(username) > 20:
            username = username[:20]

        return username
    
    @staticmethod
    def get_password() -> str:
        return f"{config['pwdPrefix']}{randint(1000000, 9999999)}"
    
    @staticmethod
    def get_birth_day() -> str:
        days = [str(i).zfill(2) for i in range(1, 29)]
        months = [str(i).zfill(2) for i in range(1, 13)]
        years = [str(x) for x in range(2000, 2007)]
        return f"{choice(years)}-{choice(months)}-{choice(days)}T23:00:00.000Z"
    
    @staticmethod
    def get_gender() -> int:
        return randint(1, 2)

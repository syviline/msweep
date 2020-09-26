import json
from random import randrange
from math import floor


class Game:
    def __init__(self):
        self.games = {}
    
    def game_start(self, ip, size, mines_amount):
        if mines_amount >= floor((size * size) / 2):
            return
        if size > 30:
            return
        self.games[ip] = {}  # This is a dict with all games, in format of:
        # {
        #   ip: {
        #           "field": field,
        #           "openfield": field,
        #           "already_checked": already_checked
        #       }
        # }
        self.games[ip]["field"] = [[" " for _ in range(size)] for _ in range(size)]  # Field we don't show to a player
        self.games[ip]["openfield"] = [["-" for _ in range(size)] for _ in range(size)]  # Field we show to a player

        self.games[ip]["already_checked"] = []  # already checked field by recursion

        self.games[ip]["mines_amount"] = mines_amount
        self.games[ip]["field_size"] = size
        self.games[ip]["state"] = "ok"

        for i in range(mines_amount):  # spawning mines
            while True:
                a = randrange(0, size)
                b = randrange(0, size)
                if self.games[ip]["field"][a][b] == "m":
                    continue
                self.games[ip]["field"][a][b] = "m"
                break
    
    def currently_working_with(self, ip):  # This is to declare IP we are currently working with
        self.ip = ip
    
    def is_valid_coord(self, x, y):  # Checking if the given coords are valid
        size = self.games[self.ip]["field_size"]
        if x >= size or y >= size or x < 0 or y < 0:
            return False
        return True
    
    def recursive_field_opening(self, x, y):  # Opening the field
        already_checked = self.games[self.ip]["already_checked"]  # Already checked fields for recursion not to get in infloop
        field = self.games[self.ip]["field"]  # Field we don't show to player(with mines)
        openfield = self.games[self.ip]["openfield"]  # Field we show to player
        if (x, y) in already_checked:
            return
        already_checked.append((x, y))
        check_array = [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)]  # This is for getting neighbour fields of a given field
        # we are going through them with for loop, and check field[x + i[0], y + i[1]]
        amount = 0  # amount of found mines
        for i in check_array:
            if self.is_valid_coord(x + i[0], y + i[1]):
                if field[x + i[0]][y + i[1]] == "m":  # If given field is a mine, we amount++
                    amount += 1
        if amount == 0:
            openfield[x][y] = " "  # field is checked and no mines were found, then we make it empty
            for i in check_array:
                if self.is_valid_coord(x + i[0], y + i[1]):
                    self.recursive_field_opening(x + i[0], y + i[1])  # if in this field no mines were found, then we check 8 neighbour fields
        else:
            openfield[x][y] = str(amount)  # field is checked and mines were found, we print a number there
    
    def get_field(self, is_json=True):  # Return the field(in json format by default)
        if self.ip not in self.games:
            return "100"
        if is_json:
            return json.dumps(self.games[self.ip]["openfield"])
        return self.games[self.ip]["openfield"]
    
    def check_for_win(self):
        this_game = self.games[self.ip]
        not_empty_fields = 0
        for i in range(self.games[self.ip]["field_size"]):
            for j in range(self.games[self.ip]["field_size"]):
                if self.games[self.ip]["openfield"][i][j] == "-" or self.games[self.ip]["openfield"][i][j] == "F":
                    not_empty_fields += 1
        if not_empty_fields == this_game["mines_amount"]:
            return "won"
        return "continue"
    
    def make_move(self, x, y):  # Makes move(and calls recursive check)
        if self.state() != "ok":
            self.stop()
            return
        if self.games[self.ip]["openfield"][x][y] == "F":
            return
        if self.games[self.ip]["field"][x][y] == "m":
            for i in range(self.games[self.ip]["field_size"]):
                for j in range(self.games[self.ip]["field_size"]):
                    if self.games[self.ip]["field"][i][j] == "m":
                        self.games[self.ip]["openfield"][i][j] = "m"
            self.games[self.ip]["state"] = "fail"
        else:
            self.recursive_field_opening(x, y)
            if self.check_for_win() == "won":
                self.games[self.ip]["state"] = "won"
        return "ok"
    
    def flag(self, x, y):
        field = self.games[self.ip]["openfield"][x]
        if field[y] == "-":
            field[y] = "F"
        else:
            field[y] = "-"
    
    def state(self):
        return self.games[self.ip]["state"]
    
    def stop(self):
        del self.games[self.ip]


# Exit codes:
# 100 - Game is not started from your ip, show "Create a game" form
# fail - You have lost
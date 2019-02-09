from player import Player

def main():
    with open('gamestate.json', 'r') as f:
        read_data = f.read()

    result = Player.betRequest(read_data)


if __name__ == "__main__":
    main()
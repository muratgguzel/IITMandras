from enum import Enum

class Teams(Enum):
    BLUE_TEAM = 1
    RED_TEAM = 2
    GREEN_TEAM = 3

class Player:
    def __init__(self, name):
        self.name = name

class KKRTeamMemberships():
    def __init__(self):
        self.team_memberships = []

    def add_team_memberships(self, player, team):
        self.team_memberships.append((player, team))

class Analysis():
    def __init__(self, team_player_memberships):
        memberships = team_player_memberships.team_memberships
        for members in memberships:
            if members[1] == Teams.RED_TEAM:
                print(f'{members[0].name} is in RED team')

if __name__ == '__main__':
    player1 = Player('Player-1')
    player2 = Player('Player-2')
    player3 = Player('Player-3')

    team_memberships = KKRTeamMemberships()
    team_memberships.add_team_memberships(player1, Teams.BLUE_TEAM)
    team_memberships.add_team_memberships(player2, Teams.RED_TEAM)
    team_memberships.add_team_memberships(player3, Teams.GREEN_TEAM)

    Analysis(team_memberships)


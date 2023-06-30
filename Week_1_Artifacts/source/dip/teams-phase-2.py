from enum import Enum
from abc import ABCMeta, abstractmethod


class Teams(Enum):
    BLUE_TEAM = 1
    RED_TEAM = 2
    GREEN_TEAM = 3


class TeamMembershipLookup():
    @abstractmethod
    def find_all_players_of_team(self, team):
        pass


class Player:
    def __init__(self, name):
        self.name = name


class KKRTeamMemberships(TeamMembershipLookup):
    def __init__(self):
        self.team_memberships = []

    def add_team_memberships(self, player, team):
        self.team_memberships.append((player, team))

    def find_all_players_of_team(self, team):
        for members in self.team_memberships:
            if members[1] == team:
                yield members[0].name

class CSKTeamMemberships(TeamMembershipLookup):
    def __init__(self):
        self.team_memberships = []

    def add_team_memberships(self, player, team):
        self.team_memberships.append((player, team))

    def find_all_players_of_team(self, team):
        for members in self.team_memberships:
            if members[1] == team:
                yield members[0].name

class Analysis():
    def __init__(self, team_membership_lookup):
        for player in team_membership_lookup.find_all_players_of_team(Teams.RED_TEAM):
            print(f'{player} is in RED team.')

if __name__ == '__main__':
    player1 = Player('Player-1')
    player2 = Player('Player-2')
    team_memberships = KKRTeamMemberships()
    team_memberships = CSKTeamMemberships()
    team_memberships.add_team_memberships(player1, Teams.BLUE_TEAM)
    team_memberships.add_team_memberships(player2, Teams.RED_TEAM)

    Analysis(team_memberships)

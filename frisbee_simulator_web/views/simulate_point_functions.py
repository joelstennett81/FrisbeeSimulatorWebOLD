import random


class PlayerInPointSimulation:
    def __init__(self, player):
        super().__init__()
        self.team = None
        self.player = player
        self.onOffense = None
        self.onDefense = None
        self.hasDisc = False
        self.playerGuarding = None
        self.guardingDisc = None
        self.guardingPlayerBeingThrownTo = None


class PointSimulation:
    def __init__(self, gameSimulation):
        super().__init__()
        # simulate by team rating variables:
        self.randomYardsThrown = None
        self.randomReceiver = None
        self.throw_type = None
        self.differenceInTeamsOverallRating = None
        self.determiner = None
        self.probabilityForWinner = None
        self.betterTeam = None
        # everything else
        self.throwStartingProbability = None
        self.gameSimulation = gameSimulation
        self.teamOne = self.gameSimulation.teamOne
        self.teamTwo = self.gameSimulation.teamTwo
        self.sevenOnFieldForTeamOne = None
        self.sevenOnFieldForTeamTwo = None
        self.sevenOnFieldForOffense = None
        self.sevenOnFieldForDefense = None
        self.teamWithDisc = None
        self.pointWinner = None
        self.discLocation = None
        self.pointOver = False
        self.yardsGainedDownField = 0
        self.playerWithDisc = None
        self.playerBeingThrownTo = None
        self.playerGuardingDisc = None
        self.playerGuardingPlayerBeingThrownTo = None
        self.receiverOptions = None
        self.defenderOptions = None
        self.throwChoice = None
        self.probabilityThrowIsCompleted = None
        self.assistThrower = None
        self.goalThrower = None
        self.throwerNumber = None
        self.simulationType = 'player_rating'
        self.oLineOnField = None
        self.dLineOnField = None

    def simulate_point(self):
        self.determine_who_starts_point_with_disc()
        if self.simulationType == 'player_rating':
            print('We are simulating point by player rating')
            self.put_correct_players_on_field()
            self.determine_starting_disc_location_before_pull()
            self.determine_who_catches_pull()
            self.determine_where_pull_is_caught()
            self.simulate_point_by_player_rating()
        else:
            print('we are simulating point by team rating')
            self.calculate_difference_in_teams_overall_rating()
            self.calculate_probability_for_winner()
            self.simulate_point_by_team_rating()

    def determine_who_starts_point_with_disc(self):
        print('determining who starts point with disc')
        if self.teamOne.startPointWithDisc:
            print('Team One starts with Disc')
            self.teamWithDisc = self.teamOne
            self.teamOne.hasDisc = True
        elif self.teamTwo.startPointWithDisc:
            print('team 2 starts with disc')
            self.teamWithDisc = self.teamTwo
            self.teamTwo.hasDisc = True
        else:
            print('neither team starts with disc')

    def put_correct_players_on_field(self):
        print('in putting correct players on field')
        if self.teamOne.startPointWithDisc:
            self.teamOne.sevenOnField = self.teamOne.oLinePlayers
            self.teamTwo.sevenOnField = self.teamTwo.dLinePlayers
            self.sevenOnFieldForOffense = self.teamOne.sevenOnField
            self.sevenOnFieldForDefense = self.teamTwo.sevenOnField
        elif self.teamTwo.startPointWithDisc:
            self.teamOne.sevenOnField = self.teamOne.dLinePlayers
            self.teamTwo.sevenOnField = self.teamTwo.oLinePlayers
            self.sevenOnFieldForOffense = self.teamTwo.sevenOnField
            self.sevenOnFieldForDefense = self.teamOne.sevenOnField
        else:
            print('error with correct players on field')
        print('seven starting on Offense: ', self.sevenOnFieldForOffense)
        print('seven starting on Defense: ', self.sevenOnFieldForDefense)

    def determine_starting_disc_location_before_pull(self):
        print('in determining starting disc location before pull')
        # if team 1 starts game with disc, its at disc location 1
        # if team 2 starts game with disc, its at disc location 2
        # disc will always start at same point, until a break happens
        if self.teamOne.startPointWithDisc:
            self.discLocation = 0
        elif self.teamTwo.startPointWithDisc:
            self.discLocation = 70
        else:
            print('error with starting disc location')

    def determine_who_catches_pull(self):
        print('determine who catches pull')
        self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1],
                                self.sevenOnFieldForOffense[2]]
        self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1],
                                self.sevenOnFieldForDefense[2]]
        self.randomReceiver = random.randint(0, 2)
        self.playerWithDisc = self.receiverOptions[self.randomReceiver]
        print('player with disc catching pull: ', self.playerWithDisc)
        self.playerGuardingDisc = self.defenderOptions[self.randomReceiver]
        self.determine_receiver_options()
        self.determine_defender_options()

    def determine_where_pull_is_caught(self):
        print('determining where pull is caught')
        if self.teamOne.startPointWithDisc:
            random_start = random.randint(-10, 15)
            self.discLocation = random_start
            print('Team one catches disc at: ', self.discLocation)
        elif self.teamTwo.startPointWithDisc:
            random_start = random.randint(55, 80)
            self.discLocation = random_start
            print('Team Two catches disc at: ', self.discLocation)
        else:
            print('error with where pull is caught')
        print('disc starts at: ', self.discLocation)

    def determine_receiver_options(self):
        print('player with disc: ', self.playerWithDisc)
        print('seven on field for offense: ', self.sevenOnFieldForOffense)
        print('throw type: ', self.throw_type)
        self.receiverOptions = []
        if self.playerWithDisc == self.sevenOnFieldForOffense[0]:
            print('first player has disc')
            if self.throw_type == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[1], self.sevenOnFieldForOffense[2]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4]]
            elif self.throw_type == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[5], self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[1]:
            print('second player has disc')
            if self.throw_type == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[2]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[5]]
            elif self.throw_type == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[5], self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[2]:
            if self.throw_type == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[5], self.sevenOnFieldForOffense[6]]
            elif self.throw_type == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[5], self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[3]:
            if self.throw_type == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[5]]
            elif self.throw_type == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[5],
                                        self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[4]:
            if self.throw_type == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[5]]
            elif self.throw_type == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[5],
                                        self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[5]:
            if self.throw_type == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[1], self.sevenOnFieldForOffense[2]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[6]]
            elif self.throw_type == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[6]:
            if self.throw_type == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[5]]
            elif self.throw_type == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[5]]
        else:
            print('something went wrong in determining receiver options')
        print('receiver options: ', self.receiverOptions)

    def determine_defender_options(self):
        if self.playerGuardingDisc == self.sevenOnFieldForDefense[0]:
            if self.throw_type == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[1], self.sevenOnFieldForDefense[2]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4]]
            elif self.throw_type == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[5], self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[1]:
            if self.throw_type == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[2]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[5]]
            elif self.throw_type == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[5], self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[2]:
            if self.throw_type == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[5], self.sevenOnFieldForDefense[6]]
            elif self.throw_type == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[5], self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[3]:
            if self.throw_type == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[5]]
            elif self.throw_type == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[5],
                                        self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[4]:
            if self.throw_type == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[5]]
            elif self.throw_type == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[5],
                                        self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[5]:
            if self.throw_type == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[1], self.sevenOnFieldForDefense[2]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[6]]
            elif self.throw_type == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[6]:
            if self.throw_type == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1]]
            elif self.throw_type == 'under' or self.throw_type == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[5]]
            elif self.throw_type == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[5]]

    def simulate_result_of_throw(self):
        print(str(self.playerWithDisc) + ' tries to throw to: ' + str(self.playerBeingThrownTo) + ' for ' + str(
            self.randomYardsThrown) + 'yards')
        if self.probabilityThrowIsCompleted < self.throwStartingProbability:
            # throw is completed
            if self.teamWithDisc == self.teamOne:
                self.discLocation += self.randomYardsThrown
            else:
                self.discLocation -= self.randomYardsThrown
            if self.teamWithDisc == self.teamOne:
                print('team one completed disc at this location: ', self.discLocation)
                if self.discLocation < -20:
                    # turnover, disc goes to goal line at location 0 and team 2 has disc
                    self.discLocation = 0
                    self.switch_teams_due_to_turnover()
                elif 70 < self.discLocation < 90:
                    self.assistThrower = self.playerWithDisc
                    self.goalThrower = self.playerBeingThrownTo
                    self.pointWinner = self.teamOne
                    self.gameSimulation.teamOneScore += 1
                    self.pointOver = True
                elif self.discLocation > 90:
                    self.discLocation = 70
                    self.switch_teams_due_to_turnover()
                else:
                    self.playerWithDisc = self.playerBeingThrownTo
                    self.playerGuardingDisc = self.playerGuardingPlayerBeingThrownTo
            else:
                print('team two completed disc at this location: ', self.discLocation)
                if self.discLocation > 90:
                    # turnover, disc goes to goal line at location 0 and team 2 has disc
                    self.discLocation = 70
                    self.switch_teams_due_to_turnover()
                elif -20 < self.discLocation < 0:
                    self.assistThrower = self.playerWithDisc
                    self.goalThrower = self.playerBeingThrownTo
                    self.pointWinner = self.teamTwo
                    self.gameSimulation.teamTwoScore += 1
                    self.pointOver = True
                elif self.discLocation < -20:
                    self.discLocation = 0
                    self.switch_teams_due_to_turnover()
                else:
                    self.playerWithDisc = self.playerBeingThrownTo
                    self.playerGuardingDisc = self.playerGuardingPlayerBeingThrownTo
        else:
            print('throw was dropped')
            # throw was either dropped or thrown away
            self.switch_teams_due_to_turnover()

    def simulate_swing_throw(self):
        self.throw_type = 'swing'
        self.determine_receiver_options()
        self.determine_defender_options()
        self.randomReceiver = random.randint(0, len(self.receiverOptions) - 1)
        self.playerBeingThrownTo = self.receiverOptions[self.randomReceiver]
        self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[self.randomReceiver]
        self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                            self.playerWithDisc.swing_throw_offense + self.playerBeingThrownTo.handle_cut_offense
                                            - self.playerGuardingDisc.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.handle_cut_defense)
        self.randomYardsThrown = random.randint(-5, 5)
        self.simulate_result_of_throw()

    def simulate_under_throw(self):
        print('simulating under throw')
        self.throw_type = 'under'
        self.determine_receiver_options()
        self.determine_defender_options()
        self.randomReceiver = random.randint(0, len(self.receiverOptions) - 1)
        self.playerBeingThrownTo = self.receiverOptions[self.randomReceiver]
        self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[self.randomReceiver]
        self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                            self.playerWithDisc.under_throw_offense + self.playerBeingThrownTo.under_cut_offense
                                            - self.playerGuardingDisc.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.under_cut_defense)
        self.randomYardsThrown = random.randint(5, 15)
        self.simulate_result_of_throw()

    def simulate_short_huck_throw(self):
        print('simulating short huck throw')
        self.throw_type = 'short_huck'
        self.determine_receiver_options()
        self.determine_defender_options()
        self.randomReceiver = random.randint(0, len(self.receiverOptions) - 1)
        self.playerBeingThrownTo = self.receiverOptions[self.randomReceiver]
        self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[self.randomReceiver]
        self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                            self.playerWithDisc.short_huck_throw_offense + self.playerBeingThrownTo.short_huck_cut_offense
                                            - self.playerGuardingDisc.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.short_huck_cut_defense)
        self.randomYardsThrown = random.randint(15, 30)
        self.simulate_result_of_throw()

    def simulate_deep_huck_throw(self):
        print('simulating deep huck throw')
        self.throw_type = 'deep_huck'
        self.determine_receiver_options()
        self.determine_defender_options()
        self.randomReceiver = random.randint(0, len(self.receiverOptions) - 1)
        self.playerBeingThrownTo = self.receiverOptions[self.randomReceiver]
        self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[self.randomReceiver]
        self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                            self.playerWithDisc.deep_huck_throw_offense + self.playerBeingThrownTo.deep_huck_cut_offense
                                            - self.playerGuardingDisc.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.deep_huck_cut_defense)
        self.randomYardsThrown = random.randint(30, 70)
        self.simulate_result_of_throw()

    def simulate_point_by_player_rating(self):
        # four pass options:
        # 1: swing for -5 to +5 yards (random number between 0-3
        # 2: under for 5 to 15 yards (random number between 4-6
        # 3: short huck for 15-30 yards (random number between 7-8)
        # 4: deep huck for 31-70 yards (cant go thru end of end zone) (random number == 9-10

        # Probability of Turnover
        while not self.pointOver:
            print('point is not over yet ')
            # determine what throw is going to be thrown
            random_number = random.randint(0, 10)
            if random_number in [0, 1, 2, 3]:
                print('throw choice is swing')
                self.throwChoice = 'swing'
                self.throwStartingProbability = 90
                self.simulate_swing_throw()
            elif random_number in [4, 5, 6]:
                print('throw choice is under')
                self.throwChoice = 'under'
                self.throwStartingProbability = 80
                self.simulate_under_throw()
            elif random_number in [7, 8]:
                print('throw choice is short huck')
                self.throwChoice = 'short_huck'
                self.throwStartingProbability = 65
                self.simulate_short_huck_throw()
            elif random_number in [9, 10]:
                print('throw choice is deep huck')
                self.throwChoice = 'deep_huck'
                self.throwStartingProbability = 55
                self.simulate_deep_huck_throw()
            print('throw has been simulated')

    def simulate_point_by_team_rating(self):
        if self.teamOne.startPointWithDisc:
            print('teamOne has disc to start')
            self.sevenOnFieldForTeamOne = self.teamOne.team.o_line_players
            self.sevenOnFieldForTeamTwo = self.teamTwo.team.d_line_players
            self.sevenOnFieldForOffense = self.teamOne.team.o_line_players
            self.sevenOnFieldForDefense = self.teamTwo.team.d_line_players
            self.discLocation = 0
            if self.betterTeam == self.teamOne:
                # Team 1 has better chance to hold as better team
                self.determiner = random.randint(1, 100)
                if self.determiner <= self.probabilityForWinner:
                    self.pointWinner = self.teamOne
                    self.gameSimulation.teamOneScore += 1
                    print('team 1 held as better team')
                # Team 2 breaks and wins the point as worse team
                else:
                    self.pointWinner = self.teamTwo
                    self.gameSimulation.teamTwoScore += 1
                    print('team 2 broke as worse team')
            elif self.betterTeam == self.teamTwo:
                # Team 1 holds and wins the point as worse team
                if self.determiner <= (100 - self.probabilityForWinner):
                    self.pointWinner = self.teamOne
                    self.gameSimulation.teamOneScore += 1
                    print('team 1 held as worse team ')
                # Team 2 breaks as the better team
                else:
                    self.pointWinner = self.teamTwo
                    self.gameSimulation.teamTwoScore += 1
                    print('team 2 broke as better team')
        else:
            print('team 2 has disc to start')
            self.sevenOnFieldForTeamOne = self.teamOne.team.d_line_players
            self.sevenOnFieldForTeamTwo = self.teamTwo.team.o_line_players
            self.sevenOnFieldForOffense = self.teamTwo.team.o_line_players
            self.sevenOnFieldForDefense = self.teamOne.team.d_line_players
            self.discLocation = 70
            if self.betterTeam == self.teamTwo:
                # Team 2 has better chance to hold as better team
                if self.determiner <= self.probabilityForWinner:
                    self.pointWinner = self.teamTwo
                    self.gameSimulation.teamTwoScore += 1
                    print('team 2 holds as better team')
                # Team 1 breaks and wins the point as worse team
                else:
                    self.pointWinner = self.teamOne
                    self.gameSimulation.teamOneScore += 1
                    print('team 1 breaks as worse team')
            elif self.betterTeam == self.teamOne:
                # Team 2 holds and wins the point as worse team
                if self.determiner <= (100 - self.probabilityForWinner):
                    self.pointWinner = self.teamTwo
                    self.gameSimulation.teamTwoScore += 1
                    print('team 2 holds as worse team')
                # Team 1 breaks as the better team
                else:
                    self.pointWinner = self.teamOne
                    self.gameSimulation.teamOneScore += 1
                    print('team 1 breaks as better team')

    def calculate_difference_in_teams_overall_rating(self):
        if self.teamOne.team.overall_rating > self.teamTwo.team.overall_rating:
            self.betterTeam = self.teamOne
            self.differenceInTeamsOverallRating = self.teamOne.team.overall_rating - self.teamTwo.team.overall_rating
        else:
            self.betterTeam = self.teamTwo
            self.differenceInTeamsOverallRating = self.teamTwo.team.overall_rating - self.teamOne.team.overall_rating

    def calculate_probability_for_winner(self):
        self.probabilityForWinner = self.differenceInTeamsOverallRating + 50

    def switch_teams_due_to_turnover(self):
        print('seven field for offense before switching: ', self.sevenOnFieldForOffense)
        print('seven on field for def before switching: ', self.sevenOnFieldForDefense)
        print('switching team due to turnover')
        print('player with disc before turn: ', self.playerWithDisc)
        print('player guarding disc before turn: ', self.playerGuardingDisc)
        print('player being thrown to before turn: ', self.playerBeingThrownTo)
        print('player guarding receiver before turn: ', self.playerGuardingPlayerBeingThrownTo)
        if self.teamWithDisc == self.teamOne:
            print('team 2 now has disc')
            self.teamWithDisc = self.teamTwo
            self.sevenOnFieldForOffense = self.teamTwo.sevenOnField
            self.sevenOnFieldForDefense = self.teamOne.sevenOnField
            self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
            self.playerGuardingDisc = self.receiverOptions[self.randomReceiver]
        else:
            print('team 1 now has disc')
            self.teamWithDisc = self.teamOne
            self.sevenOnFieldForOffense = self.teamOne.sevenOnField
            self.sevenOnFieldForDefense = self.teamTwo.sevenOnField
            self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
            self.playerGuardingDisc = self.receiverOptions[self.randomReceiver]
        print('player with disc after turn: ', self.playerWithDisc)
        print('player guarding disc after turn: ', self.playerGuardingDisc)
        print('seven on field for offense after turn: ', self.sevenOnFieldForOffense)
        print('seven on field for defense after turn: ', self.sevenOnFieldForDefense)

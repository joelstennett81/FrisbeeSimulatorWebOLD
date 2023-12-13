import random


class PlayerInPointSimulation:
    def __init__(self, team, game, player):
        super().__init__()
        self.team = team
        self.game = game
        self.player = player
        self.onOffense = None
        self.onDefense = None
        self.hasDisc = False
        self.playerGuarding = None
        self.guardingDisc = None
        self.guardingPlayerBeingThrownTo = None
        self.gameStats = PlayerGameStatsInGameSimulation(game=self.game, player=self.player)


class PlayerGameStatsInGameSimulation:
    def __init__(self, game, player):
        super().__init__()
        self.game = game
        self.player = player
        self.goals = 0
        self.assists = 0
        self.swingPassesThrown = 0
        self.swingPassesCompleted = 0
        self.underPassesThrown = 0
        self.underPassesCompleted = 0
        self.shortHucksThrown = 0
        self.shortHucksCompleted = 0
        self.deepHucksThrown = 0
        self.deepHucksCompleted = 0
        self.throwingYards = 0
        self.receivingYards = 0
        self.turnoversForced = 0
        self.throwaways = 0
        self.drops = 0
        self.callahans = 0
        self.pulls = 0


class PlayerTournamentStatsInGameSimulation:
    def __init__(self, tournament, player):
        super().__init__()
        self.tournament = tournament
        self.player = player
        self.goals = 0
        self.assists = 0
        self.swingPassesThrown = 0
        self.swingPassesCompleted = 0
        self.underPassesThrown = 0
        self.underPassesCompleted = 0
        self.shortHucksThrown = 0
        self.shortHucksCompleted = 0
        self.deepHucksThrown = 0
        self.deepHucksCompleted = 0
        self.throwingYards = 0
        self.receivingYards = 0
        self.turnoversForced = 0
        self.throwaways = 0
        self.drops = 0
        self.callahans = 0
        self.pulls = 0


class PointSimulation:
    def __init__(self, gameSimulation):
        super().__init__()
        # simulate by team rating variables:
        self.randomYardsThrown = None
        self.randomReceiver = None
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
        self.teamOnOffenseCurrently = None
        self.teamOnDefenseCurrently = None
        self.pointWinner = None
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
        self.goalScorer = None
        self.throwerNumber = None
        self.simulationType = 'player_rating'
        self.oLineOnField = None
        self.dLineOnField = None
        self.discPrePullLocation = None
        self.discCurrentLocation = None
        self.discPostGoalLocation = None
        self.playDirection = None  # Positive means going from 0-> 70, Negative means going from 0<-70
        self.teamWithDiscToStartGame = None

    def flip_play_direction(self):
        if self.playDirection == 1:
            newPlayDirection = -1
        else:
            newPlayDirection = 1
        self.gameSimulation.playDirection = newPlayDirection
        self.playDirection = newPlayDirection

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
            self.teamOnOffenseCurrently = self.teamOne
            self.teamOnDefenseCurrently = self.teamTwo
            self.teamOne.hasDisc = True
        elif self.teamTwo.startPointWithDisc:
            print('team 2 starts with disc')
            self.teamOnOffenseCurrently = self.teamTwo
            self.teamOnDefenseCurrently = self.teamOne
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

    def determine_starting_disc_location_before_pull(self):
        print('in determining starting disc location before pull')
        # team catches in endzone at 0, then disc starts at 0, and is pulled to 70
        if self.discPostGoalLocation == 0:
            self.discCurrentLocation = 0
            self.discPrePullLocation = 0
        # team catches in endzone at 70, disc starts at 70, and is pulled to 0
        else:
            self.discCurrentLocation = 70
            self.discPrePullLocation = 70

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
        if self.discPrePullLocation == 70:
            random_start = random.randint(-10, 15)
        else:
            random_start = random.randint(55, 80)
        self.discCurrentLocation = random_start
        print('disc starts at: ', self.discCurrentLocation)

    def determine_receiver_options(self):
        print('player with disc: ', self.playerWithDisc)
        print('throw type: ', self.throwChoice)
        self.receiverOptions = []
        if self.playerWithDisc == self.sevenOnFieldForOffense[0]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[1], self.sevenOnFieldForOffense[2]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[5], self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[1]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[2]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[5]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[5], self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[2]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[5], self.sevenOnFieldForOffense[6]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[5], self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[3]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[5]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[5],
                                        self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[4]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[5]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[5],
                                        self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[5]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[1], self.sevenOnFieldForOffense[2]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[6]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[6]]
        elif self.playerWithDisc == self.sevenOnFieldForOffense[6]:
            if self.throwChoice == 'swing':
                self.receiverOptions = [self.sevenOnFieldForOffense[0], self.sevenOnFieldForOffense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[4], self.sevenOnFieldForOffense[5]]
            elif self.throwChoice == 'deep_huck':
                self.receiverOptions = [self.sevenOnFieldForOffense[3], self.sevenOnFieldForOffense[4],
                                        self.sevenOnFieldForOffense[5]]
        else:
            print('something went wrong in determining receiver options')

    def determine_defender_options(self):
        if self.playerGuardingDisc == self.sevenOnFieldForDefense[0]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[1], self.sevenOnFieldForDefense[2]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[5], self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[1]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[2]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[5]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[5], self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[2]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[5], self.sevenOnFieldForDefense[6]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[5], self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[3]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[5]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[5],
                                        self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[4]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[5]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[5],
                                        self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[5]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[1], self.sevenOnFieldForDefense[2]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[6]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[6]]
        elif self.playerGuardingDisc == self.sevenOnFieldForDefense[6]:
            if self.throwChoice == 'swing':
                self.defenderOptions = [self.sevenOnFieldForDefense[0], self.sevenOnFieldForDefense[1]]
            elif self.throwChoice == 'under' or self.throwChoice == 'short_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[4], self.sevenOnFieldForDefense[5]]
            elif self.throwChoice == 'deep_huck':
                self.defenderOptions = [self.sevenOnFieldForDefense[3], self.sevenOnFieldForDefense[4],
                                        self.sevenOnFieldForDefense[5]]

    def simulate_swing_throw(self):
        self.throwChoice = 'swing'
        self.determine_receiver_options()
        self.determine_defender_options()
        self.randomReceiver = random.randint(0, len(self.receiverOptions) - 1)
        self.playerBeingThrownTo = self.receiverOptions[self.randomReceiver]
        self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[self.randomReceiver]
        self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                            self.playerWithDisc.player.swing_throw_offense + self.playerBeingThrownTo.player.handle_cut_offense
                                            - self.playerGuardingDisc.player.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.player.handle_cut_defense)
        self.randomYardsThrown = random.randint(-5, 5)
        self.simulate_result_of_throw()

    def simulate_under_throw(self):
        self.throwChoice = 'under'
        self.determine_receiver_options()
        self.determine_defender_options()
        self.randomReceiver = random.randint(0, len(self.receiverOptions) - 1)
        self.playerBeingThrownTo = self.receiverOptions[self.randomReceiver]
        self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[self.randomReceiver]
        self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                            self.playerWithDisc.player.under_throw_offense + self.playerBeingThrownTo.player.under_cut_offense
                                            - self.playerGuardingDisc.player.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.player.under_cut_defense)
        self.randomYardsThrown = random.randint(5, 15)
        self.simulate_result_of_throw()

    def simulate_short_huck_throw(self):
        self.throwChoice = 'short_huck'
        self.determine_receiver_options()
        self.determine_defender_options()
        self.randomReceiver = random.randint(0, len(self.receiverOptions) - 1)
        self.playerBeingThrownTo = self.receiverOptions[self.randomReceiver]
        self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[self.randomReceiver]
        self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                            self.playerWithDisc.player.short_huck_throw_offense + self.playerBeingThrownTo.player.short_huck_cut_offense
                                            - self.playerGuardingDisc.player.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.player.short_huck_cut_defense)
        self.randomYardsThrown = random.randint(15, 30)
        self.simulate_result_of_throw()

    def simulate_deep_huck_throw(self):
        self.throwChoice = 'deep_huck'
        self.determine_receiver_options()
        self.determine_defender_options()
        self.randomReceiver = random.randint(0, len(self.receiverOptions) - 1)
        self.playerBeingThrownTo = self.receiverOptions[self.randomReceiver]
        self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[self.randomReceiver]
        self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                            self.playerWithDisc.player.deep_huck_throw_offense + self.playerBeingThrownTo.player.deep_huck_cut_offense
                                            - self.playerGuardingDisc.player.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.player.deep_huck_cut_defense)
        self.randomYardsThrown = random.randint(30, 70)
        self.simulate_result_of_throw()

    def simulate_result_of_throw(self):
        print(str(self.playerWithDisc) + ' tries to throw to: ' + str(self.playerBeingThrownTo) + ' for ' + str(
            self.randomYardsThrown) + 'yards')
        self.playDirection = self.gameSimulation.playDirection
        if self.probabilityThrowIsCompleted < self.throwStartingProbability:
            # play direction is either positive or negative
            self.discCurrentLocation += self.randomYardsThrown * self.playDirection
            print('team ' + str(self.teamOnOffenseCurrently) + ' completed ' + str(
                self.throwChoice) + ' at this location: ' + str(
                self.discCurrentLocation))
            if self.discCurrentLocation < -20:
                # turnover, disc goes to goal line at location 0 and team 2 has disc
                self.discCurrentLocation = 0
                self.assign_completions(isCompletion=False)
                self.assign_turnovers_forced()
                self.switch_teams_due_to_turnover()
            elif (self.playDirection == 1) and (70 < self.discCurrentLocation < 90):
                self.assistThrower = self.playerWithDisc
                self.goalScorer = self.playerBeingThrownTo
                self.pointWinner = self.teamOnOffenseCurrently
                self.teamOnOffenseCurrently.score += 1
                self.discPostGoalLocation = 70
                self.assign_completions(isCompletion=True)
                self.assign_completion_yardage()
                self.assign_goals_and_assists()
                print('Team ' + str(self.teamOnOffenseCurrently) + 'Scored! ' + str(
                    self.assistThrower) + ' threw the assist to ' + str(self.goalScorer))
                self.pointOver = True
            elif (self.playDirection == -1) and (-20 < self.discCurrentLocation < 0):
                self.assistThrower = self.playerWithDisc
                self.goalScorer = self.playerBeingThrownTo
                self.pointWinner = self.teamOnOffenseCurrently
                self.teamOnOffenseCurrently.score += 1
                self.discPostGoalLocation = 0
                self.assign_completion_yardage()
                self.assign_goals_and_assists()
                self.assign_completions(isCompletion=True)
                print('Team ' + str(self.teamOnOffenseCurrently) + 'Scored! ' + str(
                    self.assistThrower) + ' threw the assist to ' + str(self.goalScorer))
                self.pointOver = True
            elif self.discCurrentLocation > 90:
                self.playerWithDisc.gameStats.throwaways += 1
                self.discCurrentLocation = 70
                self.assign_completions(isCompletion=False)
                self.switch_teams_due_to_turnover()
            else:
                self.playerWithDisc.gameStats.throwingYards += self.randomYardsThrown
                self.playerBeingThrownTo.gameStats.receivingYards += self.randomYardsThrown
                self.playerWithDisc = self.playerBeingThrownTo
                self.playerGuardingDisc = self.playerGuardingPlayerBeingThrownTo
            print('team two completed ' + str(self.throwChoice) + ' at this location: ' + str(self.discCurrentLocation))
        else:
            print('throw was dropped')
            # Disc still moves, even if it is dropped, have to handle if disc lands in middle of end zone
            # or way out of bounds
            if self.discCurrentLocation < -20:
                # turnover, disc goes to goal line at location 0 and team 2 has disc
                self.discCurrentLocation = 0
            elif -20 < self.discCurrentLocation < 0:
                self.discCurrentLocation = 0
            elif 70 < self.discCurrentLocation < 90:
                self.discCurrentLocation = 70
            elif self.discCurrentLocation > 90:
                self.discCurrentLocation = 70
            else:
                self.discCurrentLocation += self.randomYardsThrown * self.playDirection
            # throw was either dropped or thrown away
            self.assign_drops()
            self.switch_teams_due_to_turnover()

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
                self.throwChoice = 'swing'
                self.throwStartingProbability = 90
                self.simulate_swing_throw()
            elif random_number in [4, 5, 6]:
                self.throwChoice = 'under'
                self.throwStartingProbability = 80
                self.simulate_under_throw()
            elif random_number in [7, 8]:
                self.throwChoice = 'short_huck'
                self.throwStartingProbability = 65
                self.simulate_short_huck_throw()
            elif random_number in [9, 10]:
                self.throwChoice = 'deep_huck'
                self.throwStartingProbability = 55
                self.simulate_deep_huck_throw()

    def switch_teams_due_to_turnover(self):
        if self.teamOnOffenseCurrently == self.teamOne:
            print('team 2 now has disc')
            self.teamOnOffenseCurrently = self.teamTwo
            self.teamOnDefenseCurrently = self.teamOne
            self.sevenOnFieldForOffense = self.teamTwo.sevenOnField
            self.sevenOnFieldForDefense = self.teamOne.sevenOnField
            self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
            self.playerGuardingDisc = self.receiverOptions[self.randomReceiver]
        else:
            print('team 1 now has disc')
            self.teamOnOffenseCurrently = self.teamOne
            self.teamOnDefenseCurrently = self.teamTwo
            self.sevenOnFieldForOffense = self.teamOne.sevenOnField
            self.sevenOnFieldForDefense = self.teamTwo.sevenOnField
            self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
            self.playerGuardingDisc = self.receiverOptions[self.randomReceiver]
        self.flip_play_direction()

    def assign_completions(self, isCompletion):
        if self.throwChoice == 'swing':
            self.playerWithDisc.gameStats.swingPassesThrown += 1
            if isCompletion:
                self.playerWithDisc.gameStats.swingPassesCompleted += 1
        elif self.throwChoice == 'under':
            self.playerWithDisc.gameStats.underPassesThrown += 1
            if isCompletion:
                self.playerWithDisc.gameStats.underPassesCompleted += 1
        elif self.throwChoice == 'short_huck':
            self.playerWithDisc.gameStats.shortHucksThrown += 1
            if isCompletion:
                self.playerWithDisc.gameStats.shortHucksCompleted += 1
        elif self.throwChoice == 'deep_huck':
            self.playerWithDisc.gameStats.deepHucksThrown += 1
            if isCompletion:
                self.playerWithDisc.gameStats.deepHucksCompleted += 1

    def assign_drops(self):
        self.playerBeingThrownTo.gameStats.drops += 1

    def assign_completion_yardage(self):
        self.playerWithDisc.gameStats.throwingYards += self.randomYardsThrown
        self.playerBeingThrownTo.gameStats.receivingYards += self.randomYardsThrown

    def assign_goals_and_assists(self):
        self.playerWithDisc.gameStats.assists += 1
        self.playerBeingThrownTo.gameStats.goals += 1

    def assign_turnovers_forced(self):
        if self.throwChoice == 'swing':
            if (self.playerGuardingDisc.player.handle_mark_defense - self.playerWithDisc.player.swing_throw_offense) > (
                    self.playerGuardingPlayerBeingThrownTo.player.handle_cut_defense - self.playerBeingThrownTo.player.handle_cut_offense):
                # Give the D to the mark, because they have a better rating difference than the downfield defender
                self.playerGuardingDisc.gameStats.turnoversForced += 1
            else:
                self.playerGuardingPlayerBeingThrownTo.gameStats.turnoversForced += 1
        elif self.throwChoice == 'under':
            if (self.playerGuardingDisc.player.handle_mark_defense - self.playerWithDisc.player.under_throw_offense) > (
                    self.playerGuardingPlayerBeingThrownTo.player.under_cut_defense - self.playerBeingThrownTo.player.under_cut_offense):
                # Give the D to the mark, because they have a better rating difference than the downfield defender
                self.playerGuardingDisc.gameStats.turnoversForced += 1
            else:
                self.playerGuardingPlayerBeingThrownTo.gameStats.turnoversForced += 1
        elif self.throwChoice == 'short_huck':
            if (self.playerGuardingDisc.player.handle_mark_defense - self.playerWithDisc.player.short_huck_throw_offense) > (
                    self.playerGuardingPlayerBeingThrownTo.player.short_huck_cut_defense - self.playerBeingThrownTo.player.short_huck_cut_offense):
                # Give the D to the mark, because they have a better rating difference than the downfield defender
                self.playerGuardingDisc.gameStats.turnoversForced += 1
            else:
                self.playerGuardingPlayerBeingThrownTo.gameStats.turnoversForced += 1
        elif self.throwChoice == 'deep_huck':
            if (self.playerGuardingDisc.player.handle_mark_defense - self.playerWithDisc.player.deep_huck_throw_offense) > (
                    self.playerGuardingPlayerBeingThrownTo.player.deep_huck_cut_defense - self.playerBeingThrownTo.player.deep_huck_cut_offense):
                # Give the D to the mark, because they have a better rating difference than the downfield defender
                self.playerGuardingDisc.gameStats.turnoversForced += 1
            else:
                self.playerGuardingPlayerBeingThrownTo.gameStats.turnoversForced += 1

    def simulate_point_by_team_rating(self):
        if self.teamOne.startPointWithDisc:
            print('teamOne has disc to start')
            self.sevenOnFieldForTeamOne = self.teamOne.team.o_line_players
            self.sevenOnFieldForTeamTwo = self.teamTwo.team.d_line_players
            self.sevenOnFieldForOffense = self.teamOne.team.o_line_players
            self.sevenOnFieldForDefense = self.teamTwo.team.d_line_players
            self.discCurrentLocation = 0
            if self.betterTeam == self.teamOne:
                # Team 1 has better chance to hold as better team
                self.determiner = random.randint(1, 100)
                if self.determiner <= self.probabilityForWinner:
                    self.pointWinner = self.teamOne
                    self.gameSimulation.teamOne.score += 1
                    print('team 1 held as better team')
                # Team 2 breaks and wins the point as worse team
                else:
                    self.pointWinner = self.teamTwo
                    self.gameSimulation.teamTwo.score += 1
                    print('team 2 broke as worse team')
            elif self.betterTeam == self.teamTwo:
                # Team 1 holds and wins the point as worse team
                if self.determiner <= (100 - self.probabilityForWinner):
                    self.pointWinner = self.teamOne
                    self.gameSimulation.teamOne.score += 1
                    print('team 1 held as worse team ')
                # Team 2 breaks as the better team
                else:
                    self.pointWinner = self.teamTwo
                    self.gameSimulation.teamTwo.score += 1
                    print('team 2 broke as better team')
        else:
            print('team 2 has disc to start')
            self.sevenOnFieldForTeamOne = self.teamOne.team.d_line_players
            self.sevenOnFieldForTeamTwo = self.teamTwo.team.o_line_players
            self.sevenOnFieldForOffense = self.teamTwo.team.o_line_players
            self.sevenOnFieldForDefense = self.teamOne.team.d_line_players
            self.discCurrentLocation = 70
            if self.betterTeam == self.teamTwo:
                # Team 2 has better chance to hold as better team
                if self.determiner <= self.probabilityForWinner:
                    self.pointWinner = self.teamTwo
                    self.gameSimulation.teamTwo.score += 1
                    print('team 2 holds as better team')
                # Team 1 breaks and wins the point as worse team
                else:
                    self.pointWinner = self.teamOne
                    self.gameSimulation.teamOne.score += 1
                    print('team 1 breaks as worse team')
            elif self.betterTeam == self.teamOne:
                # Team 2 holds and wins the point as worse team
                if self.determiner <= (100 - self.probabilityForWinner):
                    self.pointWinner = self.teamTwo
                    self.gameSimulation.teamTwo.score += 1
                    print('team 2 holds as worse team')
                # Team 1 breaks as the better team
                else:
                    self.pointWinner = self.teamOne
                    self.gameSimulation.teamOne.score += 1
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

import random


class PointSimulation:
    def __init__(self, gameSimulation):
        super().__init__()
        self.gameSimulation = gameSimulation
        self.teamOne = self.gameSimulation.teamOne
        self.teamTwo = self.gameSimulation.teamTwo
        self.sevenOnFieldForTeamOne = None
        self.sevenOnFieldForTeamTwo = None
        self.teamWithDisc = None
        self.startsPointWithDisc = None
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
        self.swingReceiverOptionOne = None
        self.swingReceiverOptionTwo = None
        self.underReceiverOptionOne = None
        self.underReceiverOptionTwo = None
        self.shortHuckReceiverOptionOne = None
        self.shortHuckReceiverOptionTwo = None
        self.deepHuckReceiverOptionOne = None
        self.deepHuckReceiverOptionTwo = None
        self.deepHuckReceiverOptionThree = None
        self.deepHuckReceiverOptionFour = None

    def determine_who_starts_point_with_disc(self):
        if self.teamOne.startPointWithDisc:
            self.teamWithDisc = self.teamOne
            self.startsPointWithDisc = self.teamTwo
        elif self.teamTwo.startPointWithDisc:
            self.teamWithDisc = self.teamTwo
            self.startsPointWithDisc = self.teamTwo

    def simulate_point(self):
        self.put_correct_players_on_field()
        self.determine_starting_disc_location_before_pull()
        self.determine_who_catches_pull()
        self.determine_where_pull_is_caught()

    def put_correct_players_on_field(self):
        if self.teamOne.startPointWithDisc:
            self.sevenOnFieldForTeamOne = self.teamOne.team.o_line_players
            self.sevenOnFieldForTeamTwo = self.teamTwo.team.d_line_players
        elif self.teamTwo.startPointWithDisc:
            self.sevenOnFieldForTeamOne = self.teamOne.team.d_line_players
            self.sevenOnFieldForTeamTwo = self.teamTwo.team.o_line_players

    def determine_starting_disc_location_before_pull(self):
        # if team 1 starts game with disc, its at disc location 1
        # if team 2 starts game with disc, its at disc location 2
        # disc will always start at same point, until a break happens
        if self.teamOne.startPointWithDisc:
            self.discLocation = 0
        elif self.teamTwo.startPointWithDisc:
            self.discLocation = 70

    def determine_who_catches_pull(self):
        if self.startsPointWithDisc == self.teamOne:
            self.receiverOptions = [self.sevenOnFieldForTeamOne.all()[0], self.sevenOnFieldForTeamOne.all()[1],
                                    self.sevenOnFieldForTeamOne.all()[2]]
        else:
            self.receiverOptions = [self.sevenOnFieldForTeamTwo.all()[0], self.sevenOnFieldForTeamTwo.all()[1],
                                    self.sevenOnFieldForTeamTwo.all()[2]]
        self.throwerNumber = random.randint(1, 3)
        self.playerWithDisc = self.receiverOptions[self.throwerNumber]

    def determine_where_pull_is_caught(self):
        if self.startsPointWithDisc == self.teamOne:
            random_start = random.randint(-10, 15)
            self.discLocation = random_start
        elif self.startsPointWithDisc == self.teamTwo:
            random_start = random.randint(80, 55)
            self.discLocation = random_start

    def determine_receiver_options(self):
        if self.throwerNumber == 0:
            self.swingReceiverOptionOne = 1
            self.swingReceiverOptionTwo = 2
            self.underReceiverOptionOne = 3
            self.underReceiverOptionTwo = 4
            self.shortHuckReceiverOptionOne = 3
            self.shortHuckReceiverOptionTwo = 4
            self.deepHuckReceiverOptionOne = 3
            self.deepHuckReceiverOptionTwo = 4
            self.deepHuckReceiverOptionThree = 5
            self.deepHuckReceiverOptionFour = 6
        elif self.throwerNumber == 1:
            self.swingReceiverOptionOne = 0
            self.swingReceiverOptionTwo = 2
            self.underReceiverOptionOne = 4
            self.underReceiverOptionTwo = 5
            self.shortHuckReceiverOptionOne = 4
            self.shortHuckReceiverOptionTwo = 5
            self.deepHuckReceiverOptionOne = 3
            self.deepHuckReceiverOptionTwo = 4
            self.deepHuckReceiverOptionThree = 5
            self.deepHuckReceiverOptionFour = 6
        elif self.throwerNumber == 2:
            self.swingReceiverOptionOne = 0
            self.swingReceiverOptionTwo = 1
            self.underReceiverOptionOne = 5
            self.underReceiverOptionTwo = 6
            self.shortHuckReceiverOptionOne = 5
            self.shortHuckReceiverOptionTwo = 6
            self.deepHuckReceiverOptionOne = 3
            self.deepHuckReceiverOptionTwo = 4
            self.deepHuckReceiverOptionThree = 5
            self.deepHuckReceiverOptionFour = 6
        elif self.throwerNumber == 3:
            self.swingReceiverOptionOne = 0
            self.swingReceiverOptionTwo = 1
            self.underReceiverOptionOne = 4
            self.underReceiverOptionTwo = 5
            self.shortHuckReceiverOptionOne = 4
            self.shortHuckReceiverOptionTwo = 5
            self.deepHuckReceiverOptionOne = 2
            self.deepHuckReceiverOptionTwo = 4
            self.deepHuckReceiverOptionThree = 5
            self.deepHuckReceiverOptionFour = 6
        elif self.throwerNumber == 4:
            self.swingReceiverOptionOne = 1
            self.swingReceiverOptionTwo = 2
            self.underReceiverOptionOne = 3
            self.underReceiverOptionTwo = 5
            self.shortHuckReceiverOptionOne = 3
            self.shortHuckReceiverOptionTwo = 5
            self.deepHuckReceiverOptionOne = 3
            self.deepHuckReceiverOptionTwo = 2
            self.deepHuckReceiverOptionThree = 5
            self.deepHuckReceiverOptionFour = 6
        elif self.throwerNumber == 5:
            self.swingReceiverOptionOne = 1
            self.swingReceiverOptionTwo = 2
            self.underReceiverOptionOne = 4
            self.underReceiverOptionTwo = 6
            self.shortHuckReceiverOptionOne = 4
            self.shortHuckReceiverOptionTwo = 6
            self.deepHuckReceiverOptionOne = 3
            self.deepHuckReceiverOptionTwo = 4
            self.deepHuckReceiverOptionThree = 0
            self.deepHuckReceiverOptionFour = 6
        elif self.throwerNumber == 6:
            self.swingReceiverOptionOne = 1
            self.swingReceiverOptionTwo = 2
            self.underReceiverOptionOne = 4
            self.underReceiverOptionTwo = 5
            self.shortHuckReceiverOptionOne = 4
            self.shortHuckReceiverOptionTwo = 5
            self.deepHuckReceiverOptionOne = 3
            self.deepHuckReceiverOptionTwo = 4
            self.deepHuckReceiverOptionThree = 5
            self.deepHuckReceiverOptionFour = 0

    def simulate_throw(self, throwStartingProbability):
        self.playerWithDisc == self.sevenOnFieldForTeamOne.all()[self.throwerNumber]
        self.playerGuardingDisc = self.sevenOnFieldForTeamTwo.all()[self.throwerNumber]
        if self.throwChoice == 'swing':
            self.receiverOptions = [self.sevenOnFieldForTeamOne.all()[self.swingReceiverOptionOne],
                                    self.sevenOnFieldForTeamOne.all()[self.swingReceiverOptionTwo]]
            self.defenderOptions = [self.sevenOnFieldForTeamTwo.all()[self.swingReceiverOptionOne],
                                    self.sevenOnFieldForTeamTwo.all()[self.swingReceiverOptionTwo]]
            randomReceiver = random.randint(0, 1)
            self.playerBeingThrownTo = self.receiverOptions[randomReceiver]
            self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[randomReceiver]
            self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                                self.playerWithDisc.under_throw_offense + self.playerBeingThrownTo.under_cut_offense
                                                - self.playerGuardingDisc.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.under_cut_defense)
            if self.probabilityThrowIsCompleted < throwStartingProbability:
                randomYardsThrownOption = range(5, 15)
                randomChoice = random.randint(1, len(randomYardsThrownOption))
                self.discLocation += randomYardsThrownOption[randomChoice]
                if self.discLocation < -20:
                    # turnover, disc goes to goal line at location 0 and team 2 has disc
                    self.teamWithDisc = self.teamTwo
                    self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
                    self.playerGuardingDisc = self.defenderOptions[randomReceiver]
                elif 70 < self.discLocation < 90:
                    self.assistThrower = self.playerWithDisc
                    self.goalThrower = self.playerBeingThrownTo
                    self.pointWinner = self.teamOne
                    self.pointOver = True
                else:
                    self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
                    self.playerGuardingDisc = self.playerGuardingPlayerBeingThrownTo
            else:
                self.teamWithDisc = self.teamTwo
                self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
                self.playerGuardingDisc = self.defenderOptions[randomReceiver]
        elif self.throwChoice == 'under':
            self.receiverOptions = [self.sevenOnFieldForTeamOne.all()[self.underReceiverOptionOne],
                                    self.sevenOnFieldForTeamOne.all()[self.underReceiverOptionTwo]]
            self.defenderOptions = [self.sevenOnFieldForTeamTwo.all()[self.underReceiverOptionOne],
                                    self.sevenOnFieldForTeamTwo.all()[self.underReceiverOptionTwo]]
            randomReceiver = random.randint(0, 1)
            self.playerBeingThrownTo = self.receiverOptions[randomReceiver]
            self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[randomReceiver]
            self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                                self.playerWithDisc.under_throw_offense + self.playerBeingThrownTo.under_cut_offense
                                                - self.playerGuardingDisc.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.under_cut_defense)
            # if random number is less than 90, its a completion, else its a turnover
            if self.probabilityThrowIsCompleted < throwStartingProbability:
                randomYardsThrownOption = range(5, 15)
                randomChoice = random.randint(1, len(randomYardsThrownOption))
                self.discLocation += randomYardsThrownOption[randomChoice]
                if self.discLocation < -20:
                    # turnover, disc goes to goal line at location 0 and team 2 has disc
                    self.teamWithDisc = self.teamTwo
                    self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
                    self.playerGuardingDisc = self.defenderOptions[randomReceiver]
                elif 70 < self.discLocation < 90:
                    self.assistThrower = self.playerWithDisc
                    self.goalThrower = self.playerBeingThrownTo
                    self.pointWinner = self.teamOne
                    self.pointOver = True
                else:
                    self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
                    self.playerGuardingDisc = self.playerGuardingPlayerBeingThrownTo
            else:
                self.teamWithDisc = self.teamTwo
                self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
                self.playerGuardingDisc = self.receiverOptions[randomReceiver]
        elif self.throwChoice == 'short_huck':
            self.receiverOptions = [self.sevenOnFieldForTeamOne.all()[self.shortHuckReceiverOptionOne],
                                    self.sevenOnFieldForTeamOne.all()[self.shortHuckReceiverOptionTwo]]
            self.defenderOptions = [self.sevenOnFieldForTeamTwo.all()[self.shortHuckReceiverOptionOne],
                                    self.sevenOnFieldForTeamTwo.all()[self.shortHuckReceiverOptionTwo]]
            randomReceiver = random.randint(0, 1)
            self.playerBeingThrownTo = self.receiverOptions[randomReceiver]
            self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[randomReceiver]
            self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                                self.playerWithDisc.under_throw_offense + self.playerBeingThrownTo.under_cut_offense
                                                - self.playerGuardingDisc.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.under_cut_defense)
            # if random number is less than 90, its a completion, else its a turnover
            if self.probabilityThrowIsCompleted < throwStartingProbability:
                randomYardsThrownOption = range(15, 30)
                randomChoice = random.randint(1, len(randomYardsThrownOption))
                self.discLocation += randomYardsThrownOption[randomChoice]
                if self.discLocation < -20:
                    # turnover, disc goes to goal line at location 0 and team 2 has disc
                    self.teamWithDisc = self.teamTwo
                    self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
                    self.playerGuardingDisc = self.defenderOptions[randomReceiver]
                elif 70 < self.discLocation < 90:
                    self.assistThrower = self.playerWithDisc
                    self.goalThrower = self.playerBeingThrownTo
                    self.pointWinner = self.teamOne
                    self.pointOver = True
                else:
                    self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
                    self.playerGuardingDisc = self.playerGuardingPlayerBeingThrownTo
            else:
                self.teamWithDisc = self.teamTwo
                self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
                self.playerGuardingDisc = self.receiverOptions[randomReceiver]
        elif self.throwChoice == 'deep_huck':
            self.receiverOptions = [self.sevenOnFieldForTeamOne.all()[self.deepHuckReceiverOptionOne],
                                    self.sevenOnFieldForTeamOne.all()[self.deepHuckReceiverOptionTwo],
                                    self.sevenOnFieldForTeamOne.all()[self.deepHuckReceiverOptionThree],
                                    self.sevenOnFieldForTeamOne.all()[self.deepHuckReceiverOptionFour]]
            self.defenderOptions = [self.sevenOnFieldForTeamTwo.all()[self.deepHuckReceiverOptionOne],
                                    self.sevenOnFieldForTeamTwo.all()[self.deepHuckReceiverOptionTwo],
                                    self.sevenOnFieldForTeamTwo.all()[self.deepHuckReceiverOptionThree],
                                    self.sevenOnFieldForTeamTwo.all()[self.deepHuckReceiverOptionFour]]
            randomReceiver = random.randint(0, 3)
            self.playerBeingThrownTo = self.receiverOptions[randomReceiver]
            self.playerGuardingPlayerBeingThrownTo = self.defenderOptions[randomReceiver]
            self.probabilityThrowIsCompleted = (random.randint(1, 100) +
                                                self.playerWithDisc.under_throw_offense + self.playerBeingThrownTo.under_cut_offense
                                                - self.playerGuardingDisc.handle_mark_defense - self.playerGuardingPlayerBeingThrownTo.under_cut_defense)
            # if random number is less than 90, its a completion, else its a turnover
            if self.probabilityThrowIsCompleted < throwStartingProbability:
                randomYardsThrownOption = range(15, 30)
                randomChoice = random.randint(1, len(randomYardsThrownOption))
                self.discLocation += randomYardsThrownOption[randomChoice]
                if self.discLocation < -20:
                    # turnover, disc goes to goal line at location 0 and team 2 has disc
                    self.teamWithDisc = self.teamTwo
                    self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
                    self.playerGuardingDisc = self.defenderOptions[randomReceiver]
                elif 70 < self.discLocation < 90:
                    self.assistThrower = self.playerWithDisc
                    self.goalThrower = self.playerBeingThrownTo
                    self.pointWinner = self.teamOne
                    self.pointOver = True
                else:
                    self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
                    self.playerGuardingDisc = self.playerGuardingPlayerBeingThrownTo
            else:
                self.teamWithDisc = self.teamTwo
                self.playerWithDisc = self.playerGuardingPlayerBeingThrownTo
                self.playerGuardingDisc = self.receiverOptions[randomReceiver]


def simulate_play_until_score(self):
    # four pass options:
    # 1: swing for -5 to +5 yards (random number between 0-3
    # 2: under for 5 to 15 yards (random number between 4-6
    # 3: short huck for 15-30 yards (random number between 7-8)
    # 4: deep huck for 31-70 yards (cant go thru end of end zone) (random number == 9-10

    # Probability of Turnover
    while self.pointOver == False:
        if self.teamWithDisc == self.teamOne:
            # determine what throw is going to be thrown
            random_number = random.randint(0, 10)
            if random_number in [0, 1, 2, 3]:
                self.throwChoice = 'swing'
                self.simulate_throw(90)
            elif random_number in [4, 5, 6]:
                self.throwChoice = 'under'
                self.simulate_throw(80)
            elif random_number in [7, 8]:
                self.throwChoice = 'short_huck'
                self.simulate_throw(65)
            elif random_number in [9, 10]:
                self.throwChoice = 'deep_huck'
                self.simulate_throw(55)
